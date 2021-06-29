from abc import ABCMeta, abstractmethod
from typing import List, Union

from src.domain.entry import Entry, Keyword

U = Union[str, None]


class EntryRepository(metaclass=ABCMeta):

    @abstractmethod
    def get_all_entries(self, url: str) -> List[Entry]:
        raise NotImplementedError

    @abstractmethod
    def get_latest_published_entry(self, url: str) -> Entry:
        raise NotImplementedError
