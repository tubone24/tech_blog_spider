from interface.usecase.feed_usecase import FeedUsecase
from interface.usecase.entry_usecase import EntryUsecase
from util.logger import AppLog

_logger = AppLog(__name__)


class GitHubAction:
    feed_usecase: FeedUsecase
    entry_usecase: EntryUsecase

    def __init__(self, feed_usecase: FeedUsecase, entry_usecase: EntryUsecase):
        self.feed_usecase = feed_usecase
        self.entry_usecase = entry_usecase

    def run(self):
        feeds = self.feed_usecase.get_all_feed()
        for feed in feeds:
            last_published_date = self.entry_usecase.post_unread_entries(feed)
            if feed.last_published_datetime != last_published_date:
                _logger.info(
                    f"Update published date: {feed.name}  {feed.last_published_datetime} => {last_published_date}"
                )
                self.feed_usecase.update_last_published(feed, last_published_date)
