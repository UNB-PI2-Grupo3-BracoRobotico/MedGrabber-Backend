CREATE OR REPLACE FUNCTION insert_new_product(p_product_name VARCHAR, p_product_description VARCHAR, p_product_price DECIMAL, p_modified_by_username VARCHAR)
RETURNS VOID AS $$
BEGIN
    INSERT INTO product (product_name, product_description, product_price, modified_by, modified_at)
    VALUES (p_product_name, p_product_description, p_product_price, 
        (SELECT user_id FROM users WHERE username = p_modified_by_username), NOW());
END; $$
LANGUAGE plpgsql;

CREATE OR REPLACE FUNCTION insert_new_order(p_user_username VARCHAR, p_order_date DATE, p_total_cost DECIMAL, p_order_status order_status_type)
RETURNS VOID AS $$
BEGIN
    INSERT INTO customer_order (user_id, order_date, total_cost, order_status)
    VALUES ((SELECT user_id FROM users WHERE username = p_user_username), p_order_date, p_total_cost, p_order_status);
END; $$
LANGUAGE plpgsql;

CREATE OR REPLACE FUNCTION insert_new_user(p_username VARCHAR, p_password_hash VARCHAR, p_email VARCHAR, p_store_name VARCHAR, p_personal_name VARCHAR, p_machine_serial_number VARCHAR, p_phone_number VARCHAR, p_user_role user_role_type)
RETURNS VOID AS $$
BEGIN
    INSERT INTO users (username, password_hash, email, store_name, personal_name, machine_serial_number, phone_number, user_role)
    VALUES (p_username, p_password_hash, p_email, p_store_name, p_personal_name, p_machine_serial_number, p_phone_number, p_user_role);
END; $$
LANGUAGE plpgsql;
