from datetime import datetime
from typing import List, Dict
from src.interface.repository.feed_repository import FeedRepository
from domain.feed import Feed
from src.interface.usecase.feed_usecase import FeedUsecase


class FeedUsecaseImpl(FeedUsecase):
    feed_repository: FeedRepository

    def __init__(self):
        self.feed_repository = FeedRepository()

    def update_last_published(self, name: str, time: datetime) -> Dict[str, int]:
        return self.feed_repository.update_last_published(name, time)

    def get_all_feed(self) -> List[Feed]:
        return self.feed_repository.get_all_feeds()
