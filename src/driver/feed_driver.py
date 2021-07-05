import os
import harperdb
from typing import Dict
from src.interface.driver.feed_driver import FeedDriver

HARPERDB_URL = os.getenv("HARPERDB_URL")
HARPERDB_USERNAME = os.getenv("HARPERDB_USERNAME")
HARPERDB_PASSWORD = os.getenv("HARPERDB_PASSWORD")
HARPERDB_SCHEMA = os.getenv("HARPERDB_SCHEMA", "prd")


class FeedDriverImpl(FeedDriver):
    def __init__(self):
        self.db = harperdb.HarperDB(
            url=HARPERDB_URL,
            username=HARPERDB_USERNAME,
            password=HARPERDB_PASSWORD,)

    def get_feed_by_name(self, name):
        entry_url = self.db.search_by_hash(HARPERDB_SCHEMA, "entry_urls", [name], get_attributes=["url", "icon"])[0]
        time = self.db.search_by_hash(HARPERDB_SCHEMA, "last_published", [name], get_attributes=["time"])[0]["time"]
        return {"name": entry_url["name"], "url": entry_url["url"],
                "icon": entry_url["icon"], "time": time}

    def get_all_feeds(self):
        return [{"name": x["name"],
                 "url": x["url"],
                 "icon": x["icon"],
                 "time": x["time"]} for x in self.db.sql(f"SELECT * FROM {HARPERDB_SCHEMA}.entry_urls"
                                                         f" LEFT JOIN {HARPERDB_SCHEMA}.last_published "
                                                         f"ON entry_urls.name = last_published.name")]

    def update_last_published(self, name: str, time: int) -> Dict[str, int]:
        self.db.update(HARPERDB_SCHEMA, "last_published", [{"name": name, "time": time}])
        return {"name": name, "time": time}
