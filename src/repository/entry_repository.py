from typing import List

from src.domain.entry import Entry, Keyword
from src.interface.repository.entry_repository import EntryRepository
from src.interface.driver.entry_driver import EntryDriver


class EntryRepositoryImpl(EntryRepository):
    entry_driver: EntryDriver

    def get_latest_published_entry(self) -> Entry:
        pass

    def get_all_entries(self) -> List[Entry]:
        pass
