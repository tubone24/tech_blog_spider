from datetime import datetime
from unittest.mock import Mock, patch
import pytest
from driver.entry_driver import EntryDriverImpl
from util.error import NoPublishDateError


class TestEntryDriverImpl:
    @pytest.fixture
    def mock_http(self):
        return Mock()

    @pytest.fixture
    def entry_driver(self, mock_http):
        return EntryDriverImpl(mock_http, sleep_time=0)

    def test_delete_html_tag(self, entry_driver):
        # Test HTML tag removal
        text_with_tags = "<p>Hello <strong>World</strong></p>"
        result = entry_driver._delete_html_tag(text_with_tags)
        assert result == "Hello World"

    def test_delete_html_tag_with_complex_html(self, entry_driver):
        text = '<div class="content"><p>Test</p><span>Content</span></div>'
        result = entry_driver._delete_html_tag(text)
        assert result == "TestContent"

    def test_extract_html_p_text(self, entry_driver):
        html = "<html><body><p>First paragraph</p><p>Second paragraph</p></body></html>"
        result = entry_driver._extract_html_p_text(html)
        assert result == "First paragraph Second paragraph"

    def test_extract_html_p_text_no_p_tags(self, entry_driver):
        html = "<html><body><div>No paragraph tags</div></body></html>"
        result = entry_driver._extract_html_p_text(html)
        assert result == ""

    def test_get_published_time_with_published_parsed(self, entry_driver):
        # Mock entry with published_parsed
        entry = Mock()
        entry.published_parsed = (2025, 11, 17, 10, 0, 0, 0, 0, 0)
        entry.link = "https://example.com"

        result = entry_driver._get_published_time(entry)
        assert result == datetime(2025, 11, 17, 10, 0, 0)

    def test_get_published_time_with_updated_parsed(self, entry_driver):
        # Mock entry with updated_parsed (fallback)
        entry = Mock()
        entry.published_parsed = None
        del entry.published_parsed  # Simulate attribute not existing
        entry.updated_parsed = (2025, 11, 17, 11, 0, 0, 0, 0, 0)
        entry.link = "https://example.com"

        result = entry_driver._get_published_time(entry)
        assert result == datetime(2025, 11, 17, 11, 0, 0)

    def test_get_published_time_no_date_raises_error(self, entry_driver):
        # Mock entry without any date
        entry = Mock()
        del entry.published_parsed
        del entry.updated_parsed
        entry.link = "https://example.com"

        with pytest.raises(NoPublishDateError):
            entry_driver._get_published_time(entry)

    def test_get_published_time_with_none_value_raises_error(self, entry_driver):
        # Mock entry with None value (causes TypeError)
        entry = Mock()
        entry.published_parsed = None
        entry.link = "https://example.com"

        with pytest.raises(NoPublishDateError):
            entry_driver._get_published_time(entry)

    def test_get_html_with_valid_link(self, entry_driver, mock_http):
        mock_http.get.return_value = "<html><body>Test</body></html>"

        result = entry_driver._get_html("https://example.com")

        assert result == "<html><body>Test</body></html>"
        mock_http.get.assert_called_once_with("https://example.com")

    def test_get_html_with_empty_link(self, entry_driver, mock_http):
        result = entry_driver._get_html("")
        assert result == ""
        mock_http.get.assert_not_called()

    def test_get_html_with_none_link(self, entry_driver, mock_http):
        result = entry_driver._get_html(None)
        assert result == ""
        mock_http.get.assert_not_called()

    @patch("driver.entry_driver.feedparser")
    def test_get_until_last_published_entries(
        self, mock_feedparser, entry_driver, mock_http
    ):
        # Setup mock feed data
        mock_entry = Mock()
        mock_entry.link = "https://example.com/article"
        mock_entry.title = "Test Article"
        mock_entry.summary = "<p>Test Summary</p>"
        mock_entry.published_parsed = (2025, 11, 17, 12, 0, 0, 0, 0, 0)

        mock_feed = Mock()
        mock_feed.entries = [mock_entry]
        mock_feedparser.parse.return_value = mock_feed

        mock_http.get.return_value = "<html><body><p>Article content</p></body></html>"

        # Execute
        result = entry_driver.get_until_last_published_entries(
            "https://example.com/feed.xml", datetime(2025, 11, 17, 10, 0, 0)
        )

        # Assert
        assert len(result) == 1
        assert result[0]["title"] == "Test Article"
        assert result[0]["link"] == "https://example.com/article"
        assert result[0]["summary"] == "Test Summary"
        assert result[0]["text"] == "Article content"

    @patch("driver.entry_driver.feedparser")
    def test_get_until_last_published_entries_filters_old_entries(
        self, mock_feedparser, entry_driver, mock_http
    ):
        # Setup mock with old entry
        mock_entry = Mock()
        mock_entry.link = "https://example.com/old"
        mock_entry.title = "Old Article"
        mock_entry.summary = "Old Summary"
        mock_entry.published_parsed = (2025, 11, 17, 9, 0, 0, 0, 0, 0)  # Older

        mock_feed = Mock()
        mock_feed.entries = [mock_entry]
        mock_feedparser.parse.return_value = mock_feed

        # Execute
        result = entry_driver.get_until_last_published_entries(
            "https://example.com/feed.xml", datetime(2025, 11, 17, 10, 0, 0)
        )

        # Assert - should be filtered out
        assert len(result) == 0

    @patch("driver.entry_driver.feedparser")
    def test_get_until_last_published_entries_handles_no_summary(
        self, mock_feedparser, entry_driver, mock_http
    ):
        # Setup mock without summary
        mock_entry = Mock()
        mock_entry.link = "https://example.com/article"
        mock_entry.title = "Test Article"
        del mock_entry.summary  # No summary attribute
        mock_entry.published_parsed = (2025, 11, 17, 12, 0, 0, 0, 0, 0)

        mock_feed = Mock()
        mock_feed.entries = [mock_entry]
        mock_feedparser.parse.return_value = mock_feed

        mock_http.get.return_value = "<html><body><p>This is a long article content that should be truncated</p></body></html>"

        # Execute
        result = entry_driver.get_until_last_published_entries(
            "https://example.com/feed.xml", datetime(2025, 11, 17, 10, 0, 0)
        )

        # Assert - should use first 200 chars of text as summary
        assert len(result) == 1
        assert len(result[0]["summary"]) <= 200

    @patch("driver.entry_driver.feedparser")
    def test_get_all_entries(self, mock_feedparser, entry_driver, mock_http):
        # Setup
        mock_entry = Mock()
        mock_entry.link = "https://example.com/article"
        mock_entry.title = "Test Article"
        mock_entry.summary = "Summary"
        mock_entry.published_parsed = (2025, 11, 17, 12, 0, 0, 0, 0, 0)

        mock_feed = Mock()
        mock_feed.entries = [mock_entry]
        mock_feedparser.parse.return_value = mock_feed

        mock_http.get.return_value = "<html><body><p>Content</p></body></html>"

        # Execute
        result = entry_driver.get_all_entries("https://example.com/feed.xml")

        # Assert
        assert len(result) == 1
        assert result[0]["title"] == "Test Article"

    @patch("driver.entry_driver.feedparser")
    def test_get_all_entries_handles_key_error(
        self, mock_feedparser, entry_driver, mock_http
    ):
        # Setup to raise KeyError
        mock_feedparser.parse.side_effect = KeyError("Test error")

        # Execute
        result = entry_driver.get_all_entries("https://example.com/feed.xml")

        # Assert - should return empty list
        assert result == []

    @patch("driver.entry_driver.feedparser")
    def test_get_until_last_published_entries_sorts_by_published_time(
        self, mock_feedparser, entry_driver, mock_http
    ):
        # Setup mock with multiple entries in random order
        mock_entry1 = Mock()
        mock_entry1.link = "https://example.com/1"
        mock_entry1.title = "Article 1"
        mock_entry1.summary = "Summary 1"
        mock_entry1.published_parsed = (2025, 11, 17, 12, 0, 0, 0, 0, 0)

        mock_entry2 = Mock()
        mock_entry2.link = "https://example.com/2"
        mock_entry2.title = "Article 2"
        mock_entry2.summary = "Summary 2"
        mock_entry2.published_parsed = (2025, 11, 17, 11, 0, 0, 0, 0, 0)

        mock_feed = Mock()
        mock_feed.entries = [mock_entry1, mock_entry2]  # Newer first
        mock_feedparser.parse.return_value = mock_feed

        mock_http.get.return_value = "<html><body><p>Content</p></body></html>"

        # Execute
        result = entry_driver.get_until_last_published_entries(
            "https://example.com/feed.xml", datetime(2025, 11, 17, 10, 0, 0)
        )

        # Assert - should be sorted with older first
        assert len(result) == 2
        assert result[0]["title"] == "Article 2"  # Older (11:00)
        assert result[1]["title"] == "Article 1"  # Newer (12:00)
