from abc import ABCMeta, abstractmethod
from datetime import datetime


class FeedRepository(metaclass=ABCMeta):
    @abstractmethod
    def get_all_feeds(self):
        raise NotImplementedError

    @abstractmethod
    def get_feed_by_name(self, name: str):
        raise NotImplementedError

    @abstractmethod
    def update_last_published(self, name: str, time: datetime):
        raise NotImplementedError
