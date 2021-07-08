import favicon
from urllib3.exceptions import HTTPError
from interface.driver.favicon_driver import FaviconDriver
from util.logger import Logger


class FaviconDriverImpl(FaviconDriver):
    def get_favicon(self, url: str) -> str:
        try:
            icons = favicon.get(url)
        except HTTPError as e:
            Logger.get_logger().warning(
                f"Can not get Entry Favicon at {url} cause by {e}"
            )
            icons = []
        if len(icons) == 0:
            return ""
        else:
            return icons[0].url
