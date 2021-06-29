from abc import ABCMeta, abstractmethod


class OgpImageDriver(metaclass=ABCMeta):
    @abstractmethod
    def get(self, html: str) -> str:
        raise NotImplementedError
