from abc import ABCMeta, abstractmethod
from typing import Dict


class FeedDriver(metaclass=ABCMeta):
    @abstractmethod
    def get_all_feeds(self):
        raise NotImplementedError

    @abstractmethod
    def get_feed_by_name(self, name):
        raise NotImplementedError

    @abstractmethod
    def update_last_published(self, name: str, time: int) -> Dict[str, int]:
        raise NotImplementedError
