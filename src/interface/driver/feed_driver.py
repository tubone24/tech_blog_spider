from abc import ABCMeta, abstractmethod
from typing import Dict, List, Union

U = Union[str, int]


class FeedDriver(metaclass=ABCMeta):
    @abstractmethod
    def get_all_feeds(self) -> List[Dict[str, U]]:
        raise NotImplementedError

    @abstractmethod
    def get_feed_by_name(self, name) -> Dict[str, U]:
        raise NotImplementedError

    @abstractmethod
    def update_last_published(self, name: str, time: int) -> Dict[str, int]:
        raise NotImplementedError

    @abstractmethod
    def update_feed_icon(self, name: str, icon: str) -> Dict[str, str]:
        raise NotImplementedError
