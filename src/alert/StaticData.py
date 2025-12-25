import os

from utils import JSONFile, Log

log = Log("StaticData")


class StaticData:
    DIR_DATA = "data"
    DIR_DATA_STATIC = os.path.join(DIR_DATA, "static")

    def __init__(self, id):
        self.id = id

    @property
    def json_file_path(self):
        return os.path.join(self.DIR_DATA_STATIC, f"{self.id}.json")

    @property
    def json_file(self):
        return JSONFile(self.json_file_path)

    def read(self):
        return self.json_file.read()

    def write(self, data):
        self.json_file.write(data)
        n = len(data)
        log.info(f"Wrote {n:,} items to {self.json_file}")
