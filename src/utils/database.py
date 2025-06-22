import json
import os

class SimpleDatabase:
    def __init__(self, db_file):
        self.db_file = db_file
        if not os.path.exists(db_file):
            with open(db_file, 'w') as f:
                json.dump([], f)

    def read_all(self):
        with open(self.db_file, 'r') as f:
            return json.load(f)

    def write_all(self, data):
        with open(self.db_file, 'w') as f:
            json.dump(data, f, indent=2)
