from datetime import datetime
from src.interface.driver.entry_driver import EntryDriver
import feedparser


class EntryDriverImpl(EntryDriver):
    def get_latest_published_entry(self, url: str):
        d = feedparser.parse(url)
        for entry in d.entries:
            published_time = self._get_published_time(entry)

    def get_all_entries(self, url: str):
        pass

    @staticmethod
    def _get_published_time(entry):
        if hasattr(entry, "published_parsed"):
            return datetime(*entry.published_parsed[:6])
        elif hasattr(entry, "updated_parsed"):
            return datetime(*entry.updated_parsed[:6])
