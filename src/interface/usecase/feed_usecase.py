from abc import ABCMeta, abstractmethod
from datetime import datetime
from typing import List, Dict
from src.domain.feed import Feed


class FeedUsecase(metaclass=ABCMeta):
    @abstractmethod
    def get_all_feed(self) -> List[Feed]:
        raise NotImplementedError

    @abstractmethod
    def update_last_published(self, name: str, time: datetime) -> Dict[str, int]:
        raise NotImplementedError
