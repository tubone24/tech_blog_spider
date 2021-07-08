from typing import List, Tuple, Dict
from janome.tokenizer import Tokenizer
import nltk
import termextract.janome
import termextract.core
import termextract.english_postagger
from interface.driver.keyword_driver import KeywordDriver


class KeywordDriverImpl(KeywordDriver):
    def __init__(self):
        self.t = Tokenizer()

    def get_keyword_list(self, text: str, lang: str, num: int = 6) -> List[Tuple[str, float]]:
        if lang == "ja":
            term_imp = self._extract_keyword_japanese(text)
        elif lang == "en":
            term_imp = self._extract_keyword_english(text)
        else:
            term_imp = self._extract_keyword_english(text)
        # ToDo: Invalid type
        return sorted(term_imp.items(), key=lambda x: x[1], reverse=True)[:num]

    def _extract_keyword_japanese(self, text: str) -> Dict[str, float]:
        tokenize_text = self.t.tokenize(text)
        frequency = termextract.janome.cmp_noun_dict(tokenize_text)
        lr = termextract.core.score_lr(
            frequency,
            ignore_words=termextract.janome.IGNORE_WORDS,
            lr_mode=1, average_rate=1)
        return termextract.core.term_importance(frequency, lr)

    @staticmethod
    def _extract_keyword_english(text: str) -> Dict[str, float]:
        tagged_text = nltk.pos_tag(nltk.word_tokenize(text))
        frequency = termextract.english_postagger.cmp_noun_dict(tagged_text)
        lr = termextract.core.score_lr(
            frequency,
            ignore_words=termextract.english_postagger.IGNORE_WORDS,
            lr_mode=1, average_rate=1)
        return termextract.core.term_importance(frequency, lr)
