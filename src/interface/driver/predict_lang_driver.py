from typing import List, Union
from abc import ABCMeta, abstractmethod

U = Union[str, float]


class PredictLang(metaclass=ABCMeta):
    @abstractmethod
    def predict(self, text: str, k: int) -> List[List[U]]:
        raise NotImplementedError
