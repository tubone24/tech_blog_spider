import os

from controller.github_action import GitHubAction
from interactor.feed_usecase import FeedUsecaseImpl
from interactor.entry_usecase import EntryUsecaseImpl
from repository.feed_repository import FeedRepositoryImpl
from repository.entry_repository import EntryRepositoryImpl
from driver.feed_driver import FeedDriverImpl
from driver.favicon_driver import FaviconDriverImpl
from driver.entry_driver import EntryDriverImpl
from driver.ogp_image_driver import OgpImageDriverImpl
from driver.predict_lang_driver import PredictLangImpl
from driver.keyword_driver import KeywordDriverImpl
from driver.slack_driver import SlackDriverImpl
from output.slack_output import SlackOutputImpl
from util.http import HttpImpl
from util.harperdb import HarperDBImpl
from util.logger import Logger


LOGGING_LEVEL = os.getenv("LOGGING_LEVEL", "INFO")
_logger = Logger(name="TechBlogSpider", level=LOGGING_LEVEL)
HARPERDB_URL = os.getenv("HARPERDB_URL")
HARPERDB_USERNAME = os.getenv("HARPERDB_USERNAME")
HARPERDB_PASSWORD = os.getenv("HARPERDB_PASSWORD")
HARPERDB_SCHEMA = os.getenv("HARPERDB_SCHEMA", "prd")
SLACK_WEBHOOK_URL = os.getenv("SLACK_WEBHOOK_URL")
SLEEP_TIME = float(os.getenv("SLEEP_TIME", "1"))


def main():
    log = _logger.get_logger()
    log.info("aaaaaa")
    GitHubAction(
        feed_usecase=FeedUsecaseImpl(
            feed_repository=FeedRepositoryImpl(
                feed_driver=FeedDriverImpl(
                    db=HarperDBImpl(
                        url=HARPERDB_URL,
                        username=HARPERDB_USERNAME,
                        password=HARPERDB_PASSWORD,
                    ).get_instance(),
                    schema=HARPERDB_SCHEMA,
                ),
                favicon_driver=FaviconDriverImpl(),
            )
        ),
        entry_usecase=EntryUsecaseImpl(
            entry_repository=EntryRepositoryImpl(
                entry_driver=EntryDriverImpl(http=HttpImpl(), sleep_time=SLEEP_TIME),
                keyword_driver=KeywordDriverImpl(),
                predict_lang_driver=PredictLangImpl(),
                ogp_image_driver=OgpImageDriverImpl(),
            ),
            slack_output=SlackOutputImpl(
                slack_driver=SlackDriverImpl(url=SLACK_WEBHOOK_URL)
            ),
        ),
    )


if __name__ == "__main__":
    main()
