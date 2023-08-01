from validator import Validator
from library import Book
import os


class FileImport:
    def get_file_lines(self, filename):
        with open(self.path + filename, 'r') as file_object:
            lines = file_object.read().splitlines()
        return lines

    def process_file(self, file_name):
        with open(os.path.join("var/import/" + file_name)) as file:
            file_containment = file.readlines()
        result = []
        result.append(file_containment[0])
        flag = False
        validator = Validator()
        for line in file_containment[1:]:
            line = line.replace('\n', '').split(",")
            book = Book(int(line[0]), line[1], line[2], int(line[3]))
            if validator.validate(book=book):
                for j in result:
                    try:
                        if j == book:
                            flag = True
                    except:
                        continue
            if not flag:
                result.append(book)
            flag = False
        with open(os.path.join("var/import/" + file_name), 'w') as file:
            file.write(result[0])
            for i in result[1:]:
                file.write(str(i.id) + "," + i.title + ',' + i.author + ',' + str(i.year) + '\n')