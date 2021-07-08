from typing import List
import math
from src.domain.entry import Entry
from src.interface.output.slack_output import SlackOutput
from src.interface.driver.slack_driver import SlackDriver
from src.output.slack_output_data import SlackOutputData, SlackAttachment, SlackField


FOOTER_TEXT = "TechBlogSpider"
FOOTER_ICON = "https://i.imgur.com/6A4px3e.png"


class SlackOutputImpl(SlackOutput):
    slack_driver: SlackDriver

    def __init__(self):
        self.slack_driver = SlackDriver()

    def post_slack(self, feed_name: str, feed_url: str, feed_icon: str, entry: Entry):
        entry_ts = math.floor(entry.published_date.timestamp())
        fields = [SlackField(title=x.word, value=str(x.score), short="true") for x in entry.keywords]
        attachments = SlackAttachment(author_name=feed_name,
                                      author_link=feed_url,
                                      author_icon=feed_icon,
                                      fallback=entry.title,
                                      color="#EEEEEE",
                                      title=f"【{entry.language}】{entry.title}",
                                      title_link=entry.url,
                                      image_url=entry.image,
                                      text=entry.summary,
                                      footer=FOOTER_TEXT,
                                      footer_icon=FOOTER_ICON,
                                      ts=entry_ts,
                                      fields=fields)
        slack_output = SlackOutputData(username=feed_name, attachments=[attachments])
        self.slack_driver.post(slack_output)
