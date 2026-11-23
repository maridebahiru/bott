"""Unit tests for scheduler logic and duplicate prevention in daily jobs."""

from datetime import datetime
from unittest.mock import AsyncMock, MagicMock
from zoneinfo import ZoneInfo
import pytest

from config import Config
from database import Database
from scheduler import send_daily_countdown


@pytest.fixture
def scheduler_fixture(tmp_path):
    """Setup mock environment for scheduler test."""
    db_file = tmp_path / "test_scheduler.db"
    db = Database(str(db_file))

    tz = ZoneInfo("Africa/Addis_Ababa")
    cfg = Config(
        bot_token="test_token",
        owner_ids=[111],
        default_group_id=-10012345,
        event_date_str="2027-01-05",
        event_date=datetime(2027, 1, 5, 0, 0, 0, tzinfo=tz),
        timezone_name="Africa/Addis_Ababa",
        tz=tz,
        post_time_str="09:00",
        post_time=datetime(2027, 1, 5, 9, 0, 0, tzinfo=tz).time(),
        database_path=str(db_file),
        promo_image_url=None,
        default_language="both",
        log_level="INFO",
    )

    context = MagicMock()
    context.bot_data = {"config": cfg, "db": db}
    context.bot.send_message = AsyncMock(return_value=MagicMock(message_id=101))
    context.bot.send_photo = AsyncMock(return_value=MagicMock(message_id=102))

    return context, db, cfg


@pytest.mark.asyncio
async def test_scheduler_posts_when_configured(scheduler_fixture):
    """Verify normal scheduled post execution."""
    context, db, cfg = scheduler_fixture
    db.set_configured_group_id(-10012345)

    result = await send_daily_countdown(context)
    assert result is True
    context.bot.send_message.assert_awaited_once()

    # Verify duplicate prevention: calling again on the same day returns False
    result_dup = await send_daily_countdown(context)
    assert result_dup is False


@pytest.mark.asyncio
async def test_scheduler_skips_when_paused(scheduler_fixture):
    """Verify that posting is skipped when bot is paused."""
    context, db, _ = scheduler_fixture
    db.set_configured_group_id(-10012345)
    db.set_paused(True)

    result = await send_daily_countdown(context)
    assert result is False
    context.bot.send_message.assert_not_awaited()


@pytest.mark.asyncio
async def test_scheduler_skips_when_no_group(scheduler_fixture):
    """Verify that posting is skipped when no group is configured."""
    context, db, cfg = scheduler_fixture
    # Clear group
    context.bot_data["config"] = Config(
        bot_token=cfg.bot_token,
        owner_ids=cfg.owner_ids,
        default_group_id=None,
        event_date_str=cfg.event_date_str,
        event_date=cfg.event_date,
        timezone_name=cfg.timezone_name,
        tz=cfg.tz,
        post_time_str=cfg.post_time_str,
        post_time=cfg.post_time,
        database_path=cfg.database_path,
        promo_image_url=None,
        default_language="both",
        log_level="INFO",
    )

    result = await send_daily_countdown(context)
    assert result is False
    context.bot.send_message.assert_not_awaited()
