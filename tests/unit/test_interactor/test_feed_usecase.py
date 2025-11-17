from datetime import datetime
from unittest.mock import Mock
import pytest
from domain.feed import Feed
from interactor.feed_usecase import FeedUsecaseImpl


class TestFeedUsecaseImpl:
    @pytest.fixture
    def mock_feed_repository(self):
        return Mock()

    @pytest.fixture
    def feed_usecase(self, mock_feed_repository):
        return FeedUsecaseImpl(mock_feed_repository)

    @pytest.fixture
    def sample_feeds(self):
        return [
            Feed(
                name="Tech Blog 1",
                url="https://example.com/feed1.xml",
                icon="https://example.com/favicon1.ico",
                last_published_datetime=datetime(2025, 11, 17, 10, 0, 0),
            ),
            Feed(
                name="Tech Blog 2",
                url="https://example.com/feed2.xml",
                icon="https://example.com/favicon2.ico",
                last_published_datetime=datetime(2025, 11, 17, 11, 0, 0),
            ),
        ]

    def test_get_all_feed(self, feed_usecase, mock_feed_repository, sample_feeds):
        # Setup
        mock_feed_repository.get_all_feeds.return_value = sample_feeds

        # Execute
        result = feed_usecase.get_all_feed()

        # Assert
        mock_feed_repository.get_all_feeds.assert_called_once()
        assert result == sample_feeds
        assert len(result) == 2
        assert result[0].name == "Tech Blog 1"
        assert result[1].name == "Tech Blog 2"

    def test_get_all_feed_empty(self, feed_usecase, mock_feed_repository):
        # Setup
        mock_feed_repository.get_all_feeds.return_value = []

        # Execute
        result = feed_usecase.get_all_feed()

        # Assert
        mock_feed_repository.get_all_feeds.assert_called_once()
        assert result == []
        assert len(result) == 0

    def test_update_last_published(self, feed_usecase, mock_feed_repository):
        # Setup
        feed = Feed(
            name="Tech Blog",
            url="https://example.com/feed.xml",
            icon="https://example.com/favicon.ico",
            last_published_datetime=datetime(2025, 11, 17, 10, 0, 0),
        )
        new_time = datetime(2025, 11, 17, 12, 0, 0)
        expected_result = {"name": "Tech Blog", "time": 1731845100}
        mock_feed_repository.update_last_published.return_value = expected_result

        # Execute
        result = feed_usecase.update_last_published(feed, new_time)

        # Assert
        mock_feed_repository.update_last_published.assert_called_once_with(
            "Tech Blog", new_time
        )
        assert result == expected_result
        assert result["name"] == "Tech Blog"

    def test_update_last_published_with_different_feeds(
        self, feed_usecase, mock_feed_repository, sample_feeds
    ):
        # Test updating multiple feeds
        for feed in sample_feeds:
            new_time = datetime(2025, 11, 18, 10, 0, 0)
            expected_result = {"name": feed.name, "time": 1731924600}
            mock_feed_repository.update_last_published.return_value = expected_result

            # Execute
            result = feed_usecase.update_last_published(feed, new_time)

            # Assert
            assert result["name"] == feed.name

    def test_repository_method_delegation(
        self, feed_usecase, mock_feed_repository, sample_feeds
    ):
        # Verify that usecase properly delegates to repository
        mock_feed_repository.get_all_feeds.return_value = sample_feeds

        # Execute get_all_feed
        result = feed_usecase.get_all_feed()

        # Verify delegation
        mock_feed_repository.get_all_feeds.assert_called_once()
        assert result == sample_feeds
