from interface.usecase.feed_usecase import FeedUsecase
from interface.usecase.entry_usecase import EntryUsecase


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
            self.feed_usecase.update_last_published(feed, last_published_date)
