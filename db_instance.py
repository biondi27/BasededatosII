import json
import threading
import os

class SimpleDB:
    def __init__(self, filename):
        self.filename = filename
        self.lock = threading.Lock()
        self._ensure_file()

    def _ensure_file(self):
        if not os.path.exists(self.filename):
            with open(self.filename, 'w') as f:
                json.dump({}, f)

    def read_all(self):
        with self.lock:
            try:
                with open(self.filename, 'r') as f:
                    return json.load(f)
            except (json.JSONDecodeError, FileNotFoundError):
                return {}

    def write_data(self, key, value):
        with self.lock:
            try:
                with open(self.filename, 'r') as f:
                    data = json.load(f)
            except (json.JSONDecodeError, FileNotFoundError):
                data = {}

            data[key] = value

            with open(self.filename, 'w') as f:
                json.dump(data, f)

    def delete_data(self, key):
        with self.lock:
            try:
                with open(self.filename, 'r') as f:
                    data = json.load(f)
            except (json.JSONDecodeError, FileNotFoundError):
                data = {}

            if key in data:
                del data[key]

            with open(self.filename, 'w') as f:
                json.dump(data, f)

    def get_data(self, key):
        with self.lock:
            try:
                with open(self.filename, 'r') as f:
                    data = json.load(f)
                return data.get(key)
            except (json.JSONDecodeError, FileNotFoundError):
                return None