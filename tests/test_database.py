"""Unit tests for SQLite database persistence and duplicate prevention."""

import pytest
from database import Database


@pytest.fixture
def temp_db(tmp_path):
    """Fixture providing a clean temporary SQLite database using tmp_path."""
    db_file = tmp_path / "test_aelafat.db"
    db = Database(str(db_file))
    return db


def test_settings_crud(temp_db):
    """Test setting and getting configuration values."""
    temp_db.set_setting("test_key", "hello_world")
    assert temp_db.get_setting("test_key") == "hello_world"

    # Update value
    temp_db.set_setting("test_key", "new_value")
    assert temp_db.get_setting("test_key") == "new_value"

    # Default fallback
    assert temp_db.get_setting("non_existent", "fallback") == "fallback"


def test_group_configuration(temp_db):
    """Test group ID configuration."""
    assert temp_db.get_configured_group_id() is None
    temp_db.set_configured_group_id(-1001234567890)
    assert temp_db.get_configured_group_id() == -1001234567890


def test_pause_resume(temp_db):
    """Test pause and resume setting."""
    assert not temp_db.is_paused()
    temp_db.set_paused(True)
    assert temp_db.is_paused()
    temp_db.set_paused(False)
    assert not temp_db.is_paused()


def test_duplicate_posting_prevention(temp_db):
    """Verify that duplicate postings on the same day to the same chat are detected."""
    chat_id = -100987654321
    post_date = "2026-11-23"

    # Initially, has not posted today
    assert not temp_db.has_posted_today(post_date, chat_id)

    # Record successful post
    row_id = temp_db.record_post(
        post_date=post_date,
        chat_id=chat_id,
        days_remaining=43,
        post_type="daily",
        message_id=555,
        status="success",
    )
    assert row_id > 0

    # Now, duplicate check must return True
    assert temp_db.has_posted_today(post_date, chat_id)

    # Different date should still be False
    assert not temp_db.has_posted_today("2026-11-24", chat_id)

    # Different chat_id should still be False
    assert not temp_db.has_posted_today(post_date, -100000000)


def test_milestones_tracking(temp_db):
    """Test milestone message tracking."""
    assert not temp_db.is_milestone_sent(30)
    temp_db.record_milestone_sent(days_remaining=30, chat_id=-1001, message_id=12)
    assert temp_db.is_milestone_sent(30)
    assert not temp_db.is_milestone_sent(14)


def test_admin_management(temp_db):
    """Test adding, querying, and removing administrators."""
    user_id = 99887766
    assert not temp_db.is_admin(user_id)

    temp_db.add_admin(user_id, username="orthodox_servant", added_by=112233)
    assert temp_db.is_admin(user_id)

    admins = temp_db.get_all_admins()
    assert len(admins) == 1
    assert admins[0]["user_id"] == user_id
    assert admins[0]["username"] == "orthodox_servant"

    removed = temp_db.remove_admin(user_id)
    assert removed is True
    assert not temp_db.is_admin(user_id)
