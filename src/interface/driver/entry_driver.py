from abc import ABCMeta, abstractmethod


class EntryDriver(metaclass=ABCMeta):
    @abstractmethod
    def get_all_entries(self):
        raise NotImplementedError

    @abstractmethod
    def get_latest_published_entry(self, name):
        raise NotImplementedError
