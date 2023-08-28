from validator import Validator
from library import Book, Library
import os


class FileImport:
    def __init__(self, path) -> None:
        self.path = path

    def get_dir_files(self, dirname):
        files = []
        for file in os.listdir(dirname):
            entry_path = os.path.join(dirname, file)
            if os.path.isfile(entry_path):
                files.append(entry_path)
        return files

    def get_file_lines(self, filename):
        with open(self.path + filename, 'r') as file_object:
            lines = file_object.read().splitlines()
        return lines

    def save_file(self, file, file_name):
        if not os.path.exists(self.path):
            os.makedirs(self.path)
        file.save(os.path.join(self.path, file_name))
        with open(os.path.join("var/import/" + file_name), 'r') as file:
            file_containment = file.readlines()
            return file_containment
        
    def write_new_file(self, file_name, result, library,  flag=True):
        if flag == True:
            path = "var/import/"
        else:
            path = "var/data/"
        with open(os.path.join(path + file_name), 'w') as file:
            file.write(result[0])
            for i in result[1:]:
                library.storage.add_line("books", {"title" : i.title, "author": i.author, "year" : str(i.year)})

    def process_file(self, file, file_name, library):
        file_containment = self.save_file(file, file_name)
        result = []
        result.append(file_containment[0])
        flag = False
        validator = Validator()
        for num, line in enumerate(file_containment[1:]):
            line = line.replace('\n', '').split(",")
            book = Book(line[1], line[2], int(line[3]))
            book.id = num + 1
            if validator.validate(object=book):
                for j in result:
                    try:
                        if j == book:
                            flag = True
                    except:
                        continue
            if not flag:
                result.append(book)
            flag = False
        self.write_new_file(file_name, result, library=library, flag=False)
        return len(result) - 1

    def import_file(self, file_name, library : Library):
        with open(self.path + file_name, "r") as file:
            lines = file.readlines()
        counter = 0
        validator = Validator()
        for line in lines[1:]:
            line = line.replace('\n', '').split(',')
            if validator.validate(Book(line[1], line[2], line[3])):
                counter += 1
                library.storage.add_line('books', {'title' : line[1], 'author' : line[2], "year" : line[3]})
        return counter
