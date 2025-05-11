-- Add a sample admin user
INSERT INTO users (username, password, email, role, confirmed)
VALUES ('admin', 'admin123', 'admin@example.com', 'super', 1);

-- Add sample locations
INSERT INTO locations (name, latitude, longitude)
VALUES ('Farm Lane A', 49.2123, -2.1356);

-- Add sample products
INSERT INTO products (name, description, price, location_id)
VALUES ('Free Range Eggs', 'Box of 6 large eggs', 2.50, 1);

-- Add sample order
INSERT INTO orders (user_id, product_id, quantity, total_price)
VALUES (1, 1, 2, 5.00);

