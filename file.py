from validator import Validator
from library import Book
import os


def process_lines(lines) -> int:
    # TODO: implement saving lines to storage
    return len(lines) - 1


class FileImport:
    def __init__(self, path) -> None:
        self.path = path

    def get_file_lines(self, filename):
        with open(self.path + filename, 'r') as file_object:
            lines = file_object.read().splitlines()
        return lines

    def save_file(self, file, file_name):
        file.save(os.path.join(self.path, file_name))
        with open(os.path.join("var/import/" + file_name)) as file:
            file_containment = file.readlines()
            print(file_containment)
            return file_containment
        
    def write_new_file(self, file_name, result):
        with open(os.path.join("var/import/" + file_name), 'w') as file:
            file.write(result[0])
            for i in result[1:]:
                if i == result[-1]:
                    file.write(str(i.id) + "," + i.title + ',' + i.author + ',' + str(i.year))
                else:
                    file.write(str(i.id) + "," + i.title + ',' + i.author + ',' + str(i.year) + '\n')

    def process_file(self, file, file_name):
        file_containment = self.save_file(file, file_name)
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
        self.write_new_file(file_name, result)
        return len(result) - 1
