from datetime import datetime
from interface.driver.entry_driver import EntryDriver
from interface.util.http import Http
from util.error import NoPublishDateError, NoEntrySummaryError
import feedparser
from bs4 import BeautifulSoup
import re
import requests
from time import sleep
from retrying import retry
from util.logger import AppLog
from typing import Dict, Union, List

U = Union[str, datetime]
_logger = AppLog(__name__)


class EntryDriverImpl(EntryDriver):
    http: Http
    sleep_time: float

    def __init__(self, http: Http, sleep_time: float = 1):
        self.http = http
        self.sleep_time = sleep_time
        self.html_tag = re.compile(r"<[^>]*?>")

    def get_until_last_published_entries(
        self, url: str, time: datetime
    ) -> List[Dict[str, U]]:
        d = feedparser.parse(url)
        result = []
        for entry in d.entries:
            try:
                published_time = self._get_published_time(entry)
            except NoPublishDateError:
                _logger.warn(f"No Published Data: skip {url}")
                continue
            if published_time <= time:
                continue
            html = self._get_html(entry.link)
            text = self._extract_html_p_text(html)
            try:
                summary = self._delete_html_tag(entry.summary)
            except AttributeError:
                _logger.warn(f"NoEntrySummaryError {entry.link}")
                summary = text[:200]
            result.append(
                {
                    "link": entry.link,
                    "title": entry.title,
                    "summary": summary,
                    "published_time": published_time,
                    "text": text,
                    "html": html,
                }
            )
            sleep(self.sleep_time)
        sorted_result = sorted(result, key=lambda x: x["published_time"].timestamp())
        return sorted_result

    # ToDo: Check RSS specification
    def get_latest_published_entry(self, url: str):
        d = feedparser.parse(url)
        if len(d.entries) > 0:
            entry = d.entries[0]
            published_time = self._get_published_time(entry)
            html = self.http.get(entry.link)
            text = self._extract_html_p_text(html)
            return {
                "link": entry.link,
                "title": entry.title,
                "summary": self._delete_html_tag(entry.summary),
                "published_time": published_time,
                "text": text,
            }

    def get_all_entries(self, url: str) -> List[Dict[str, U]]:
        try:
            d = feedparser.parse(url)
        except KeyError as e:
            _logger.error(e)
            return []
        result = []
        for entry in d.entries:
            try:
                published_time = self._get_published_time(entry)
            except NoPublishDateError:
                _logger.warn(f"No Published Data: skip {url}")
                continue
            html = self._get_html(entry.link)
            text = self._extract_html_p_text(html)
            try:
                summary = self._delete_html_tag(entry.summary)
            except AttributeError:
                _logger.warn(f"NoEntrySummaryError {entry.link}")
                summary = text[:200]
            result.append(
                {
                    "link": entry.link,
                    "title": entry.title,
                    "summary": summary,
                    "published_time": published_time,
                    "text": text,
                    "html": html,
                }
            )
            sleep(self.sleep_time)
        sorted_result = sorted(result, key=lambda x: x["published_time"].timestamp())
        return sorted_result

    @staticmethod
    def _get_published_time(entry):
        try:
            if hasattr(entry, "published_parsed"):
                return datetime(*entry.published_parsed[:6])
            elif hasattr(entry, "updated_parsed"):
                return datetime(*entry.updated_parsed[:6])
            else:
                _logger.warn(f"No Published Data: skip {entry.link}")
                raise NoPublishDateError()
        except TypeError as e:
            _logger.debug(e)
            raise NoPublishDateError()
        except NoPublishDateError as e:
            raise NoPublishDateError()

    @staticmethod
    def _extract_html_p_text(html: str) -> str:
        soup = BeautifulSoup(html, "html.parser")
        p_tag_list = soup.find_all("p")
        return " ".join([p.get_text() for p in p_tag_list])

    def _delete_html_tag(self, text: str) -> str:
        return self.html_tag.sub("", text)

    @retry(wait_exponential_multiplier=1000, wait_exponential_max=4000)
    def _get_html(self, link: str):
        _logger.debug(f"Getting HTML from: {link}")
        if link is None or link == "":
            return ""
        try:
            return self.http.get(link)
        except requests.exceptions.RequestException as e:
            if 400 <= e.response.status_code < 500:
                # if 4xx Error, can not get html with requests because of forbidden for crawler.
                _logger.warn(e)
                return ""
            else:
                raise e
        except Exception as e:
            _logger.error(e)
            return ""
