from abc import ABCMeta, abstractmethod
from datetime import datetime
from typing import Dict, List
from domain.feed import Feed


class FeedRepository(metaclass=ABCMeta):
    @abstractmethod
    def get_all_feeds(self) -> List[Feed]:
        raise NotImplementedError

    @abstractmethod
    def get_feed_by_name(self, name: str) -> Feed:
        raise NotImplementedError

    @abstractmethod
    def update_last_published(self, name: str, time: datetime) -> Dict[str, int]:
        raise NotImplementedError
