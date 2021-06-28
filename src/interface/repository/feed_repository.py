from abc import ABCMeta, abstractmethod


class FeedRepository(metaclass=ABCMeta):
    @abstractmethod
    def get_all_feeds(self):
        raise NotImplementedError

    @abstractmethod
    def get_feed_by_name(self, name: str):
        raise NotImplementedError
