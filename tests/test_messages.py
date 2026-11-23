"""Unit tests for messages and spiritual reflections."""

from datetime import datetime
from zoneinfo import ZoneInfo
from countdown import calculate_countdown
from messages import (
    DAILY_REFLECTIONS_AMHARIC,
    DAILY_REFLECTIONS_ENGLISH,
    MILESTONE_MESSAGES,
    format_countdown_message,
    get_daily_reflection,
)


def test_reflections_count_and_content():
    """Verify there are at least 30 verified Amharic reflections and non-empty content."""
    assert len(DAILY_REFLECTIONS_AMHARIC) >= 30
    assert len(DAILY_REFLECTIONS_ENGLISH) >= 30
    assert len(DAILY_REFLECTIONS_AMHARIC) == len(DAILY_REFLECTIONS_ENGLISH)

    for item in DAILY_REFLECTIONS_AMHARIC:
        assert isinstance(item, str)
        assert len(item.strip()) > 10

    for item in DAILY_REFLECTIONS_ENGLISH:
        assert isinstance(item, str)
        assert len(item.strip()) > 10


def test_milestone_messages_exist():
    """Check required milestone milestones: 30, 14, 7, 3, 2, 1, 0."""
    required = {30, 14, 7, 3, 2, 1, 0}
    for days in required:
        assert days in MILESTONE_MESSAGES
        assert "am" in MILESTONE_MESSAGES[days]
        assert "en" in MILESTONE_MESSAGES[days]
        assert len(MILESTONE_MESSAGES[days]["am"]) > 0
        assert len(MILESTONE_MESSAGES[days]["en"]) > 0


def test_bilingual_message_formatting():
    """Test formatting with bilingual option."""
    tz = ZoneInfo("Africa/Addis_Ababa")
    mock_now = datetime(2026, 11, 23, 9, 0, 0, tzinfo=tz)
    info = calculate_countdown("2027-01-05", now=mock_now)

    msg = format_countdown_message(info, language="both")
    assert "የአእላፋት ዝማሬ" in msg
    assert "Aelafat Zimare" in msg
    assert "January 05, 2027" in msg or "January 5, 2027" in msg
    assert str(info.days_remaining) in msg


def test_amharic_only_formatting():
    """Test formatting with Amharic only."""
    tz = ZoneInfo("Africa/Addis_Ababa")
    mock_now = datetime(2026, 11, 23, 9, 0, 0, tzinfo=tz)
    info = calculate_countdown("2027-01-05", now=mock_now)

    msg = format_countdown_message(info, language="am")
    assert "የአእላፋት ዝማሬ" in msg
    assert "ቀሪ" in msg
    assert "ቀናት ብቻ!" in msg


def test_event_day_celebration_message():
    """Test celebration message formatting on day 0."""
    tz = ZoneInfo("Africa/Addis_Ababa")
    event_day_now = datetime(2027, 1, 5, 9, 0, 0, tzinfo=tz)
    info = calculate_countdown("2027-01-05", now=event_day_now)

    msg = format_countdown_message(info, language="both")
    assert "ዛሬ ታላቁ ቀን የአእላፋት ዝማሬ ደረሰ!" in msg
    assert "Glorious Day of Aelafat Zimare" in msg


def test_past_event_message():
    """Test message after event date."""
    tz = ZoneInfo("Africa/Addis_Ababa")
    past_now = datetime(2027, 1, 10, 9, 0, 0, tzinfo=tz)
    info = calculate_countdown("2027-01-05", now=past_now)

    msg = format_countdown_message(info, language="both")
    assert "በታላቅ በረከት ተከናውኗል" in msg
    assert "took place" in msg
