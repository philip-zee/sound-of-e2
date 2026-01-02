class IMDatabase:
    def __init__(self):
        self.database = {}

    def select(self, key):
        if not self.__contains__(key):
            return None
        return self.database[key]

    def insert(self, key, value):
        if self.__contains__(key):
            raise ValueError("Key already exists.")
        else:
            self.database[key] = value
    
    def update(self, key, value):
        """Update an existing entry."""
        if key in self.database:
            self.database[key] |= value

    def __contains__(self, key):
        return key in self.database

    def __len__(self):
        return len(self.database)

    def __repr__(self):
        return f"IMDatabase({self.database})"
