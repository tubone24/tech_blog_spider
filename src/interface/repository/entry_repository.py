from datetime import datetime
from abc import ABCMeta, abstractmethod
from typing import List

from domain.entry import Entry


class EntryRepository(metaclass=ABCMeta):
    @abstractmethod
    def get_all_entries(self, url: str) -> List[Entry]:
        raise NotImplementedError

    @abstractmethod
    def get_until_last_published_entries(self, url: str, time: datetime) -> List[Entry]:
        raise NotImplementedError

    @abstractmethod
    def get_latest_published_entry(self, url: str) -> Entry:
        raise NotImplementedError
