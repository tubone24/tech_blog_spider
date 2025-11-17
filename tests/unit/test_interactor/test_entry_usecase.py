from datetime import datetime
from unittest.mock import Mock
import pytest
from domain.entry import Entry, Keyword
from domain.feed import Feed
from interactor.entry_usecase import EntryUsecaseImpl


class TestEntryUsecaseImpl:
    @pytest.fixture
    def mock_entry_repository(self):
        return Mock()

    @pytest.fixture
    def mock_slack_output(self):
        return Mock()

    @pytest.fixture
    def entry_usecase(self, mock_entry_repository, mock_slack_output):
        return EntryUsecaseImpl(mock_entry_repository, mock_slack_output)

    @pytest.fixture
    def sample_feed(self):
        return Feed(
            name="Tech Blog",
            url="https://example.com/feed.xml",
            icon="https://example.com/favicon.ico",
            last_published_datetime=datetime(2025, 11, 17, 10, 0, 0),
        )

    @pytest.fixture
    def sample_entries(self):
        return [
            Entry(
                title="Article 1",
                url="https://example.com/article1",
                summary="Summary 1",
                image="https://example.com/image1.png",
                language="en",
                text="Text 1",
                published_date=datetime(2025, 11, 17, 11, 0, 0),
                keywords=[Keyword(word="python", score=0.9)],
            ),
            Entry(
                title="Article 2",
                url="https://example.com/article2",
                summary="Summary 2",
                image="https://example.com/image2.png",
                language="ja",
                text="Text 2",
                published_date=datetime(2025, 11, 17, 12, 0, 0),
                keywords=[Keyword(word="testing", score=0.85)],
            ),
        ]

    def test_post_unread_entries_with_new_entries(
        self,
        entry_usecase,
        mock_entry_repository,
        mock_slack_output,
        sample_feed,
        sample_entries,
    ):
        # Setup
        mock_entry_repository.get_until_last_published_entries.return_value = (
            sample_entries
        )

        # Execute
        result = entry_usecase.post_unread_entries(sample_feed)

        # Assert
        mock_entry_repository.get_until_last_published_entries.assert_called_once_with(
            sample_feed.url, sample_feed.last_published_datetime
        )
        assert mock_slack_output.post_slack.call_count == 2

        # Verify first call
        first_call = mock_slack_output.post_slack.call_args_list[0]
        assert first_call[1]["feed_name"] == "Tech Blog"
        assert first_call[1]["feed_url"] == "https://example.com/feed.xml"
        assert first_call[1]["entry"] == sample_entries[0]

        # Verify second call
        second_call = mock_slack_output.post_slack.call_args_list[1]
        assert second_call[1]["entry"] == sample_entries[1]

        # Verify return value is the published_date of the last entry
        assert result == sample_entries[-1].published_date

    def test_post_unread_entries_with_no_new_entries(
        self,
        entry_usecase,
        mock_entry_repository,
        mock_slack_output,
        sample_feed,
    ):
        # Setup
        mock_entry_repository.get_until_last_published_entries.return_value = []

        # Execute
        result = entry_usecase.post_unread_entries(sample_feed)

        # Assert
        mock_entry_repository.get_until_last_published_entries.assert_called_once_with(
            sample_feed.url, sample_feed.last_published_datetime
        )
        mock_slack_output.post_slack.assert_not_called()

        # Verify return value is the feed's last_published_datetime
        assert result == sample_feed.last_published_datetime

    def test_post_unread_entries_with_single_entry(
        self,
        entry_usecase,
        mock_entry_repository,
        mock_slack_output,
        sample_feed,
        sample_entries,
    ):
        # Setup
        single_entry = [sample_entries[0]]
        mock_entry_repository.get_until_last_published_entries.return_value = (
            single_entry
        )

        # Execute
        result = entry_usecase.post_unread_entries(sample_feed)

        # Assert
        assert mock_slack_output.post_slack.call_count == 1
        mock_slack_output.post_slack.assert_called_once()
        call_args = mock_slack_output.post_slack.call_args[1]
        assert call_args["feed_name"] == "Tech Blog"
        assert call_args["entry"] == sample_entries[0]

        # Verify return value
        assert result == sample_entries[0].published_date

    def test_post_unread_entries_with_feed_without_icon(
        self,
        entry_usecase,
        mock_entry_repository,
        mock_slack_output,
        sample_entries,
    ):
        # Setup
        feed_without_icon = Feed(
            name="Tech Blog",
            url="https://example.com/feed.xml",
            icon=None,
            last_published_datetime=datetime(2025, 11, 17, 10, 0, 0),
        )
        mock_entry_repository.get_until_last_published_entries.return_value = [
            sample_entries[0]
        ]

        # Execute
        result = entry_usecase.post_unread_entries(feed_without_icon)

        # Assert
        call_args = mock_slack_output.post_slack.call_args[1]
        assert call_args["feed_icon"] is None
