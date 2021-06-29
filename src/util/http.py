import requests
from src.interface.util.http import Http

UA = "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.0.1916.47 " \
     "Safari/537.36 "


class HttpImpl(Http):
    def post(self, url: str, body) -> str:
        headers = {"User-Agent": UA}
        res = requests.post(url, data=body, headers=headers)
        return res.text

    def get(self, url: str) -> str:
        headers = {"User-Agent": UA}
        res = requests.get(url, headers=headers)
        return res.text
