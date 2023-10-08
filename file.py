from validator import Validator
import os


class FileLines:
    def __init__(self, files_dir="/var/data/"):
        self.path = os.path.dirname(__file__) + files_dir
        if not os.path.exists(self.path):
            os.makedirs(self.path)

    def write_headers(self, headers, ext=".csv", delimiter=","):
        for key, value in headers.items():
            if not os.path.exists(self.path + key + ext):
                self.write_lines(key + ext, [delimiter.join(value)])

    def read_lines(self, filename: str) -> list:
        if not os.path.exists(self.path + filename):
            f = open(self.path + filename, "w")
            f.write("\n")
            f.close()
        with open(self.path + filename, 'r') as file_object:
            lines = file_object.read().splitlines()
        return lines

    def write_lines(self, filename: str, lines: list):
        with open(self.path + filename, 'w') as file_object:
            file_object.writelines("\n".join(lines))

    def append_line(self, filename: str, line: str):
        with open(self.path + filename, 'a') as file_object:
            file_object.write(line + "\n")


class FileImport:
    def __init__(self, path, filename=None) -> None:
        self.path = path
        self.filename = filename
        if filename:
            self.lines = FileLines(self.path).read_lines(self.filename)

    def get_files(self):
        files = []
        for file in os.listdir(self.path):
            entry_path = os.path.join(self.path, file)
            if os.path.isfile(entry_path):
                files.append(entry_path)
        return files

    def read_data(self, filename: str) -> list:
        if os.path.exists(self.path + filename):
            lines = FileLines(self.path).read_lines(filename)
            return lines[1:]
        return []

    def get_lines(self):
        return self.lines

    def save_file(self, file, file_name):
        if not os.path.exists(self.path):
            os.makedirs(self.path)
        file.save(os.path.join(self.path, file_name))

    def process_file(self, file, file_name, library):
        self.save_file(file, file_name)
        lines = FileLines('/var/import/').read_lines(file_name)
        validator = Validator()
        counter = 0
        for i in lines[1:]:
            line = i.split(",")
            book = {'title': line[1], 'author': line[2], "year": line[3]}
            if validator.validate(struct=book):
                library.storage.add_line('books', book)
                counter += 1
        return counter

    def import_file(self, file_name, library):
        with open(self.path + file_name, "r") as file:
            lines = file.readlines()
        counter = 0
        validator = Validator()
        for line in lines[1:]:
            line = line.replace('\n', '').split(',')
            book = {'title': line[1], 'author': line[2], "year": line[3]}
            if validator.validate(book):
                counter += 1
                library.storage.add_line('books', book)
        return counter
