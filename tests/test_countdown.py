"""Unit tests for countdown date and time calculations."""

from datetime import datetime
from zoneinfo import ZoneInfo
import pytest

from countdown import calculate_countdown, CountdownInfo, MILESTONE_DAYS


def test_countdown_future_date():
    """Test countdown calculation for a known future date."""
    tz = ZoneInfo("Africa/Addis_Ababa")
    # Simulate current date: 2026-11-23 at 10:00:00 EAT
    mock_now = datetime(2026, 11, 23, 10, 0, 0, tzinfo=tz)
    target_date = "2027-01-05"

    info: CountdownInfo = calculate_countdown(
        target_date_str=target_date,
        timezone_name="Africa/Addis_Ababa",
        now=mock_now,
    )

    # From 2026-11-23 to 2027-01-05 is 43 calendar days
    assert info.days_remaining == 43
    assert not info.is_event_day
    assert not info.is_past
    assert info.target_datetime.year == 2027
    assert info.target_datetime.month == 1
    assert info.target_datetime.day == 5


def test_countdown_milestones():
    """Verify that milestone days are correctly detected."""
    tz = ZoneInfo("Africa/Addis_Ababa")

    # 30 days before Jan 5, 2027 is Dec 6, 2026
    now_30d = datetime(2026, 12, 6, 9, 0, 0, tzinfo=tz)
    info_30d = calculate_countdown("2027-01-05", now=now_30d)
    assert info_30d.days_remaining == 30
    assert info_30d.is_milestone
    assert info_30d.milestone_days == 30

    # 7 days before Jan 5, 2027 is Dec 29, 2026
    now_7d = datetime(2026, 12, 29, 9, 0, 0, tzinfo=tz)
    info_7d = calculate_countdown("2027-01-05", now=now_7d)
    assert info_7d.days_remaining == 7
    assert info_7d.is_milestone
    assert info_7d.milestone_days == 7

    # 1 day before Jan 5, 2027 is Jan 4, 2027
    now_1d = datetime(2027, 1, 4, 9, 0, 0, tzinfo=tz)
    info_1d = calculate_countdown("2027-01-05", now=now_1d)
    assert info_1d.days_remaining == 1
    assert info_1d.is_milestone
    assert info_1d.milestone_days == 1


def test_countdown_event_day():
    """Test behavior on the event day itself (day 0)."""
    tz = ZoneInfo("Africa/Addis_Ababa")
    now_event_day = datetime(2027, 1, 5, 9, 0, 0, tzinfo=tz)

    info = calculate_countdown("2027-01-05", now=now_event_day)
    assert info.days_remaining == 0
    assert info.is_event_day
    assert not info.is_past
    assert info.is_milestone
    assert info.milestone_days == 0


def test_countdown_past_event():
    """Test behavior after the event has passed."""
    tz = ZoneInfo("Africa/Addis_Ababa")
    now_past = datetime(2027, 1, 6, 9, 0, 0, tzinfo=tz)

    info = calculate_countdown("2027-01-05", now=now_past)
    assert info.days_remaining < 0
    assert not info.is_event_day
    assert info.is_past


def test_timezone_conversion():
    """Verify timezone conversions from UTC to Africa/Addis_Ababa (+3 hours)."""
    utc_tz = ZoneInfo("UTC")
    # 2026-11-23 21:00 UTC is 2026-11-24 00:00 Africa/Addis_Ababa
    utc_now = datetime(2026, 11, 23, 21, 30, 0, tzinfo=utc_tz)

    info = calculate_countdown(
        "2027-01-05",
        timezone_name="Africa/Addis_Ababa",
        now=utc_now,
    )

    assert info.current_datetime.day == 24
    assert info.current_datetime.hour == 0
    assert info.current_datetime.minute == 30
