import math
from datetime import datetime
from domain.feed import Feed
from interface.usecase.entry_usecase import EntryUsecase
from interface.repository.entry_repository import EntryRepository
from interface.output.slack_output import SlackOutput
from util.logger import Logger


class EntryUsecaseImpl(EntryUsecase):
    entry_repository: EntryRepository
    slack_output: SlackOutput

    def __init__(self, entry_repository: EntryRepository, slack_output: SlackOutput):
        self.entry_repository = entry_repository
        self.slack_output = slack_output

    def post_unread_entries(self, feed: Feed) -> datetime:
        entries = self.entry_repository.get_all_entries(feed.url)
        for entry in entries:
            td = feed.last_published_datetime - entry.published_date
            if math.floor(td.total_seconds()) < 0:
                self.slack_output.post_slack(
                    feed_name=feed.name,
                    feed_url=feed.url,
                    feed_icon=feed.icon,
                    entry=entry,
                )
        if len(entries) == 0:
            return feed.last_published_datetime
        Logger.get_logger().info(
            f"Update published date: {feed.name}  {entries[-1].published_date}"
        )
        return entries[-1].published_date
