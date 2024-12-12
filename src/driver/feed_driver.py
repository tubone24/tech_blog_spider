import os
from typing import Dict, List, Union
from pymongo import MongoClient
from interface.driver.feed_driver import FeedDriver
from pymongo.errors import ServerSelectionTimeoutError

U = Union[str, int]


class FeedDriverImpl(FeedDriver):
    def __init__(self, connection_string: str, database: str = "prd"):
        self.client = MongoClient(
            connection_string,
            tls=True,
            authSource="admin",
        )
        self.db = self.client[database]
        self.entry_urls = self.db.entry_urls
        self.last_published = self.db.last_published
        try:
            self.client.admin.command("ping")
        except ServerSelectionTimeoutError:
            print("サーバー選択がタイムアウトしました")
            self.client.close()
            raise ServerSelectionTimeoutError

    def get_feed_by_name(self, name) -> Dict[str, U]:
        entry_url = self.entry_urls.find_one(
            {"name": name}, {"_id": 0, "url": 1, "icon": 1}
        )
        time = self.last_published.find_one({"name": name}, {"_id": 0, "time": 1})
        return {
            "name": name,
            "url": entry_url["url"],
            "icon": entry_url["icon"],
            "time": time["time"] if time else None,
        }

    def get_all_feeds(self) -> List[Dict[str, U]]:
        pipeline = [
            {
                "$lookup": {
                    "from": "last_published",
                    "localField": "name",
                    "foreignField": "name",
                    "as": "last_published",
                }
            },
            {
                "$project": {
                    "_id": 0,
                    "name": 1,
                    "url": 1,
                    "icon": 1,
                    "time": {"$arrayElemAt": ["$last_published.time", 0]},
                }
            },
        ]
        return list(self.entry_urls.aggregate(pipeline))

    def update_last_published(self, name: str, time: int) -> Dict[str, int]:
        self.last_published.update_one(
            {"name": name}, {"$set": {"time": time}}, upsert=True
        )
        return {"name": name, "time": time}

    def update_feed_icon(self, name: str, icon: str) -> Dict[str, str]:
        self.entry_urls.update_one({"name": name}, {"$set": {"icon": icon}})
        return {"name": name, "icon": icon}
