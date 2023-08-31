class DatabaseError(Exception):
    def __init__(self, message):
        self.message = message


class DatabaseUndefinedError(DatabaseError):
    pass


class UniqueError(DatabaseError):
    pass
