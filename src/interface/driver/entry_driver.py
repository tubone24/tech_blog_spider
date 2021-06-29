from abc import ABCMeta, abstractmethod


class EntryDriver(metaclass=ABCMeta):
    @abstractmethod
    def get_all_entries(self, url: str):
        raise NotImplementedError

    @abstractmethod
    def get_latest_published_entry(self, url: str):
        raise NotImplementedError
