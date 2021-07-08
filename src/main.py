from src.interface.usecase.feed_usecase import FeedUsecase
from src.interface.usecase.entry_usecase import EntryUsecase
from src.util.logger import Logger


import os

LOGGING_LEVEL = os.getenv("LOGGING_LEVEL", "INFO")
_logger = Logger.get_logger(name="TechBlogSpider", level=LOGGING_LEVEL)


def main():
    feed_usecase = FeedUsecase()
    entry_usecase = EntryUsecase()
    feeds = feed_usecase.get_all_feed()
    for feed in feeds:
        last_published_date = entry_usecase.post_unread_entries(feed)
        feed_usecase.update_last_published(feed, last_published_date)


if __name__ == "__main__":
    main()
