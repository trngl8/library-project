import os
import csv


class DataStorage:

    def __init__(self):
        struct = {
            'books': [
                "ID", "TITLE", "AUTHOR", "YEAR", "ISBN"
            ],
            'users': [
                "NAME", "EMAIL", "PHONE"
            ]
        }
        self.path = "var/data"
        if not os.path.exists("var/data/users.csv"):
            open("var/data/users.csv", 'w')
        self.data = []
        #self.read_from_csv_catalog(path + "/books.csv")

    def save_user(self, user):
        with open("var/data/users.csv", "a") as file_object:
            file_object.write(user.name + ',' + user.email + ',' + user.phone + '\n')
        self.data.append([user.name, user.email, user.phone])

    def find_one(self, email) -> dict:
        for item in self.data:
            if item[1] == email:
                return {'name': item[0], 'email': item[1], 'phone': item[2]}
        raise Exception("User not found")

    def read_from_csv_catalog(self):
        try:
            with open(self.path, 'r') as file:
                reader = csv.reader(file)
                reader = list(reader)
        except FileNotFoundError:
            print("Checkout if file exists in var/data/")
            return []
        return reader
