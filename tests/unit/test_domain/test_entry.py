from datetime import datetime
import pytest
from domain.entry import Entry, Keyword


class TestKeyword:
    def test_keyword_creation(self):
        keyword = Keyword(word="python", score=0.95)
        assert keyword.word == "python"
        assert keyword.score == 0.95

    def test_keyword_immutability(self):
        keyword = Keyword(word="python", score=0.95)
        with pytest.raises(AttributeError):
            keyword.word = "java"

    def test_keyword_equality(self):
        keyword1 = Keyword(word="python", score=0.95)
        keyword2 = Keyword(word="python", score=0.95)
        assert keyword1 == keyword2


class TestEntry:
    @pytest.fixture
    def sample_keywords(self):
        return [
            Keyword(word="python", score=0.95),
            Keyword(word="testing", score=0.85),
        ]

    @pytest.fixture
    def sample_entry(self, sample_keywords):
        return Entry(
            title="Test Article",
            url="https://example.com/article",
            summary="This is a test article about Python testing",
            image="https://example.com/image.png",
            language="en",
            text="Full article text goes here...",
            published_date=datetime(2025, 11, 17, 10, 0, 0),
            keywords=sample_keywords,
        )

    def test_entry_creation(self, sample_entry, sample_keywords):
        assert sample_entry.title == "Test Article"
        assert sample_entry.url == "https://example.com/article"
        assert sample_entry.summary == "This is a test article about Python testing"
        assert sample_entry.image == "https://example.com/image.png"
        assert sample_entry.language == "en"
        assert sample_entry.text == "Full article text goes here..."
        assert sample_entry.published_date == datetime(2025, 11, 17, 10, 0, 0)
        assert sample_entry.keywords == sample_keywords

    def test_entry_immutability(self, sample_entry):
        with pytest.raises(AttributeError):
            sample_entry.title = "New Title"

    def test_entry_equality(self, sample_keywords):
        entry1 = Entry(
            title="Test",
            url="https://example.com",
            summary="Summary",
            image="https://example.com/img.png",
            language="en",
            text="Text",
            published_date=datetime(2025, 11, 17, 10, 0, 0),
            keywords=sample_keywords,
        )
        entry2 = Entry(
            title="Test",
            url="https://example.com",
            summary="Summary",
            image="https://example.com/img.png",
            language="en",
            text="Text",
            published_date=datetime(2025, 11, 17, 10, 0, 0),
            keywords=sample_keywords,
        )
        assert entry1 == entry2

    def test_entry_with_empty_keywords(self):
        entry = Entry(
            title="Test",
            url="https://example.com",
            summary="Summary",
            image="",
            language="ja",
            text="テキスト",
            published_date=datetime(2025, 11, 17, 10, 0, 0),
            keywords=[],
        )
        assert entry.keywords == []
        assert entry.language == "ja"

    def test_entry_japanese_content(self):
        entry = Entry(
            title="日本語のタイトル",
            url="https://example.jp/article",
            summary="これは日本語の記事です",
            image="https://example.jp/image.png",
            language="ja",
            text="完全な記事のテキストがここに入ります...",
            published_date=datetime(2025, 11, 17, 10, 0, 0),
            keywords=[Keyword(word="Python", score=0.9)],
        )
        assert entry.title == "日本語のタイトル"
        assert entry.language == "ja"
        assert entry.summary == "これは日本語の記事です"
