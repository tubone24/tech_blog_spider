import os
import harperdb
from typing import Dict, List, Union
from interface.driver.feed_driver import FeedDriver

U = Union[str, int]


class FeedDriverImpl(FeedDriver):
    def __init__(self, db: harperdb.HarperDB, schema: str = "prd"):
        self.db = db
        self.schema = schema

    def get_feed_by_name(self, name) -> Dict[str, U]:
        entry_url = self.db.search_by_hash(
            self.schema, "entry_urls", [name], get_attributes=["url", "icon"]
        )[0]
        time = self.db.search_by_hash(
            self.schema, "last_published", [name], get_attributes=["time"]
        )[0]["time"]
        return {
            "name": entry_url["name"],
            "url": entry_url["url"],
            "icon": entry_url["icon"],
            "time": time,
        }

    def get_all_feeds(self) -> List[Dict[str, U]]:
        return [
            {"name": x["name"], "url": x["url"], "icon": x["icon"], "time": x["time"]}
            for x in self.db.sql(
                f"SELECT * FROM {self.schema}.entry_urls"
                f" LEFT JOIN {self.schema}.last_published "
                f"ON entry_urls.name = last_published.name"
            )
        ]

    def update_last_published(self, name: str, time: int) -> Dict[str, int]:
        try:
            self.db.search_by_hash(
                self.schema, "last_published", [name], get_attributes=["time"]
            )
        except IndexError:
            self.db.insert(
                self.schema, "last_published", [{"name": name, "time": time}]
            )
        self.db.update(self.schema, "last_published", [{"name": name, "time": time}])
        return {"name": name, "time": time}
