from tinydb import TinyDB, Query

import constants

KEY = 'KEY'
VALUE = 'VALUE'
Q = Query()


class Storage:
    def __init__(self):
        self.db = TinyDB(constants.TINY_DB_FILE_PATH)

    def get(self, key):
        results = self.db.search(Q[KEY] == key)
        return results[0][VALUE] if len(results) >= 0 else None

    def get_all(self):
        return {item[KEY]: item[VALUE] for item in self.db.all()}

    def put(self, key, value):
        self.db.upsert({KEY: key, VALUE: value}, Q[KEY] == key)

    def remove(self, key):
        self.db.remove(Q[KEY] == key)

    def contains_key(self, key):
        return len(self.db.search(Q[KEY] == key)) > 0

    def clear(self):
        self.db.purge()

    def size(self):
        return len(self.db)
