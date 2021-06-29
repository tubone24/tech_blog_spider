from typing import List

from src.domain.entry import Entry, Keyword
from src.interface.repository.entry_repository import EntryRepository
from src.interface.driver.entry_driver import EntryDriver
from src.interface.driver.keyword_driver import KeywordDriver
from src.interface.driver.predict_lang_driver import PredictLang
from src.interface.driver.ogp_image_driver import OgpImageDriver


class EntryRepositoryImpl(EntryRepository):
    entry_driver: EntryDriver
    keyword_driver: KeywordDriver
    predict_lang: PredictLang
    ogp_image: OgpImageDriver

    def get_latest_published_entry(self, url: str) -> Entry:
        pass

    def get_all_entries(self, url: str) -> List[Entry]:
        pass