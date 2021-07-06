from datetime import datetime
import math
from src.domain.feed import Feed
from src.interface.repository.feed_repository import FeedRepository
from src.interface.driver.feed_driver import FeedDriver
from typing import List


class EntryRepositoryImpl(FeedRepository):

    feed_driver: FeedDriver

    def __init__(self, feed_driver: FeedDriver):
        self.feed_driver = feed_driver

    def get_feed_by_name(self, name: str):
        res = self.feed_driver.get_feed_by_name(name=name)
        last_published_datetime = datetime.fromtimestamp(res["time"])
        return Feed(name=res["name"], url=res["url"], icon=res["icon"], last_published_datetime=last_published_datetime)

    def get_all_feeds(self) -> List[Feed]:
        result = []
        res = self.feed_driver.get_all_feeds()
        for r in res:
            last_published_datetime = datetime.fromtimestamp(r["time"])
            result.append(Feed(name=r["name"], url=r["url"], icon=r["icon"], last_published_datetime=last_published_datetime))
        return result

    def update_last_published(self, name: str, time: datetime):
        unixtime = math.floor(time.timestamp())
        return self.feed_driver.update_last_published(name, unixtime)
