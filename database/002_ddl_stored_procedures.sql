CREATE OR REPLACE FUNCTION insert_new_product(p_product_name VARCHAR, p_product_description VARCHAR, p_product_price DECIMAL(10,2), p_modified_by_user_id VARCHAR)
RETURNS VOID AS $$
BEGIN
    INSERT INTO product (product_name, product_description, product_price, modified_by, modified_at)
    VALUES (p_product_name, p_product_description, p_product_price, p_modified_by_user_id, CURRENT_TIMESTAMP);  
END; $$
LANGUAGE plpgsql;

CREATE OR REPLACE FUNCTION insert_new_order(p_user_user_id VARCHAR, p_order_date DATE, p_total_cost DECIMAL, p_order_status order_status_type)
RETURNS INTEGER AS $$
DECLARE 
    new_order_id INTEGER;
BEGIN
    INSERT INTO customer_order (user_id, order_date, total_cost, order_status)
    VALUES ((SELECT user_id FROM users WHERE user_id = p_user_user_id), p_order_date, p_total_cost, p_order_status)
    RETURNING customer_order_id INTO new_order_id;

    RETURN new_order_id;
END; $$
LANGUAGE plpgsql;

CREATE OR REPLACE FUNCTION upsert_user(p_user_id VARCHAR, p_email VARCHAR, p_store_name VARCHAR, p_machine_serial_number VARCHAR, p_phone_number VARCHAR)
RETURNS VOID AS $$
BEGIN
    IF EXISTS (SELECT 1 FROM users WHERE user_id = p_user_id) THEN
        UPDATE users SET
            email = p_email,
            store_name = p_store_name,
            machine_serial_number = p_machine_serial_number,
            phone_number = p_phone_number
        WHERE user_id = p_user_id;
    ELSE
        INSERT INTO users (user_id, email, store_name, machine_serial_number, phone_number)
        VALUES (p_user_id, p_email, p_store_name, p_machine_serial_number, p_phone_number);
    END IF;
END; $$
LANGUAGE plpgsql;


CREATE OR REPLACE FUNCTION insert_position(
    p_position_x INTEGER,
    p_position_y INTEGER,
    p_product_id INTEGER,
    p_product_amount INTEGER,
    p_modified_by_user_id VARCHAR(50),
    p_is_exit BOOLEAN DEFAULT FALSE
) RETURNS VOID AS $$
DECLARE
    v_modified_by_id INTEGER;
BEGIN

    SELECT user_id INTO v_modified_by_id FROM users WHERE user_id = p_modified_by_user_id;

    IF v_modified_by_id IS NULL THEN
        RAISE 'User % not found', p_modified_by_user_id;
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
    FOR v_position_x IN 0..6 LOOP
        FOR v_position_y IN 0..4 LOOP
            INSERT INTO position (position_x, position_y, is_exit)
            VALUES (v_position_x, v_position_y, FALSE)
            ON CONFLICT (position_x, position_y) DO NOTHING;
        END LOOP;
    END LOOP;
    -- Set a position as an exit point
    UPDATE position SET is_exit = TRUE WHERE position_x = 0 AND position_y = 0;
    UPDATE position SET is_exit = TRUE WHERE position_x = 0 AND position_y = 1;
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
    p_modified_by_user_id VARCHAR(128),
    p_position_x INTEGER,
    p_position_y INTEGER,
    p_product_amount INTEGER
) RETURNS VOID AS $$
DECLARE
    v_product_id INTEGER;
    v_product_exists INTEGER;
BEGIN

    SELECT product_id INTO v_product_exists FROM position WHERE position_x = p_position_x AND position_y = p_position_y AND is_exit = FALSE;
    IF v_product_exists IS NOT NULL THEN
        RAISE EXCEPTION 'Product already exists at the specified position';
    END IF;

    INSERT INTO product (product_name, product_description, product_price, peso, size, modified_by, modified_at)
    VALUES (p_product_name, p_product_description, p_product_price, p_peso, p_size, p_modified_by_user_id, CURRENT_TIMESTAMP)
    RETURNING product_id INTO v_product_id;
    
    INSERT INTO product_aud (product_id, product_name, product_description, product_price, peso, size, modified_by, aud_status, modified_at)
    VALUES (v_product_id, p_product_name, p_product_description, p_product_price, p_peso, p_size, p_modified_by_user_id, 'created' , CURRENT_TIMESTAMP);

    UPDATE position
    SET product_id = v_product_id,
        product_amount = p_product_amount,
        modified_by = p_modified_by_user_id,
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


CREATE OR REPLACE FUNCTION delete_product(
    p_product_id INTEGER,
    p_modified_by_user_id VARCHAR(128)
)  RETURNS VOID AS $$
DECLARE
    v_product_name VARCHAR(50);
    v_product_description VARCHAR(300);
    v_product_price DECIMAL(10,2);
    v_peso DECIMAL(8,2);
    v_size product_size_enum;
BEGIN
    UPDATE position
        SET product_id = NULL,
            product_amount = 0,
            modified_by = p_modified_by_user_id,
            modified_at = CURRENT_TIMESTAMP
        WHERE product_id = p_product_id
            AND is_exit = FALSE;
    
    IF NOT FOUND THEN
        RAISE EXCEPTION 'Position not found or is an exit';
    END IF;

    SELECT 
        product_name, 
        product_description, 
        product_price, 
        peso, 
        size
    INTO 
        v_product_name, 
        v_product_description, 
        v_product_price, 
        v_peso, 
        v_size
    FROM product
    WHERE product_id = p_product_id;

    INSERT INTO product_aud (product_id, product_name, product_description, product_price, peso, size, modified_by, aud_status, modified_at)
    VALUES (p_product_id, v_product_name, v_product_description, v_product_price, v_peso, v_size, p_modified_by_user_id, 'deleted' , CURRENT_TIMESTAMP);

    UPDATE product
        SET is_hidden = TRUE
        WHERE product_id = p_product_id;

    IF NOT FOUND THEN
        RAISE EXCEPTION 'Product not found, cannot be deleted';
    END IF;
END
$$ LANGUAGE plpgsql;

CREATE OR REPLACE FUNCTION update_product(
    p_product_id INTEGER,
    p_product_name VARCHAR(50),
    p_product_description VARCHAR(300),
    p_product_price DECIMAL(10,2),
    p_peso DECIMAL(8,2),
    p_size product_size_enum,
    p_modified_by_user VARCHAR(128),
    p_position_x INTEGER,
    p_position_y INTEGER,
    p_product_amount INTEGER
)  RETURNS VOID AS $$
BEGIN
    UPDATE position
        SET product_id = NULL,
        product_amount = 0,
        modified_at = CURRENT_TIMESTAMP,
        modified_by = p_modified_by_user
        WHERE
            product_id = p_product_id;    

    IF NOT FOUND THEN
        RAISE EXCEPTION 'Position not found or is an exit';
    END IF;

    UPDATE position
        SET product_id = p_product_id,
            product_amount = p_product_amount,
            modified_by = p_modified_by_user,
            modified_at = CURRENT_TIMESTAMP
        WHERE 
            position_x = p_position_x
            AND position_y = p_position_y
            AND is_exit = FALSE; 

    IF NOT FOUND THEN
        RAISE EXCEPTION 'Position not found or is an exit';
    END IF;

    UPDATE product
        SET
            product_name = p_product_name,
            product_description = p_product_description,
            product_price = p_product_price,
            peso = p_peso,
            size = p_size,
            modified_by = p_modified_by_user,
            modified_at = CURRENT_TIMESTAMP
        WHERE
            product_id = p_product_id;
    
    IF NOT FOUND THEN
        RAISE EXCEPTION 'Product not founded';
    END IF;

    INSERT INTO product_aud (product_id, product_name, product_description, product_price, peso, size, modified_by, aud_status, modified_at)
    VALUES (p_product_id, p_product_name, p_product_description, p_product_price, p_peso, p_size, p_modified_by_user, 'edited' , CURRENT_TIMESTAMP);
END
$$ LANGUAGE plpgsql;

CREATE OR REPLACE PROCEDURE insert_order_product_and_update_position(
    _customer_order_id INTEGER,
    _product_id INTEGER,
    _product_amount INTEGER,
    _modified_by VARCHAR(128)
)
LANGUAGE plpgsql
AS $$
DECLARE
    _position RECORD;
BEGIN
    -- Get position based on the product_id with the most quantity
    SELECT position_x, position_y, product_amount INTO _position
    FROM position
    WHERE product_id = _product_id 
    ORDER BY product_amount DESC
    LIMIT 1;

    -- Check if there is enough product_amount in the position
    IF _position.product_amount < _product_amount THEN
        RAISE EXCEPTION 'Not enough product in position';
    END IF;

    -- Insert into order_product
    INSERT INTO order_product (
        customer_order_id,
        product_id,
        product_amount
    ) VALUES (
        _customer_order_id,
        _product_id,
        _product_amount
    );

    -- Subtract product_amount from position
    UPDATE position
    SET product_amount = product_amount - _product_amount, modified_by = _modified_by, modified_at = CURRENT_TIMESTAMP
    WHERE position_x = _position.position_x AND position_y = _position.position_y;
END;
$$;
