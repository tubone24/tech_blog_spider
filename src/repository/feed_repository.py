from datetime import datetime, timedelta
import math
from src.domain.feed import Feed
from src.interface.repository.feed_repository import FeedRepository
from src.interface.driver.feed_driver import FeedDriver
from src.interface.driver.favicon_driver import FaviconDriver
from src.util.error import EmptyLastPublishedRecordError
from typing import List, Dict
from src.util.logger import Logger


class EntryRepositoryImpl(FeedRepository):

    feed_driver: FeedDriver
    favicon_driver: FaviconDriver

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
            try:
                if r["time"] is None or r["time"] == "":
                    raise EmptyLastPublishedRecordError()
                last_published_datetime = datetime.fromtimestamp(r["time"])
            except EmptyLastPublishedRecordError:
                Logger.get_logger().info(f"new feed record: {r['name']}")
                last_published_datetime = datetime.now() - timedelta(days=30)
            if r["icon"] is not None or r["icon"] != "":
                result.append(Feed(name=r["name"], url=r["url"], icon=r["icon"], last_published_datetime=last_published_datetime))
            else:
                icon = self.favicon_driver.get_favicon(r["url"])
                result.append(Feed(name=r["name"], url=icon, icon=r["icon"], last_published_datetime=last_published_datetime))
        return result

    def update_last_published(self, name: str, time: datetime) -> Dict[str, int]:
        unixtime = math.floor(time.timestamp())
        return self.feed_driver.update_last_published(name, unixtime)
