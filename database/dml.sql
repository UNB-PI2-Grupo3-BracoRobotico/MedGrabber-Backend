-- Insert a user
INSERT INTO users (username, password_hash, personal_name, user_role)
VALUES ('jdoe', 'hashed_password', 'John Doe', 'customer');

-- Insert a product
INSERT INTO product (product_name, product_description, product_price, modified_by)
VALUES ('Test Product', 'This is a test product.', 9.99, 1); -- assuming 1 is the user_id of the user who added this product

-- Insert an order
INSERT INTO order (user_id, order_date, total_cost, order_status)
VALUES (1, CURRENT_DATE, 9.99, 'created'); -- assuming 1 is the user_id of the customer

-- Insert an order_product
INSERT INTO order_product (order_id, product_id, product_amount)
VALUES (1, 1, 2); -- assuming 1 is the order_id and product_id

-- Insert a payment
INSERT INTO payment (order_id, payment_date, payment_method, payment_status)
VALUES (1, CURRENT_DATE, 'Credit Card', 'pending'); -- assuming 1 is the order_id
