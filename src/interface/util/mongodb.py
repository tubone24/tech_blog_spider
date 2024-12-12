from abc import ABC, abstractmethod
from pymongo import MongoClient


class MongoDB(ABC):
    @abstractmethod
    def __init__(self, connection_string: str):
        pass

    @abstractmethod
    def get_instance(self) -> MongoClient:
        pass
