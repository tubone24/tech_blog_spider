from typing import Dict, Union
from abc import ABCMeta, abstractmethod

U = Union[str, int]


class Http(metaclass=ABCMeta):
    @abstractmethod
    def get(self, url: str) -> str:
        raise NotImplementedError

    @abstractmethod
    def post(self, url: str, body: Dict[str, U]) -> str:
        raise NotImplementedError
