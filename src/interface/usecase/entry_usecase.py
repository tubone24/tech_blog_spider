from datetime import datetime
from domain.feed import Feed
from abc import ABCMeta, abstractmethod


class EntryUsecase(metaclass=ABCMeta):
    @abstractmethod
    def post_unread_entries(self, feed: Feed) -> datetime:
        raise NotImplementedError
