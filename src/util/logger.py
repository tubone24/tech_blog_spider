import logging
from util.error import DeclarationDuplicateInstanceError


class Logger:
    __instance = None

    def __init__(self, name: str, level: str):
        if Logger.__instance is not None:
            raise DeclarationDuplicateInstanceError()
        else:
            Logger.__instance = self
            logger = logging.getLogger(name)
            logger.setLevel(level)
            self.logger = logger

    @classmethod
    def get_logger(cls, name="TechBlogSpider", level="INFO"):
        if cls.__instance is None:
            cls(name, level)
        return cls.__instance
