from datetime import datetime
from typing import List, Dict
from interface.repository.feed_repository import FeedRepository
from domain.feed import Feed
from interface.usecase.feed_usecase import FeedUsecase


class FeedUsecaseImpl(FeedUsecase):
    feed_repository: FeedRepository

    def __init__(self):
        self.feed_repository = FeedRepository()

    def update_last_published(self, feed: Feed, time: datetime) -> Dict[str, int]:
        return self.feed_repository.update_last_published(feed.name, time)

    def get_all_feed(self) -> List[Feed]:
        return self.feed_repository.get_all_feeds()
