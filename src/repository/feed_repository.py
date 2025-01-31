from datetime import datetime, timedelta
import math
from domain.feed import Feed
from interface.repository.feed_repository import FeedRepository
from interface.driver.feed_driver import FeedDriver
from interface.driver.favicon_driver import FaviconDriver
from util.error import EmptyLastPublishedRecordError
from typing import List, Dict
from util.logger import AppLog


_logger = AppLog(__name__)


class FeedRepositoryImpl(FeedRepository):
    feed_driver: FeedDriver
    favicon_driver: FaviconDriver

    def __init__(self, feed_driver: FeedDriver, favicon_driver: FaviconDriver):
        self.feed_driver = feed_driver
        self.favicon_driver = favicon_driver

    def get_feed_by_name(self, name: str):
        res = self.feed_driver.get_feed_by_name(name=name)
        last_published_datetime = datetime.fromtimestamp(res["time"])
        return Feed(
            name=res["name"],
            url=res["url"],
            icon=res["icon"],
            last_published_datetime=last_published_datetime,
        )

    def get_all_feeds(self) -> List[Feed]:
        result = []
        res = self.feed_driver.get_all_feeds()
        for r in res:
            _logger.debug(r)
            try:
                if r["time"] is None or r["time"] == "":
                    raise EmptyLastPublishedRecordError()
                last_published_datetime = datetime.fromtimestamp(r["time"])
            except EmptyLastPublishedRecordError:
                _logger.info(f"new feed record: {r['name']}")
                last_published_datetime = datetime.now() - timedelta(days=30)
            if r["icon"] is None or r["icon"] == "":
                icon = self.favicon_driver.get_favicon(r["url"])
                self.feed_driver.update_feed_icon(name=r["name"], icon=icon)
                result.append(
                    Feed(
                        name=r["name"],
                        url=r["url"],
                        icon=icon,
                        last_published_datetime=last_published_datetime,
                    )
                )
            else:
                result.append(
                    Feed(
                        name=r["name"],
                        url=r["url"],
                        icon=r["icon"],
                        last_published_datetime=last_published_datetime,
                    )
                )
        return result

    def update_last_published(self, name: str, time: datetime) -> Dict[str, int]:
        unixtime = math.floor(time.timestamp())
        return self.feed_driver.update_last_published(name, unixtime)
