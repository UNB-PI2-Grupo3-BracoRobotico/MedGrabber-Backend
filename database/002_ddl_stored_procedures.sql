CREATE OR REPLACE FUNCTION insert_new_product(p_product_name VARCHAR, p_product_description VARCHAR, p_product_price DECIMAL(10,2), p_modified_by_username VARCHAR)
RETURNS VOID AS $$
DECLARE
  user_role user_role_type;
  user_id INTEGER;
BEGIN
    SELECT users.user_role, users.user_id INTO user_role, user_id
    FROM users
    WHERE users.username = p_modified_by_username;

    IF user_role = 'stock_manager' THEN
        INSERT INTO product (product_name, product_description, product_price, modified_by, modified_at)
        VALUES (p_product_name, p_product_description, p_product_price, user_id, CURRENT_TIMESTAMP);
    ELSE
        RAISE EXCEPTION 'User role must be "stock_manager" to insert a new product';
    END IF;
END; $$
LANGUAGE plpgsql;


CREATE OR REPLACE FUNCTION insert_new_order(p_user_username VARCHAR, p_order_date DATE, p_total_cost DECIMAL, p_order_status order_status_type)
RETURNS VOID AS $$
BEGIN
    INSERT INTO customer_order (user_id, order_date, total_cost, order_status)
    VALUES ((SELECT user_id FROM users WHERE username = p_user_username), p_order_date, p_total_cost, p_order_status);
END; $$
LANGUAGE plpgsql;

CREATE OR REPLACE FUNCTION upsert_user(p_username VARCHAR, p_password_hash VARCHAR, p_email VARCHAR, p_store_name VARCHAR, p_personal_name VARCHAR, p_machine_serial_number VARCHAR, p_phone_number VARCHAR, p_user_role user_role_type)
RETURNS VOID AS $$
BEGIN
    IF EXISTS (SELECT 1 FROM users WHERE username = p_username) THEN
        UPDATE users SET
            password_hash = p_password_hash,
            email = p_email,
            store_name = p_store_name,
            personal_name = p_personal_name,
            machine_serial_number = p_machine_serial_number,
            phone_number = p_phone_number,
            user_role = p_user_role
        WHERE username = p_username;
    ELSE
        INSERT INTO users (username, password_hash, email, store_name, personal_name, machine_serial_number, phone_number, user_role)
        VALUES (p_username, p_password_hash, p_email, p_store_name, p_personal_name, p_machine_serial_number, p_phone_number, p_user_role);
    END IF;
END; $$
LANGUAGE plpgsql;

CREATE OR REPLACE FUNCTION insert_position(
    p_position_x INTEGER,
    p_position_y INTEGER,
    p_product_id INTEGER,
    p_product_amount INTEGER,
    p_modified_by_username VARCHAR(50),
    p_is_exit BOOLEAN DEFAULT FALSE
) RETURNS VOID AS $$
DECLARE
    v_modified_by_id INTEGER;
BEGIN

    SELECT user_id INTO v_modified_by_id FROM users WHERE username = p_modified_by_username;

    IF v_modified_by_id IS NULL THEN
        RAISE 'User % not found', p_modified_by_username;
    END IF;

    IF p_is_exit AND p_product_id IS NOT NULL THEN
        RAISE 'Cannot add product to an exit position';
    END IF;

    IF EXISTS (SELECT 1 FROM position WHERE position_x = p_position_x AND position_y = p_position_y) THEN
        UPDATE position
        SET product_id = p_product_id,
            product_amount = p_product_amount,
            modified_by = v_modified_by_id,
            modified_at = CURRENT_TIMESTAMP,
            is_exit = p_is_exit
        WHERE position_x = p_position_x AND position_y = p_position_y;
    ELSE
        INSERT INTO position (position_x, position_y, product_id, product_amount, modified_by, modified_at, is_exit)
        VALUES (p_position_x, p_position_y, p_product_id, p_product_amount, v_modified_by_id, CURRENT_TIMESTAMP, p_is_exit);
    END IF;

    COMMIT;
END;
$$ LANGUAGE plpgsql;


CREATE OR REPLACE FUNCTION initialize_positions() RETURNS VOID AS $$
DECLARE
    v_position_x INTEGER;
    v_position_y INTEGER;
BEGIN
    FOR v_position_x IN 1..5 LOOP
        FOR v_position_y IN 1..5 LOOP
            INSERT INTO position (position_x, position_y, is_exit)
            VALUES (v_position_x, v_position_y, FALSE)
            ON CONFLICT (position_x, position_y) DO NOTHING;
        END LOOP;
    END LOOP;
    -- Set a position as an exit point
    UPDATE position SET is_exit = TRUE WHERE position_x = 5 AND position_y = 5;
EXCEPTION
    WHEN OTHERS THEN
        RAISE EXCEPTION 'Failed to initialize positions: %', SQLERRM;
END;
$$ LANGUAGE plpgsql;


CREATE OR REPLACE FUNCTION create_product_and_position(
    p_product_name VARCHAR(50),
    p_product_description VARCHAR(300),
    p_product_price DECIMAL(10,2),
    p_peso DECIMAL(8,2),
    p_size product_size_enum,
    p_modified_by_username VARCHAR(50),
    p_position_x INTEGER,
    p_position_y INTEGER,
    p_product_amount INTEGER
) RETURNS VOID AS $$
DECLARE
    v_user_id INTEGER;
    v_product_id INTEGER;
    v_product_exists INTEGER;
BEGIN
    SELECT user_id INTO v_user_id FROM users WHERE username = p_modified_by_username;
    IF NOT FOUND THEN
        RAISE EXCEPTION 'User not found';
    END IF;

    SELECT product_id INTO v_product_exists FROM position WHERE position_x = p_position_x AND position_y = p_position_y AND is_exit = FALSE;
    IF v_product_exists IS NOT NULL THEN
        RAISE EXCEPTION 'Product already exists at the specified position';
    END IF;

    INSERT INTO product (product_name, product_description, product_price, peso, size, modified_by, modified_at)
    VALUES (p_product_name, p_product_description, p_product_price, p_peso, p_size, v_user_id, CURRENT_TIMESTAMP)
    RETURNING product_id INTO v_product_id;

    UPDATE position
    SET product_id = v_product_id,
        product_amount = p_product_amount,
        modified_by = v_user_id,
        modified_at = CURRENT_TIMESTAMP
    WHERE position_x = p_position_x AND position_y = p_position_y AND is_exit = FALSE;

    IF NOT FOUND THEN
        RAISE EXCEPTION 'Position not found or is an exit';
    END IF;
EXCEPTION
    WHEN OTHERS THEN
        RAISE EXCEPTION 'Failed to insert product: % - %', p_product_name, SQLERRM;
END;
$$ LANGUAGE plpgsql;



CREATE OR REPLACE FUNCTION update_product_and_position(
    p_product_id INTEGER,
    p_product_name VARCHAR(50),
    p_product_description VARCHAR(300),
    p_product_price DECIMAL(10,2),
    p_peso DECIMAL(8,2),
    p_size product_size_enum,
    p_modified_by_username VARCHAR(50),
    p_position_x INTEGER,
    p_position_y INTEGER,
    p_product_amount INTEGER
) RETURNS VOID AS $$
DECLARE
    v_user_id INTEGER;
BEGIN
    SELECT user_id INTO v_user_id FROM users WHERE username = p_modified_by_username;
    IF NOT FOUND THEN
        RAISE EXCEPTION 'User not found';
    END IF;

    UPDATE product
    SET
        product_name = p_product_name,
        product_description = p_product_description,
        product_price = p_product_price,
        peso = p_peso,
        size = p_size,
        modified_by = v_user_id,
        modified_at = CURRENT_TIMESTAMP
    WHERE
        product_id = p_product_id;

    IF NOT FOUND THEN
        RAISE EXCEPTION 'Product not found';
    END IF;

    UPDATE position
    SET product_amount = p_product_amount,
        modified_by = v_user_id,
        modified_at = CURRENT_TIMESTAMP
        position_x = p_position_x
        position_y = p_position_y
    WHERE product_id = p_product_id
        AND is_exit = FALSE;

    IF NOT FOUND THEN
        RAISE EXCEPTION 'Position not found or is an exit';
    END IF;
EXCEPTION
    WHEN OTHERS THEN
        RAISE EXCEPTION 'Failed to update product: % - %', p_product_id, SQLERRM;
END;
$$ LANGUAGE plpgsql;
