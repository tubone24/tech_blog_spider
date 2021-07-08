import urllib.error
from datetime import datetime
from time import sleep
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
from janome.tokenizer import Tokenizer
import nltk
import termextract.janome
import termextract.core
import termextract.english_postagger
from bs4 import BeautifulSoup
import urllib.request
from http.cookiejar import CookieJar
from fasttext import load_model

HARPERDB_URL = os.getenv("HARPERDB_URL")
HARPERDB_USERNAME = os.getenv("HARPERDB_USERNAME")
HARPERDB_PASSWORD = os.getenv("HARPERDB_PASSWORD")
HARPERDB_SCHEMA = os.getenv("HARPERDB_SCHEMA", "prd")
SLACK_WEBHOOK_URL = os.getenv("SLACK_WEBHOOK_URL")
LOGGING_LEVEL = os.getenv("LOGGING_LEVEL", "INFO")
SLEEP_TIME = int(os.getenv("LOGGING_LEVEL", "1"))


db = harperdb.HarperDB(
    url=HARPERDB_URL,
    username=HARPERDB_USERNAME,
    password=HARPERDB_PASSWORD,)

html_tag = re.compile(r"<[^>]*?>")

t = Tokenizer()

fasttext_model = load_model("lid.176.bin")

logger = logging.getLogger(__name__)
logger.setLevel(LOGGING_LEVEL)


class EmptyLastPublishedRecordError(BaseException):
    pass


def predict_language_for_fasttext(text, k=1):
    label, score = fasttext_model.predict(text, k)
    return list(zip([lang.replace("__label__", "") for lang in label], score))


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
    fields = [{"title": x[0], "value": x[1], "short": "true"} for x in result["keywords"]]
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
                "ts": result["published_time"],
                "fields": fields
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
            logger.debug(f"new entry detected {entry.link}")
            text = extract_html_text(entry.link)
            if text == "":
                text = html_tag.sub("", entry.summary)
            # https://github.com/facebookresearch/fastText/issues/1079
            language = predict_language_for_fasttext(text.replace("\n", ""))[0][0]
            logger.debug(language)
            if language == "ja":
                keywords = extract_keyword_japanese(text)
            elif language == "en":
                keywords = extract_keyword_english(text)
            else:
                keywords = []
            try:
                image = get_ogp_image(entry.link)
            except urllib.error.HTTPError as e:
                logger.warning(f"Can not get OGP image: {e}")
                image = "https://i.imgur.com/mfYPqRr.png"
            result.append(
                {"link": entry.link,
                 "title": f"【{language}】{entry.title}",
                 "summary": html_tag.sub("", entry.summary),
                 "published_time": math.floor(published_time.timestamp()),
                 "image": image,
                 "keywords": keywords})
            sleep(SLEEP_TIME)
    sorted_result = sorted(result, key=lambda x: x['published_time'])
    if published_time is None or len(sorted_result) == 0:
        return sorted_result, math.floor(last_indexed_publish_time.timestamp())
    return sorted_result, math.floor(sorted_result[-1]["published_time"])


def extract_keyword_japanese(text):
    tokenize_text = t.tokenize(text)
    frequency = termextract.janome.cmp_noun_dict(tokenize_text)
    lr = termextract.core.score_lr(
        frequency,
        ignore_words=termextract.janome.IGNORE_WORDS,
        lr_mode=1, average_rate=1)
    term_imp = termextract.core.term_importance(frequency, lr)
    score_sorted_term_imp = sorted(term_imp.items(), key=lambda x: x[1], reverse=True)
    logger.debug(f"keywords: {score_sorted_term_imp}")
    return score_sorted_term_imp[:6]


def extract_keyword_english(text):
    tagged_text = nltk.pos_tag(nltk.word_tokenize(text))
    frequency = termextract.english_postagger.cmp_noun_dict(tagged_text)
    lr = termextract.core.score_lr(
        frequency,
        ignore_words=termextract.english_postagger.IGNORE_WORDS,
        lr_mode=1, average_rate=1)
    term_imp = termextract.core.term_importance(frequency, lr)
    score_sorted_term_imp = sorted(term_imp.items(), key=lambda x: x[1], reverse=True)
    logger.debug(f"keywords: {score_sorted_term_imp}")
    return score_sorted_term_imp[:6]


def extract_html_text(url):
    try:
        req = urllib.request.Request(
            url,
            data=None,
            headers={
                "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.36 (KHTML, like Gecko) "
                              "Chrome/35.0.1916.47 Safari/537.36 "
            }
        )
        cj = CookieJar()
        opener = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(cj))
        res = opener.open(req).read()
    except urllib.error.HTTPError as e:
        logger.warning(f"Can not get p tags: {e}")
        return ""
    soup = BeautifulSoup(res, "html.parser")
    p_tag_list = soup.find_all("p")
    return " ".join([p.get_text() for p in p_tag_list])


@retry(wait_exponential_multiplier=1000, wait_exponential_max=4000)
def get_ogp_image(link: str):
    try:
        ogp = opengraph_py3.OpenGraph(url=link)
        if ogp.is_valid():
            return ogp["image"]
        else:
            return ""
    except AttributeError as e:
        logger.warning(f"No Head contents: {e}")
        return ""
    except urllib.error.HTTPError as e:
        if 400 <= e.code < 500:
            # if 4xx Error, can not get OGP with urllib3 because of forbidden for crawler.
            return ""
        else:
            raise e


def get_favicon(link):
    icons = favicon.get(link)
    if len(icons) == 0:
        return ""
    else:
        return icons[0].url


def main():
    for entry in get_entry_urls():
        logger.debug(f"Start Entry: {entry['name']}")
        try:
            time = get_last_published(entry["name"])
        except EmptyLastPublishedRecordError:
            time = insert_last_published(entry["name"])
        try:
            result, new_time = get_entry(entry["url"], time)
        except Exception as e:
            logger.warning(f"Can not get Entry {entry['url']} {e}")
            continue
        for r in result:
            if entry["icon"] is not None or entry["icon"] != "":
                icon = entry["icon"]
            else:
                try:
                    icon = get_favicon(entry["url"])
                except Exception as e:
                    logger.warning(f"Can not get Entry Favicon {entry['url']} {e}")
                    icon = ""
            post_slack(entry["name"], entry["url"], icon, r)
        update_last_published(entry["name"], new_time)


if __name__ == "__main__":
    main()