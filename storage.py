import os
import csv


class DataStorage:

    def __init__(self):
        struct = {
            'books': [
                "ID", "TITLE", "AUTHOR", "YEAR", "ISBN", "AVAILABLE", "CREATED"
            ],
            'users': [
                "ID", "NAME", "EMAIL", "PHONE"
            ],
            'orders': [
                "ID", "FIRST_NAME", "LAST_NAME", "EMAIL", "PHONE", "ADDRESS", "PERIOD", "TOTAL_PRICE", "CREATED"
            ],
            'books_orders': [
                "ID", "BOOK_ID", "ORDER_ID", "PRICE"
            ]
        }
        self.ext = '.csv'
        self.path = os.path.dirname(__file__) + "/var/data/"
        for key, value in struct.items():
            if not os.path.exists(self.path + key + self.ext):
                with open(self.path + key + self.ext, 'w') as file_object:
                    file_object.write(",".join(value) + '\n')
        self.data = []

    def save_user(self, user):
        with open(self.path + "users.csv", "a") as file_object:
            file_object.write(user.name + ',' + user.email + ',' + user.phone + '\n')
        self.data.append([user.name, user.email, user.phone])

    def find_one(self, email) -> dict:
        for item in self.data:
            if item[1] == email:
                return {'name': item[0], 'email': item[1], 'phone': item[2]}
        raise Exception("User not found")

    def read_from_csv_catalog(self, filename):
        try:
            with open(self.path + filename + self.ext, 'r') as file:
                reader = csv.reader(file)
                reader = list(reader)
        except FileNotFoundError:
            print("Checkout if file exists in var/data/")
            return []
        return reader

    def get_file_lines(self, filename):
        with open(self.path + filename + self.ext, 'r') as file_object:
            lines = file_object.read().splitlines()
        return lines
