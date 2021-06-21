from datetime import datetime
import math
import re
import os
import json
import requests
import feedparser
import harperdb
import opengraph_py3
import favicon

HARPERDB_URL = os.getenv("HARPERDB_URL")
HARPERDB_USERNAME = os.getenv("HARPERDB_USERNAME")
HARPERDB_PASSWORD = os.getenv("HARPERDB_PASSWORD")
HARPERDB_SCHEMA = os.getenv("HARPERDB_SCHEMA", "prd")
SLACK_WEBHOOK_URL = os.getenv("SLACK_WEBHOOK_URL")


db = harperdb.HarperDB(
    url=HARPERDB_URL,
    username=HARPERDB_USERNAME,
    password=HARPERDB_PASSWORD,)

html_tag = re.compile(r"<[^>]*?>")


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
                "footer_icon": "https://platform.slack-edge.com/img/default_application_icon.png",
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
            ogp = opengraph_py3.OpenGraph(url=entry.link)
            if ogp.is_valid():
                result.append(
                    {"link": entry.link,
                     "title": entry.title,
                     "summary": html_tag.sub("", entry.summary),
                     "published_time": math.floor(published_time.timestamp()),
                     "image": ogp["image"]})
            else:
                result.append(
                    {"link": entry.link,
                     "title": entry.title,
                     "summary": html_tag.sub("", entry.summary),
                     "published_time": math.floor(published_time.timestamp()),
                     "image": "https://i.imgur.com/mfYPqRr.png"})
    sorted_result = sorted(result, key=lambda x: x['published_time'])
    if published_time is None or len(sorted_result) == 0:
        return sorted_result, math.floor(last_indexed_publish_time.timestamp())
    return sorted_result, math.floor(sorted_result[-1]["published_time"])


def main():
    for entry in get_entry_urls():
        try:
            time = get_last_published(entry["name"])
        except EmptyLastPublishedRecordError:
            time = insert_last_published(entry["name"])
        result, new_time = get_entry(entry["url"], time)
        for r in result:
            if entry["icon"] is not None or entry["icon"] == "":
                icon = entry["icon"]
            else:
                icons = favicon.get(entry["url"])
                if len(icons) == 0:
                    icon = ""
                else:
                    icon = icons[0].url
            post_slack(entry["name"], entry["url"], icon, r)
        update_last_published(entry["name"], new_time)


if __name__ == "__main__":
    main()
