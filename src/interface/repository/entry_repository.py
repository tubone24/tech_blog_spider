from abc import ABCMeta, abstractmethod
from typing import List, Union

from src.domain.entry import Entry, Keyword

U = Union[str, None]


class EntryRepository(metaclass=ABCMeta):
    @abstractmethod
    def create(self, name: str, url: str, icon: U = None):
        raise NotImplementedError

    @abstractmethod
    def get_all_entries(self) -> Entries:
        raise NotImplementedError

    @abstractmethod
    def get_latest_published_entry(self) -> Entry:
        raise NotImplementedError

    @abstractmethod
    def add_entry(self, title: str, url: str, summary: str, image: str, language: str, text: str, published_date: str,
                  keywords: List[Keyword]) -> Entry:
        raise NotImplementedError
