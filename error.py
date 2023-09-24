class DatabaseError(Exception):
    def __init__(self, message="Database error"):
        self.message = message


class DatabaseUndefinedError(DatabaseError):
    pass


class UniqueError(DatabaseError):
    pass


class EntityNotFound(DatabaseError):
    pass
