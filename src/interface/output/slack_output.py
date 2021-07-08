from abc import ABCMeta, abstractmethod
from domain.entry import Entry


class SlackOutput(metaclass=ABCMeta):
    @abstractmethod
    def post_slack(self, feed_name: str, feed_url: str, feed_icon: str, entry: Entry):
        raise NotImplementedError
