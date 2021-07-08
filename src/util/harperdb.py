from interface.util.harperdb import HarperDB
from harperdb import HarperDB as Hdb


class HarperDBImpl(HarperDB):
    def __init__(self, url: str, username: str, password: str):
        self.db = Hdb(url=url, username=username, password=password)

    def get_instance(self):
        return self.db
