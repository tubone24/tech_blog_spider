from datetime import datetime, timedelta
from unittest.mock import Mock
import pytest
from repository.feed_repository import FeedRepositoryImpl
from util.error import EmptyLastPublishedRecordError


class TestFeedRepositoryImpl:
    @pytest.fixture
    def mock_feed_driver(self):
        return Mock()

    @pytest.fixture
    def mock_favicon_driver(self):
        return Mock()

    @pytest.fixture
    def feed_repository(self, mock_feed_driver, mock_favicon_driver):
        return FeedRepositoryImpl(mock_feed_driver, mock_favicon_driver)

    def test_get_feed_by_name(self, feed_repository, mock_feed_driver):
        # Setup
        mock_feed_driver.get_feed_by_name.return_value = {
            "name": "Tech Blog",
            "url": "https://example.com/feed.xml",
            "icon": "https://example.com/favicon.ico",
            "time": 1700000000,
        }

        # Execute
        result = feed_repository.get_feed_by_name("Tech Blog")

        # Assert
        assert result.name == "Tech Blog"
        assert result.url == "https://example.com/feed.xml"
        assert result.icon == "https://example.com/favicon.ico"
        assert result.last_published_datetime == datetime.fromtimestamp(1700000000)
        mock_feed_driver.get_feed_by_name.assert_called_once_with(name="Tech Blog")

    def test_get_all_feeds_with_existing_time_and_icon(
        self, feed_repository, mock_feed_driver, mock_favicon_driver
    ):
        # Setup
        mock_feed_driver.get_all_feeds.return_value = [
            {
                "name": "Blog 1",
                "url": "https://example.com/feed1.xml",
                "icon": "https://example.com/favicon1.ico",
                "time": 1700000000,
            },
            {
                "name": "Blog 2",
                "url": "https://example.com/feed2.xml",
                "icon": "https://example.com/favicon2.ico",
                "time": 1700001000,
            },
        ]

        # Execute
        result = feed_repository.get_all_feeds()

        # Assert
        assert len(result) == 2
        assert result[0].name == "Blog 1"
        assert result[0].icon == "https://example.com/favicon1.ico"
        assert result[1].name == "Blog 2"
        # Favicon driver should not be called when icon exists
        mock_favicon_driver.get_favicon.assert_not_called()
        mock_feed_driver.update_feed_icon.assert_not_called()

    def test_get_all_feeds_with_missing_icon(
        self, feed_repository, mock_feed_driver, mock_favicon_driver
    ):
        # Setup
        mock_feed_driver.get_all_feeds.return_value = [
            {
                "name": "Blog 1",
                "url": "https://example.com/feed.xml",
                "icon": None,
                "time": 1700000000,
            }
        ]
        mock_favicon_driver.get_favicon.return_value = (
            "https://example.com/new-favicon.ico"
        )

        # Execute
        result = feed_repository.get_all_feeds()

        # Assert
        assert len(result) == 1
        assert result[0].icon == "https://example.com/new-favicon.ico"
        mock_favicon_driver.get_favicon.assert_called_once_with(
            "https://example.com/feed.xml"
        )
        mock_feed_driver.update_feed_icon.assert_called_once_with(
            name="Blog 1", icon="https://example.com/new-favicon.ico"
        )

    def test_get_all_feeds_with_empty_icon(
        self, feed_repository, mock_feed_driver, mock_favicon_driver
    ):
        # Setup
        mock_feed_driver.get_all_feeds.return_value = [
            {
                "name": "Blog 1",
                "url": "https://example.com/feed.xml",
                "icon": "",
                "time": 1700000000,
            }
        ]
        mock_favicon_driver.get_favicon.return_value = "https://example.com/favicon.ico"

        # Execute
        result = feed_repository.get_all_feeds()

        # Assert
        assert result[0].icon == "https://example.com/favicon.ico"
        mock_favicon_driver.get_favicon.assert_called_once()

    def test_get_all_feeds_with_none_time(
        self, feed_repository, mock_feed_driver, mock_favicon_driver
    ):
        # Setup
        mock_feed_driver.get_all_feeds.return_value = [
            {
                "name": "New Blog",
                "url": "https://example.com/feed.xml",
                "icon": "https://example.com/favicon.ico",
                "time": None,
            }
        ]

        # Execute
        before_execution = datetime.now()
        result = feed_repository.get_all_feeds()
        after_execution = datetime.now()

        # Assert - should set time to 30 days ago
        assert len(result) == 1
        expected_time = datetime.now() - timedelta(days=30)
        # Allow 1 minute tolerance for test execution time
        assert result[0].last_published_datetime >= expected_time - timedelta(minutes=1)
        assert result[0].last_published_datetime <= after_execution

    def test_get_all_feeds_with_empty_time(
        self, feed_repository, mock_feed_driver, mock_favicon_driver
    ):
        # Setup
        mock_feed_driver.get_all_feeds.return_value = [
            {
                "name": "New Blog",
                "url": "https://example.com/feed.xml",
                "icon": "https://example.com/favicon.ico",
                "time": "",
            }
        ]

        # Execute
        result = feed_repository.get_all_feeds()

        # Assert - should set time to 30 days ago
        assert len(result) == 1
        expected_time = datetime.now() - timedelta(days=30)
        assert result[0].last_published_datetime >= expected_time - timedelta(minutes=1)

    def test_update_last_published(self, feed_repository, mock_feed_driver):
        # Setup
        test_time = datetime(2025, 11, 17, 12, 0, 0)
        expected_unixtime = int(test_time.timestamp())
        mock_feed_driver.update_last_published.return_value = {
            "name": "Tech Blog",
            "time": expected_unixtime,
        }

        # Execute
        result = feed_repository.update_last_published("Tech Blog", test_time)

        # Assert
        mock_feed_driver.update_last_published.assert_called_once_with(
            "Tech Blog", expected_unixtime
        )
        assert result["name"] == "Tech Blog"
        assert result["time"] == expected_unixtime

    def test_update_last_published_floors_timestamp(
        self, feed_repository, mock_feed_driver
    ):
        # Setup - test with microseconds to ensure floor operation
        test_time = datetime(2025, 11, 17, 12, 0, 0, 999999)
        expected_unixtime = int(test_time.timestamp())
        mock_feed_driver.update_last_published.return_value = {
            "name": "Tech Blog",
            "time": expected_unixtime,
        }

        # Execute
        result = feed_repository.update_last_published("Tech Blog", test_time)

        # Assert - should use floor, not round
        called_unixtime = mock_feed_driver.update_last_published.call_args[0][1]
        assert called_unixtime == int(test_time.timestamp())

    def test_get_all_feeds_mixed_scenarios(
        self, feed_repository, mock_feed_driver, mock_favicon_driver
    ):
        # Setup - test with mix of valid, missing icon, and missing time
        mock_feed_driver.get_all_feeds.return_value = [
            {
                "name": "Complete Blog",
                "url": "https://example.com/feed1.xml",
                "icon": "https://example.com/favicon1.ico",
                "time": 1700000000,
            },
            {
                "name": "No Icon Blog",
                "url": "https://example.com/feed2.xml",
                "icon": None,
                "time": 1700001000,
            },
            {
                "name": "New Blog",
                "url": "https://example.com/feed3.xml",
                "icon": "https://example.com/favicon3.ico",
                "time": None,
            },
        ]
        mock_favicon_driver.get_favicon.return_value = (
            "https://example.com/new-favicon.ico"
        )

        # Execute
        result = feed_repository.get_all_feeds()

        # Assert
        assert len(result) == 3
        # First blog - complete data
        assert result[0].name == "Complete Blog"
        assert result[0].icon == "https://example.com/favicon1.ico"
        assert result[0].last_published_datetime == datetime.fromtimestamp(1700000000)
        # Second blog - missing icon
        assert result[1].name == "No Icon Blog"
        assert result[1].icon == "https://example.com/new-favicon.ico"
        # Third blog - missing time
        assert result[2].name == "New Blog"
        expected_time = datetime.now() - timedelta(days=30)
        assert result[2].last_published_datetime >= expected_time - timedelta(minutes=1)

        # Favicon driver called once for missing icon
        mock_favicon_driver.get_favicon.assert_called_once()
