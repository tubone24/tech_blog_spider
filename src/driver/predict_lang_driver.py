from fasttext import load_model
from src.interface.driver.predict_lang_driver import PredictLang

fasttext_model = load_model("lid.176.bin")


class PredictLangImpl(PredictLang):
    def predict(self, text: str, k: int):
        label, score = fasttext_model.predict(text, k)
        return list(zip([lang.replace("__label__", "") for lang in label], score))
