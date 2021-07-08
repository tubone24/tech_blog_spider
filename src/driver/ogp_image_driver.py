from bs4 import BeautifulSoup
from interface.driver.ogp_image_driver import OgpImageDriver


class OgpImageDriverImpl(OgpImageDriver):
    def get(self, html: str) -> str:
        soup = BeautifulSoup(html, "html.parser")
        ogp_img = soup.find("meta", attrs={"property": "og:image", "content": True})
        if ogp_img is not None:
            return ogp_img["content"]
        else:
            return ""
