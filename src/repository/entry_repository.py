from typing import List

from src.domain.entry import Entry, Keyword
from src.interface.repository.entry_repository import EntryRepository


class EntryRepositoryImpl(EntryRepository):
    def add_entry(self, title: str, url: str, summary: str, image: str, language: str, text: str, published_date: str,
                  keywords: List[Keyword]) -> Entry:
        pass

    def get_latest_published_entry(self) -> Entry:
        pass

    def get_all_entries(self) -> Entries:
        pass

    def create(self, name, url, icon=None):
        return Entries(name, url, icon, [])
