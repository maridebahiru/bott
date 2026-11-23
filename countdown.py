"""Countdown calculation utilities for Aelafat Countdown Bot.

Handles dynamic date and time math in the Africa/Addis_Ababa timezone.
"""

from dataclasses import dataclass
from datetime import datetime, time, timedelta
from typing import Optional
from zoneinfo import ZoneInfo


@dataclass(frozen=True)
class CountdownInfo:
    """Detailed countdown status representation."""

    target_datetime: datetime
    current_datetime: datetime
    days_remaining: int
    hours_remaining: int
    minutes_remaining: int
    seconds_remaining: int
    total_seconds: float
    is_event_day: bool
    is_past: bool
    is_milestone: bool
    milestone_days: Optional[int]


# Recognized milestone days
MILESTONE_DAYS = {30, 14, 7, 3, 2, 1, 0}


def calculate_countdown(
    target_date_str: str = "2027-01-05",
    timezone_name: str = "Africa/Addis_Ababa",
    now: Optional[datetime] = None,
) -> CountdownInfo:
    """
    Calculate real-time countdown details to the specified target date.

    :param target_date_str: Target date in 'YYYY-MM-DD' format.
    :param timezone_name: IANA timezone string, default 'Africa/Addis_Ababa'.
    :param now: Optional override of current datetime (useful for unit testing).
    """
    try:
        tz = ZoneInfo(timezone_name)
    except Exception:
        tz = ZoneInfo("Africa/Addis_Ababa")

    # Current time in target timezone
    if now is None:
        current_dt = datetime.now(tz)
    else:
        if now.tzinfo is None:
            current_dt = now.replace(tzinfo=tz)
        else:
            current_dt = now.astimezone(tz)

    # Parse target date
    parts = [int(p) for p in target_date_str.split("-")]
    target_date = datetime(parts[0], parts[1], parts[2], 0, 0, 0, tzinfo=tz)

    current_date = current_dt.date()
    target_date_only = target_date.date()

    # Calendar days difference
    calendar_days = (target_date_only - current_date).days

    # Time delta
    time_diff = target_date - current_dt
    total_seconds = time_diff.total_seconds()

    is_event_day = calendar_days == 0
    is_past = calendar_days < 0

    if calendar_days > 0:
        days_remaining = calendar_days
        # Time remaining until midnight of event day
        hours_remaining = int(total_seconds // 3600) % 24
        minutes_remaining = int(total_seconds // 60) % 60
        seconds_remaining = int(total_seconds) % 60
    elif is_event_day:
        days_remaining = 0
        hours_remaining = 0
        minutes_remaining = 0
        seconds_remaining = 0
    else:
        days_remaining = calendar_days  # negative
        hours_remaining = 0
        minutes_remaining = 0
        seconds_remaining = 0

    is_milestone = calendar_days in MILESTONE_DAYS
    milestone_days = calendar_days if is_milestone else None

    return CountdownInfo(
        target_datetime=target_date,
        current_datetime=current_dt,
        days_remaining=days_remaining,
        hours_remaining=hours_remaining,
        minutes_remaining=minutes_remaining,
        seconds_remaining=seconds_remaining,
        total_seconds=total_seconds,
        is_event_day=is_event_day,
        is_past=is_past,
        is_milestone=is_milestone,
        milestone_days=milestone_days,
    )
