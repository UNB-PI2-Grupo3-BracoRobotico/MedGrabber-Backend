-- -- Insert a user
-- INSERT INTO users (username, password_hash, email, store_name, personal_name, machine_serial_number, phone_number, user_role) 
-- VALUES 
-- ('johnsmith', 'hashedpassword1', 'johnsmith1@example.com', 'Smith Store 1', 'John Smith 1', '123ABC', '1234567891', 'stock_manager'),
-- ('janedoe', 'hashedpassword2', 'janedoe@example.com', 'Doe Store', 'Jane Doe', '456DEF', '1234567892', 'customer'),
-- ('alexjohnson', 'hashedpassword3', 'alexjohnson@example.com', 'Johnson Store', 'Alex Johnson', '789GHI', '1234567893', 'customer'),
-- ('emilywhite', 'hashedpassword4', 'emilywhite@example.com', 'White Store', 'Emily White', '012JKL', '1234567894', 'stock_manager'),
-- ('michaelgreen', 'hashedpassword5', 'michaelgreen@example.com', 'Green Store', 'Michael Green', '345MNO', '1234567895', 'customer');

-- INSERT INTO product (product_name, product_description, product_price, modified_by, modified_at)
-- VALUES 
-- ('Apple', 'A tasty fruit', 1.50, 11, CURRENT_TIMESTAMP),
-- ('Orange', 'Citrus fruit', 2.00, 12, CURRENT_TIMESTAMP),
-- ('Banana', 'Perfect for smoothies', 1.20, 13, CURRENT_TIMESTAMP),
-- ('Grape', 'Great in fruit salads', 3.00, 14, CURRENT_TIMESTAMP),
-- ('Pineapple', 'Sweet and tangy', 4.00, 15, CURRENT_TIMESTAMP);

-- INSERT INTO customer_order (user_id, order_date, total_cost, order_status)
-- VALUES 
-- (12, CURRENT_DATE, 10.00, 'created'),
-- (13, CURRENT_DATE, 15.00, 'pending'),
-- (15, CURRENT_DATE, 20.00, 'paid'),
-- (12, CURRENT_DATE, 25.00, 'delivered'),
-- (13, CURRENT_DATE, 30.00, 'canceled');

-- INSERT INTO order_product (customer_order_id, product_id, product_amount)
-- VALUES 
-- (6, 16, 5),
-- (7, 17, 7),
-- (8, 18, 4),
-- (9, 19, 6),
-- (10, 20, 3);

-- INSERT INTO payment (customer_order_id, payment_date, payment_method, payment_status)
-- VALUES 
-- (6, CURRENT_DATE, 'Credit Card', 'pending'),
-- (7, CURRENT_DATE, 'Debit Card', 'paid'),
-- (8, CURRENT_DATE, 'Paypal', 'canceled'),
-- (9, CURRENT_DATE, 'Credit Card', 'pending'),
-- (10, CURRENT_DATE, 'Debit Card', 'paid');

-- INSERT INTO position (position_x, position_y, product_id, product_amount, modified_by, modified_at)
-- VALUES 
-- (1, 1, 16, 20, 11, CURRENT_TIMESTAMP),
-- (2, 2, 17, 15, 12, CURRENT_TIMESTAMP),
-- (3, 3, 18, 10, 13, CURRENT_TIMESTAMP),
-- (4, 4, 19, 25, 14, CURRENT_TIMESTAMP),
-- (5, 5, 20, 30, 15, CURRENT_TIMESTAMP);
