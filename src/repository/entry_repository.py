from typing import List
from domain.entry import Entry, Keyword
from interface.repository.entry_repository import EntryRepository
from interface.driver.entry_driver import EntryDriver
from interface.driver.keyword_driver import KeywordDriver
from interface.driver.predict_lang_driver import PredictLangDriver
from interface.driver.ogp_image_driver import OgpImageDriver


class EntryRepositoryImpl(EntryRepository):
    entry_driver: EntryDriver
    keyword_driver: KeywordDriver
    predict_lang_driver: PredictLangDriver
    ogp_image_driver: OgpImageDriver

    def __init__(self, entry_driver: EntryDriver, keyword_driver: KeywordDriver, predict_lang_driver: PredictLangDriver, ogp_image_driver: OgpImageDriver):
        self.entry_driver = entry_driver
        self.keyword_driver = keyword_driver
        self.predict_lang_driver = predict_lang_driver
        self.ogp_image_driver = ogp_image_driver

    def get_latest_published_entry(self, url: str) -> Entry:
        pass

    def get_all_entries(self, url: str) -> List[Entry]:
        entries = self.entry_driver.get_all_entries(url)
        result = []
        for entry in entries:
            language = self.predict_lang_driver.predict(text=entry.text, k=1)[0][0]
            keywords = [Keyword(word=x[0], score=x[1]) for x in self.keyword_driver.get_keyword_list(entry.text, language)]
            result.append(Entry(title=entry.title, url=entry.url, summary=entry.summary, image=entry.image, language=language, text=entry.text, published_date=entry.published_date, keywords=keywords))
        return result
