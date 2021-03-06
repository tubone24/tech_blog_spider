import requests
from interface.util.http import Http
from util.logger import AppLog

UA = (
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.47 "
    "Safari/537.36 "
)


_logger = AppLog(__name__)


class HttpImpl(Http):
    def post(self, url: str, body) -> str:
        headers = {"User-Agent": UA}
        res = requests.post(url, data=body, headers=headers)
        res.raise_for_status()
        _logger.debug(res.text)
        return res.text

    def get(self, url: str) -> str:
        headers = {"User-Agent": UA}
        res = requests.get(url, headers=headers)
        res.raise_for_status()
        _logger.debug(res.text)
        return res.text
