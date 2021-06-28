from abc import ABCMeta, abstractmethod


class FeedDriver(metaclass=ABCMeta):
    @abstractmethod
    def get_all_feeds(self):
        NotImplementedError

    @abstractmethod
    def get_feed_by_name(self, name):
        NotImplementedError
