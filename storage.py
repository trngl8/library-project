import os
import csv


class FileLines:
    def __init__(self, files_dir="/var/data/"):
        self.path = os.path.dirname(__file__) + files_dir
        if not os.path.exists(self.path):
            os.makedirs(self.path)

    def write_headers(self, headers, ext=".csv"):
        for key, value in headers.items():
            if not os.path.exists(self.path + key + ext):
                with open(self.path + key + ext, 'w') as file_object:
                    file_object.write(",".join(value) + '\n')

    def read_lines(self, filename) -> list:
        with open(self.path + filename, 'r') as file_object:
            lines = file_object.read().splitlines()
        return lines

    def write_lines(self, filename, lines):
        with open(self.path + filename, "w") as file_object:
            file_object.writelines("\n".join(lines))

    def write_line(self, filename, line):
        with open(self.path + filename, "a") as file_object:
            file_object.write(line + "\n")


class DataStorage:

    def __init__(self, file_lines: FileLines):
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
        self.lines = file_lines
        self.path = file_lines.path
        self.lines.write_headers(struct, self.ext)
        self.data = {}
        self.counters = {}
        self.headers = {}

    def save_user(self, user):
        with open(self.path + "users.csv", "a") as file_object:
            file_object.write(user.name + ',' + user.email + ',' + user.phone + '\n')
        # self.data.append([user.name, user.email, user.phone])

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

    def get_lines(self, entity_name):
        # if entity_name in self.data:
        #     return self.data[entity_name]
        lines = self.lines.read_lines(entity_name + self.ext)
        self.headers[entity_name] = lines.pop(0)
        self.counters[entity_name] = len(lines)
        self.data[entity_name] = lines
        return self.data[entity_name]

    def add_line(self, entity_name, item) -> int:
        if entity_name not in self.data:
            self.get_lines(entity_name)
        new_id = self.counters[entity_name] + 1
        line = str(new_id) + "," + ",".join(item.values())
        self.lines.write_line(entity_name + self.ext, line)
        self.counters[entity_name] = new_id
        self.data[entity_name].append(line)
        return new_id

    def remove_line(self, entity_name, item_id):
        if entity_name not in self.data:
            self.get_lines(entity_name)
        self.counters[entity_name] -= 1
        del self.data[entity_name][int(item_id) - 1]
        self.lines.write_lines(entity_name + self.ext, self.data[entity_name])

    def get_header(self, entity_name):
        if entity_name not in self.headers:
            self.get_lines(entity_name)
        return self.headers[entity_name]

    def get_count(self, entity_name):
        if entity_name not in self.counters:
            self.get_lines(entity_name)
        return self.counters[entity_name]
