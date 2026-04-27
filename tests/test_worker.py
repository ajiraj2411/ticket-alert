import pytest
from unittest.mock import patch, MagicMock
from app.worker import check_booking, notify


@patch('app.worker.requests.get')
def test_check_booking_success(mock_get):
    # Mock the API responses
    mock_search_response = MagicMock()
    mock_search_response.status_code = 200
    mock_search_response.json.return_value = {
        "data": [{"eventId": "123"}]
    }

    mock_show_response = MagicMock()
    mock_show_response.status_code = 200
    mock_show_response.json.return_value = {
        "venues": [{"name": "Test Venue"}]
    }

    mock_get.side_effect = [mock_search_response, mock_show_response]

    result = check_booking("test movie", "test city")
    assert result is True


@patch('app.worker.requests.get')
def test_check_booking_no_venues(mock_get):
    mock_search_response = MagicMock()
    mock_search_response.status_code = 200
    mock_search_response.json.return_value = {
        "data": [{"eventId": "123"}]
    }

    mock_show_response = MagicMock()
    mock_show_response.status_code = 200
    mock_show_response.json.return_value = {}

    mock_get.side_effect = [mock_search_response, mock_show_response]

    result = check_booking("test movie", "test city")
    assert result is False


@patch('app.worker.requests.post')
def test_notify(mock_post):
    notify("123", "Test message")
    mock_post.assert_called_once()