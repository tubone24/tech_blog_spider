from datetime import datetime
from unittest.mock import Mock
import pytest
from repository.entry_repository import EntryRepositoryImpl


class TestEntryRepositoryImpl:
    @pytest.fixture
    def mock_entry_driver(self):
        return Mock()

    @pytest.fixture
    def mock_keyword_driver(self):
        return Mock()

    @pytest.fixture
    def mock_predict_lang_driver(self):
        return Mock()

    @pytest.fixture
    def mock_ogp_image_driver(self):
        return Mock()

    @pytest.fixture
    def entry_repository(
        self,
        mock_entry_driver,
        mock_keyword_driver,
        mock_predict_lang_driver,
        mock_ogp_image_driver,
    ):
        return EntryRepositoryImpl(
            mock_entry_driver,
            mock_keyword_driver,
            mock_predict_lang_driver,
            mock_ogp_image_driver,
        )

    @pytest.fixture
    def sample_entry_data(self):
        return {
            "title": "Test Article",
            "link": "https://example.com/article",
            "summary": "Test summary",
            "published_time": datetime(2025, 11, 17, 10, 0, 0),
            "text": "This is test article text",
            "html": "<html><body><p>Test</p></body></html>",
        }

    def test_get_until_last_published_entries_with_english_entry(
        self,
        entry_repository,
        mock_entry_driver,
        mock_keyword_driver,
        mock_predict_lang_driver,
        mock_ogp_image_driver,
        sample_entry_data,
    ):
        # Setup
        mock_entry_driver.get_until_last_published_entries.return_value = [
            sample_entry_data
        ]
        mock_predict_lang_driver.predict.return_value = [["en", 0.95]]
        mock_keyword_driver.get_keyword_list.return_value = [
            ("python", 0.9),
            ("testing", 0.85),
        ]
        mock_ogp_image_driver.get.return_value = "https://example.com/image.png"

        # Execute
        result = entry_repository.get_until_last_published_entries(
            "https://example.com/feed.xml", datetime(2025, 11, 17, 9, 0, 0)
        )

        # Assert
        assert len(result) == 1
        entry = result[0]
        assert entry.title == "Test Article"
        assert entry.url == "https://example.com/article"
        assert entry.summary == "Test summary"
        assert entry.language == "en"
        assert entry.image == "https://example.com/image.png"
        assert len(entry.keywords) == 2
        assert entry.keywords[0].word == "python"
        assert entry.keywords[0].score == 0.9

        # Verify driver calls
        mock_entry_driver.get_until_last_published_entries.assert_called_once()
        mock_predict_lang_driver.predict.assert_called_once_with(
            text="This is test article text", k=1
        )
        mock_keyword_driver.get_keyword_list.assert_called_once_with(
            "This is test article text", "en"
        )
        mock_ogp_image_driver.get.assert_called_once()

    def test_get_until_last_published_entries_with_japanese_entry(
        self,
        entry_repository,
        mock_entry_driver,
        mock_keyword_driver,
        mock_predict_lang_driver,
        mock_ogp_image_driver,
    ):
        # Setup
        japanese_entry = {
            "title": "日本語記事",
            "link": "https://example.jp/article",
            "summary": "テストサマリー",
            "published_time": datetime(2025, 11, 17, 10, 0, 0),
            "text": "これは日本語のテキストです",
            "html": "<html><body><p>テスト</p></body></html>",
        }
        mock_entry_driver.get_until_last_published_entries.return_value = [
            japanese_entry
        ]
        mock_predict_lang_driver.predict.return_value = [["ja", 0.98]]
        mock_keyword_driver.get_keyword_list.return_value = [("Python", 0.9)]
        mock_ogp_image_driver.get.return_value = "https://example.jp/image.png"

        # Execute
        result = entry_repository.get_until_last_published_entries(
            "https://example.jp/feed.xml", datetime(2025, 11, 17, 9, 0, 0)
        )

        # Assert
        assert len(result) == 1
        entry = result[0]
        assert entry.title == "日本語記事"
        assert entry.language == "ja"
        assert len(entry.keywords) == 1

    def test_get_until_last_published_entries_filters_unsupported_language(
        self,
        entry_repository,
        mock_entry_driver,
        mock_keyword_driver,
        mock_predict_lang_driver,
        mock_ogp_image_driver,
        sample_entry_data,
    ):
        # Setup - language is French (not supported)
        mock_entry_driver.get_until_last_published_entries.return_value = [
            sample_entry_data
        ]
        mock_predict_lang_driver.predict.return_value = [["fr", 0.95]]

        # Execute
        result = entry_repository.get_until_last_published_entries(
            "https://example.com/feed.xml", datetime(2025, 11, 17, 9, 0, 0)
        )

        # Assert - entry should be filtered out
        assert len(result) == 0
        # Keyword and OGP drivers should not be called
        mock_keyword_driver.get_keyword_list.assert_not_called()
        mock_ogp_image_driver.get.assert_not_called()

    def test_get_until_last_published_entries_with_multiple_entries(
        self,
        entry_repository,
        mock_entry_driver,
        mock_keyword_driver,
        mock_predict_lang_driver,
        mock_ogp_image_driver,
    ):
        # Setup
        entries = [
            {
                "title": "Article 1",
                "link": "https://example.com/1",
                "summary": "Summary 1",
                "published_time": datetime(2025, 11, 17, 10, 0, 0),
                "text": "English text",
                "html": "<html></html>",
            },
            {
                "title": "Article 2",
                "link": "https://example.com/2",
                "summary": "Summary 2",
                "published_time": datetime(2025, 11, 17, 11, 0, 0),
                "text": "日本語テキスト",
                "html": "<html></html>",
            },
        ]
        mock_entry_driver.get_until_last_published_entries.return_value = entries
        mock_predict_lang_driver.predict.side_effect = [[["en", 0.95]], [["ja", 0.98]]]
        mock_keyword_driver.get_keyword_list.side_effect = [
            [("keyword1", 0.9)],
            [("キーワード", 0.85)],
        ]
        mock_ogp_image_driver.get.side_effect = [
            "https://example.com/img1.png",
            "https://example.com/img2.png",
        ]

        # Execute
        result = entry_repository.get_until_last_published_entries(
            "https://example.com/feed.xml", datetime(2025, 11, 17, 9, 0, 0)
        )

        # Assert
        assert len(result) == 2
        assert result[0].title == "Article 1"
        assert result[0].language == "en"
        assert result[1].title == "Article 2"
        assert result[1].language == "ja"

    def test_get_all_entries(
        self,
        entry_repository,
        mock_entry_driver,
        mock_keyword_driver,
        mock_predict_lang_driver,
        mock_ogp_image_driver,
        sample_entry_data,
    ):
        # Setup
        mock_entry_driver.get_all_entries.return_value = [sample_entry_data]
        mock_predict_lang_driver.predict.return_value = [["en", 0.95]]
        mock_keyword_driver.get_keyword_list.return_value = [("test", 0.8)]
        mock_ogp_image_driver.get.return_value = "https://example.com/image.png"

        # Execute
        result = entry_repository.get_all_entries("https://example.com/feed.xml")

        # Assert
        assert len(result) == 1
        assert result[0].title == "Test Article"
        mock_entry_driver.get_all_entries.assert_called_once_with(
            "https://example.com/feed.xml"
        )

    def test_get_all_entries_no_language_filter(
        self,
        entry_repository,
        mock_entry_driver,
        mock_keyword_driver,
        mock_predict_lang_driver,
        mock_ogp_image_driver,
        sample_entry_data,
    ):
        # Setup - even unsupported languages are included in get_all_entries
        mock_entry_driver.get_all_entries.return_value = [sample_entry_data]
        mock_predict_lang_driver.predict.return_value = [["fr", 0.95]]
        mock_keyword_driver.get_keyword_list.return_value = []
        mock_ogp_image_driver.get.return_value = ""

        # Execute
        result = entry_repository.get_all_entries("https://example.com/feed.xml")

        # Assert - all entries returned regardless of language
        assert len(result) == 1
        assert result[0].language == "fr"
