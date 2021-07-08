from abc import ABCMeta, abstractmethod
from harperdb import HarperDB


class HarperDB(metaclass=ABCMeta):
    @abstractmethod
    def get_instance(self) -> HarperDB:
        raise NotImplementedError
