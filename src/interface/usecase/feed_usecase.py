from abc import ABCMeta, abstractmethod

from src.domain.feed import Feed


class FeedUsecase(metaclass=ABCMeta):
    @abstractmethod
    async def get_list(self, page: int) -> Articles:
        raise NotImplementedError
