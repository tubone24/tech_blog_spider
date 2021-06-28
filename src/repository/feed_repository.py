from datetime import datetime
from src.domain.feed import Feed
from src.interface.repository.feed_repository import FeedRepository
from src.driver.feed_driver import FeedDriver


class EntryRepositoryImpl(FeedRepository):
    feed_driver: FeedDriver

    def __init__(self, feed_driver: FeedDriver):
        self.feed_driver = feed_driver

    def get_feed_by_name(self, name: str):
        res = self.feed_driver.get_feed_by_name(name=name)
        last_published_datetime = datetime.fromtimestamp(res["time"])
        return Feed(name=res["name"], url=res["url"], icon=res["icon"], last_published_datetime=last_published_datetime)

    def get_all_feeds(self):
        pass
