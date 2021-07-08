import os
import logging
from logging import config
import yaml

yaml_path = os.path.join(os.path.dirname(__file__), "logging.yaml")

with open(yaml_path) as f:
    dict_config = yaml.load(f, Loader=yaml.FullLoader)

config.dictConfig(dict_config)


class AppLog:

    logger = None

    def __init__(self, name):
        self.logger = logging.getLogger(name)

    def debug(self, msg, *args, **kwargs):
        self.logger.debug(msg, *args, **kwargs)

    def info(self, msg, *args, **kwargs):
        self.logger.info(msg, *args, **kwargs)

    def warn(self, msg, *args, **kwargs):
        self.logger.warning(msg, *args, **kwargs)

    def error(self, msg, *args, **kwargs):
        self.logger.error(msg, *args, **kwargs)

    def exception(self, msg, *args, **kwargs):
        self.logger.exception(msg, *args, **kwargs)

    def critical(self, msg, *args, **kwargs):
        self.logger.critical(msg, *args, **kwargs)


def get_logger(name):
    return AppLog(name)
