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
    p_position_id INTEGER,
    p_position_x INTEGER,
    p_position_y INTEGER,
    p_product_id INTEGER,
    p_product_amount INTEGER,
    p_modified_by_username VARCHAR(50)
) RETURNS VOID AS $$
BEGIN
    
    IF EXISTS (SELECT 1 FROM position WHERE position_id = p_position_id) THEN
        
        UPDATE position
        SET position_x = p_position_x,
            position_y = p_position_y,
            product_id = p_product_id,
            product_amount = p_product_amount,
            modified_by_username = p_modified_by_username,
            modified_at = CURRENT_TIMESTAMP
        WHERE position_id = p_position_id;
    ELSE
        
        INSERT INTO position (position_id, position_x, position_y, product_id, product_amount, modified_by_username, modified_at)
        VALUES (p_position_id, p_position_x, p_position_y, p_product_id, p_product_amount, p_modified_by_username, CURRENT_TIMESTAMP);
    END IF;
    
    COMMIT;
END;
$$ LANGUAGE plpgsql;
