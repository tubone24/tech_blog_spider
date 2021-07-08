from abc import ABCMeta, abstractmethod


class FaviconDriver(metaclass=ABCMeta):
    @abstractmethod
    def get_favicon(self, url: str) -> str:
        raise NotImplementedError
