import logging
from util.error import DeclarationDuplicateInstanceError


class Logger:
    __logger = None

    def __init__(self, name: str, level: str):
        if Logger.__logger is not None:
            raise DeclarationDuplicateInstanceError()
        else:

            logger = logging.getLogger(name)
            logger.setLevel(level)
            Logger.__logger = logger

    @classmethod
    def get_logger(cls, name="TechBlogSpider", level="INFO"):
        if cls.__logger is None:
            cls(name, level)
        return cls.__logger
