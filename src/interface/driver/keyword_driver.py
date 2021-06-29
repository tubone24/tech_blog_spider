from abc import ABCMeta, abstractmethod


class KeywordDriver(metaclass=ABCMeta):
    @abstractmethod
    def get_keyword_list(self, text: str, lang: str, num: int = 6):
        raise NotImplementedError
