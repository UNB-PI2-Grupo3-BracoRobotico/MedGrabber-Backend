CREATE TYPE user_role_type as ENUM ('customer', 'stock_manager');

CREATE TYPE order_status_type as ENUM (
    'created', 'pending', 'paid', 'separation', 'delivered', 'canceled'
);

CREATE TYPE product_size_enum AS ENUM ('P', 'M', 'G');

CREATE TYPE payment_status_type as ENUM ('pending', 'paid', 'canceled');

CREATE TABLE users (
    user_id SERIAL PRIMARY KEY,
    username VARCHAR(50) NOT NULL,
    password_hash VARCHAR(50) NOT NULL,
    email VARCHAR(50),
    store_name VARCHAR(50),
    personal_name VARCHAR(50) NOT NULL,
    machine_serial_number VARCHAR(50),
    phone_number VARCHAR(50) UNIQUE,
    user_role user_role_type
);

CREATE TABLE product (
    product_id SERIAL PRIMARY KEY,
    product_name VARCHAR(50),
    product_description VARCHAR(300),
    product_price DECIMAL(10,2),
    modified_by INTEGER,
    modified_at TIMESTAMP,
    peso DECIMAL(8,2),
    size product_size_enum,
    FOREIGN KEY (modified_by) REFERENCES users(user_id)
);

CREATE TABLE customer_order (
    customer_order_id SERIAL PRIMARY KEY,
    user_id INTEGER,
    order_date DATE,
    total_cost DECIMAL(10,2),
    order_status order_status_type,
    FOREIGN KEY (user_id) REFERENCES users(user_id)
);

CREATE TABLE order_product (
    customer_order_id INTEGER,
    product_id INTEGER,
    product_amount INTEGER,
    PRIMARY KEY (customer_order_id, product_id),
    FOREIGN KEY (customer_order_id) REFERENCES customer_order(customer_order_id),
    FOREIGN KEY (product_id) REFERENCES product(product_id)
);

CREATE TABLE payment (
    payment_id SERIAL PRIMARY KEY,
    customer_order_id INTEGER,
    payment_date DATE,
    payment_method VARCHAR(50),
    payment_status payment_status_type,
    FOREIGN KEY (customer_order_id) REFERENCES customer_order(customer_order_id)
);

CREATE TABLE position (
    position_x INTEGER,
    position_y INTEGER,
    product_id INTEGER,
    product_amount INTEGER,
    modified_by INTEGER,
    modified_at TIMESTAMP,
    is_exit BOOLEAN NOT NULL DEFAULT FALSE,
    PRIMARY KEY (position_x, position_y),
    FOREIGN KEY (modified_by) REFERENCES users(user_id),
    FOREIGN KEY (product_id) REFERENCES product(product_id),
    CONSTRAINT no_product_on_exit CHECK ((is_exit = FALSE) OR (is_exit = TRUE AND product_id IS NULL))
);
