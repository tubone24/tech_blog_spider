import urllib.error
from datetime import datetime
import math
import re
import os
import json
import logging
import requests
import feedparser
import harperdb
import opengraph_py3
import favicon
from retrying import retry

HARPERDB_URL = os.getenv("HARPERDB_URL")
HARPERDB_USERNAME = os.getenv("HARPERDB_USERNAME")
HARPERDB_PASSWORD = os.getenv("HARPERDB_PASSWORD")
HARPERDB_SCHEMA = os.getenv("HARPERDB_SCHEMA", "prd")
SLACK_WEBHOOK_URL = os.getenv("SLACK_WEBHOOK_URL")
LOGGING_LEVEL = os.getenv("LOGGING_LEVEL", "INFO")


db = harperdb.HarperDB(
    url=HARPERDB_URL,
    username=HARPERDB_USERNAME,
    password=HARPERDB_PASSWORD,)

html_tag = re.compile(r"<[^>]*?>")

logger = logging.getLogger(__name__)
logger.setLevel(LOGGING_LEVEL)


class EmptyLastPublishedRecordError(BaseException):
    pass


def get_last_published(name: str):
    try:
        test = db.search_by_hash(HARPERDB_SCHEMA, "last_published", [name], get_attributes=["time"])
        return test[0]["time"]
    except IndexError:
        raise EmptyLastPublishedRecordError()


def insert_last_published(name: str):
    db.insert(HARPERDB_SCHEMA, "last_published", [{"name": name, "time": 123456789}])
    return 123456789


def update_last_published(name: str, time: int):
    result = db.update(HARPERDB_SCHEMA, "last_published", [{"name": name, "time": time}])
    return result


def get_entry_urls():
    return [{"name": x["name"],
             "url": x["url"],
             "icon": x["icon"]} for x in db.sql(f"select * from {HARPERDB_SCHEMA}.entry_urls")]


def post_slack(name, url, icon, result):
    payload = {
        "username": name,
        "attachments": [
            {
                "author_name": name,
                "author_link": url,
                "author_icon": icon,
                "fallback": result["title"],
                "color":"#EEEEEE",
                "title": result["title"],
                "title_link": result["link"],
                "image_url": result["image"],
                "text": result["summary"],
                "footer": "TechBlogSpider",
                "footer_icon": "https://i.imgur.com/6A4px3e.png",
                "ts": result["published_time"]
            }
        ]
    }
    requests.post(SLACK_WEBHOOK_URL, data=json.dumps(payload))


def get_entry(url: str, time: int):
    d = feedparser.parse(url)
    result = []
    published_time = None
    last_indexed_publish_time = datetime.fromtimestamp(time)
    for entry in d.entries:
        if hasattr(entry, "published_parsed"):
            published_time = datetime(*entry.published_parsed[:6])
        elif hasattr(entry, "updated_parsed"):
            published_time = datetime(*entry.updated_parsed[:6])
        td = last_indexed_publish_time - published_time
        if math.floor(td.total_seconds()) < 0:
            try:
                image = get_ogp_image(entry.link)
            except urllib.error.HTTPError:
                image = "https://i.imgur.com/mfYPqRr.png"
            result.append(
                {"link": entry.link,
                 "title": entry.title,
                 "summary": html_tag.sub("", entry.summary),
                 "published_time": math.floor(published_time.timestamp()),
                 "image": image})
    sorted_result = sorted(result, key=lambda x: x['published_time'])
    if published_time is None or len(sorted_result) == 0:
        return sorted_result, math.floor(last_indexed_publish_time.timestamp())
    return sorted_result, math.floor(sorted_result[-1]["published_time"])


# @retry(wait_exponential_multiplier=1000, wait_exponential_max=4000)
def get_ogp_image(link: str):
    try:
        ogp = opengraph_py3.OpenGraph(url=link)
        if ogp.is_valid():
            return ogp["image"]
        else:
            return "https://i.imgur.com/mfYPqRr.png"
    except AttributeError as e:
        return "https://i.imgur.com/mfYPqRr.png"


def get_favicon(link):
    icons = favicon.get(link)
    if len(icons) == 0:
        return ""
    else:
        return icons[0].url


def main():
    for entry in get_entry_urls():
        print(f"Start Entry: {entry['name']}")
        logger.debug(f"Start Entry: {entry['name']}")
        try:
            time = get_last_published(entry["name"])
        except EmptyLastPublishedRecordError:
            time = insert_last_published(entry["name"])
        try:
            result, new_time = get_entry(entry["url"], time)
        except Exception  as e:
            logger.warning(f"Can not get Entry: {entry['url']}: {e}")
            continue
        for r in result:
            if entry["icon"] is not None or entry["icon"] == "":
                icon = entry["icon"]
            else:
                try:
                    icon = get_favicon(entry["url"])
                except Exception as e:
                    logger.warning(f"Can not get Entry Favicon {entry['url']}:   {e}")
                    icon = ""
            post_slack(entry["name"], entry["url"], icon, r)
        update_last_published(entry["name"], new_time)


if __name__ == "__main__":
    main()
