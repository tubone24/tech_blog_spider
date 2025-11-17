from datetime import datetime
import pytest
from domain.feed import Feed


class TestFeed:
    @pytest.fixture
    def sample_feed(self):
        return Feed(
            name="Tech Blog",
            url="https://example.com/feed.xml",
            icon="https://example.com/favicon.ico",
            last_published_datetime=datetime(2025, 11, 17, 10, 0, 0),
        )

    def test_feed_creation(self, sample_feed):
        assert sample_feed.name == "Tech Blog"
        assert sample_feed.url == "https://example.com/feed.xml"
        assert sample_feed.icon == "https://example.com/favicon.ico"
        assert sample_feed.last_published_datetime == datetime(2025, 11, 17, 10, 0, 0)

    def test_feed_with_none_icon(self):
        feed = Feed(
            name="Tech Blog",
            url="https://example.com/feed.xml",
            icon=None,
            last_published_datetime=datetime(2025, 11, 17, 10, 0, 0),
        )
        assert feed.icon is None

    def test_feed_mutability(self, sample_feed):
        # Feed is mutable (not frozen)
        new_datetime = datetime(2025, 11, 18, 10, 0, 0)
        sample_feed.last_published_datetime = new_datetime
        assert sample_feed.last_published_datetime == new_datetime

    def test_feed_update_icon(self, sample_feed):
        new_icon = "https://example.com/new-favicon.ico"
        sample_feed.icon = new_icon
        assert sample_feed.icon == new_icon

    def test_feed_equality(self):
        feed1 = Feed(
            name="Tech Blog",
            url="https://example.com/feed.xml",
            icon="https://example.com/favicon.ico",
            last_published_datetime=datetime(2025, 11, 17, 10, 0, 0),
        )
        feed2 = Feed(
            name="Tech Blog",
            url="https://example.com/feed.xml",
            icon="https://example.com/favicon.ico",
            last_published_datetime=datetime(2025, 11, 17, 10, 0, 0),
        )
        assert feed1 == feed2

    def test_feed_inequality(self):
        feed1 = Feed(
            name="Tech Blog 1",
            url="https://example.com/feed1.xml",
            icon="https://example.com/favicon.ico",
            last_published_datetime=datetime(2025, 11, 17, 10, 0, 0),
        )
        feed2 = Feed(
            name="Tech Blog 2",
            url="https://example.com/feed2.xml",
            icon="https://example.com/favicon.ico",
            last_published_datetime=datetime(2025, 11, 17, 10, 0, 0),
        )
        assert feed1 != feed2

    def test_feed_japanese_name(self):
        feed = Feed(
            name="技術ブログ",
            url="https://example.jp/feed.xml",
            icon="https://example.jp/favicon.ico",
            last_published_datetime=datetime(2025, 11, 17, 10, 0, 0),
        )
        assert feed.name == "技術ブログ"
