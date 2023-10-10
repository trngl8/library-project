from validator import Validator
import os


class Directory:
    def __init__(self, files_dir="var/data/"):
        self._relative_path = files_dir
        self._path = os.path.dirname(__file__) + files_dir
        if not os.path.exists(self._path):
            os.makedirs(self._path)

    def file(self, filename):
        return File(self._relative_path + filename)

    @property
    def path(self):
        return self._path

    @property
    def relative_path(self):
        return self._relative_path

    def get_files(self):
        files = []
        for file in os.listdir(self._path):
            entry_path = os.path.join(self._path, file)
            if os.path.isfile(entry_path):
                files.append(entry_path)
        return files


class File(Directory):
    def __init__(self, filename):
        relative_dir = os.path.dirname(filename)
        absolute_dir = os.path.dirname(__file__)
        super().__init__(relative_dir)
        if not os.path.exists(absolute_dir + '/' + filename):
            raise FileNotFoundError(f"File {filename} not found in {absolute_dir}")

    def write_headers(self, headers, ext=".csv", delimiter=","):
        for key, value in headers.items():
            if not os.path.exists(self.path + key + ext):
                self.write_lines(key + ext, [delimiter.join(value)])

    def lines (self, filename):
        return self.read_lines(filename)

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
    def __init__(self, path, filename) -> None:
        self.path = path
        self.filename = filename
        self._lines = File(self.path + self.filename).read_lines(self.filename)

    @property
    def lines(self):
        return self._lines

    def save_file(self, file, file_name):
        file.save(os.path.join(self.path, file_name))

    def process_file(self, file, file_name, library):
        if not os.path.exists(self.path):
            os.makedirs(self.path)
        file.save(os.path.join(self.path, file_name))
        lines = File('/var/import/').read_lines(file_name)
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
