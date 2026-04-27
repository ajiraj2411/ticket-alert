import pytest
from unittest.mock import patch, MagicMock
from app.bot import handle_message, validate_movie_city


def test_validate_movie_city():
    assert validate_movie_city("Leo", "Chennai") is True
    assert validate_movie_city("Movie 123", "City-Name") is True
    assert validate_movie_city("", "Chennai") is False
    assert validate_movie_city("Leo", "") is False
    assert validate_movie_city("Movie!", "Chennai") is False
    assert validate_movie_city("a" * 101, "Chennai") is False
    assert validate_movie_city("Leo", "b" * 51) is False


@patch('app.bot.SessionLocal')
@patch('app.bot.send_message')
def test_handle_start(mock_send, mock_session):
    mock_db = MagicMock()
    mock_session.return_value = mock_db

    data = {
        "message": {
            "chat": {"id": "123"},
            "text": "/start"
        }
    }

    handle_message(data)

    mock_send.assert_called_with("123", "🎬 Welcome!\n\nCommands:\n/add movie,city\n/list\n/remove movie,city\n/status")


@patch('app.bot.SessionLocal')
@patch('app.bot.send_message')
def test_handle_add(mock_send, mock_session):
    mock_db = MagicMock()
    mock_session.return_value = mock_db
    mock_query = MagicMock()
    mock_db.query.return_value = mock_query
    mock_query.filter_by.return_value.first.return_value = None  # No existing alert

    data = {
        "message": {
            "chat": {"id": "123"},
            "text": "/add test movie,test city"
        }
    }

    handle_message(data)

    mock_send.assert_called_with("123", "✅ Alert added!\n🎬 test movie\n📍 test city")