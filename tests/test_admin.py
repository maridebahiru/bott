"""Unit tests for administrative authorization and command logic."""

from unittest.mock import AsyncMock, MagicMock
import pytest
from telegram.constants import ChatMemberStatus
from handlers.admin import is_user_authorized_admin
from config import Config
from database import Database


@pytest.fixture
def mock_context(tmp_path):
    """Create a mock Telegram context with initialized Config and Database."""
    db_file = tmp_path / "test_admin.db"
    db = Database(str(db_file))

    cfg = Config(
        bot_token="test_token",
        owner_ids=[111111],
        default_group_id=None,
        event_date_str="2027-01-05",
        event_date=MagicMock(),
        timezone_name="Africa/Addis_Ababa",
        tz=MagicMock(),
        post_time_str="09:00",
        post_time=MagicMock(),
        database_path=str(db_file),
        promo_image_url=None,
        default_language="both",
        log_level="INFO",
    )

    context = MagicMock()
    context.bot_data = {"config": cfg, "db": db}
    return context, db


@pytest.mark.asyncio
async def test_bot_owner_authorized(mock_context):
    """Verify that a configured bot owner is authorized."""
    context, _ = mock_context
    update = MagicMock()
    update.effective_user.id = 111111  # Matches owner_ids
    update.effective_chat.type = "private"

    authorized = await is_user_authorized_admin(update, context)
    assert authorized is True


@pytest.mark.asyncio
async def test_unauthorized_user(mock_context):
    """Verify that an arbitrary user is denied access."""
    context, _ = mock_context
    update = MagicMock()
    update.effective_user.id = 999999  # Not owner, not in db
    update.effective_chat.type = "private"

    authorized = await is_user_authorized_admin(update, context)
    assert authorized is False


@pytest.mark.asyncio
async def test_db_admin_authorized(mock_context):
    """Verify that a database-registered administrator is authorized."""
    context, db = mock_context
    db.add_admin(222222, username="moderator")

    update = MagicMock()
    update.effective_user.id = 222222
    update.effective_chat.type = "private"

    authorized = await is_user_authorized_admin(update, context)
    assert authorized is True


@pytest.mark.asyncio
async def test_telegram_group_admin_authorized(mock_context):
    """Verify that a Telegram chat admin in a group is recognized as authorized."""
    context, _ = mock_context
    update = MagicMock()
    update.effective_user.id = 333333
    update.effective_chat.type = "supergroup"

    # Mock chat.get_member returning administrator status
    member_mock = MagicMock()
    member_mock.status = ChatMemberStatus.ADMINISTRATOR
    update.effective_chat.get_member = AsyncMock(return_value=member_mock)

    authorized = await is_user_authorized_admin(update, context)
    assert authorized is True
