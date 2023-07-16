DROP TABLE IF EXISTS orders;

CREATE TABLE orders (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  first_name TEXT NOT NULL,
  second_name TEXT NOT NULL,
  email TEXT NOT NULL,
  phone TEXT NOT NULL,
  address TEXT NOT NULL,
  period INTEGER NOT NULL,
  total_price INTEGER NOT NULL,
  status TEXT NOT NULL,
  created TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE books (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  title TEXT NOT NULL,
  author TEXT NOT NULL,
  publishing_year INTEGER NOT NULL,
  isbn TEXT NOT NULL,
  available INTEGER NOT NULL,
  created TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE books_orders (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  order_id INTEGER NOT NULL,
  book_id INTEGER NOT NULL,
  price INTEGER NOT NULL,
  FOREIGN KEY (order_id) REFERENCES orders (id),
  FOREIGN KEY (book_id) REFERENCES books (id)
);
