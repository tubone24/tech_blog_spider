from abc import ABCMeta, abstractmethod
from typing import List, Dict, Union
from datetime import datetime

U = Union[str, datetime]


class EntryDriver(metaclass=ABCMeta):
    @abstractmethod
    def get_all_entries(self, url: str) -> List[Dict[str, U]]:
        raise NotImplementedError

    @abstractmethod
    def get_latest_published_entry(self, url: str):
        raise NotImplementedError
