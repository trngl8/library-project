INSERT INTO orders (first_name, last_name, email, phone, address, period, total_price, status, created)
VALUES
  ('Firstname', 'Lastname', 'test@test.com', '+380001111111', 'any street', 2, 10, 'new', '2018-01-01 00:00:00');

INSERT INTO books (title, author, publishing_year, isbn, available, created)
VALUES
  ('Book title', 'Book author', 2018, '1234567890123', 1, '2018-01-01 00:00:00');

INSERT INTO books_orders (order_id, book_id, price)
VALUES
  (1, 1, 10);






