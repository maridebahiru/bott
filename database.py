"""SQLite Database management for Aelafat Countdown Bot.

Handles persistent storage of:
- Bot settings (group ID, event date, posting time, timezone, pause status, promo image)
- Posting history and duplicate prevention
- Milestone records
- Administrator accounts
"""

import sqlite3
import logging
from contextlib import contextmanager
from datetime import datetime
from pathlib import Path
from typing import Any, Generator, Optional

logger = logging.getLogger(__name__)


class Database:
    """Thread-safe SQLite database manager for Aelafat Countdown Bot."""

    def __init__(self, db_path: str = "aelafat.db"):
        self.db_path = db_path
        parent_dir = Path(db_path).parent
        if parent_dir and not parent_dir.exists():
            parent_dir.mkdir(parents=True, exist_ok=True)
        self._init_db()

    @contextmanager
    def _connection(self) -> Generator[sqlite3.Connection, None, None]:
        """Context manager creating a connection that commits and guarantees closure."""
        conn = sqlite3.connect(self.db_path, timeout=30.0)
        conn.row_factory = sqlite3.Row
        conn.execute("PRAGMA foreign_keys = ON")
        try:
            conn.execute("PRAGMA journal_mode = WAL")
        except sqlite3.OperationalError:
            pass

        try:
            yield conn
            conn.commit()
        except Exception:
            conn.rollback()
            raise
        finally:
            conn.close()

    def _init_db(self) -> None:
        """Create tables and default settings if they do not exist."""
        with self._connection() as conn:
            cursor = conn.cursor()

            # Settings table (Key-Value configuration)
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS settings (
                    key TEXT PRIMARY KEY,
                    value TEXT NOT NULL,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)

            # Posting history table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS posting_history (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    post_date TEXT NOT NULL,
                    post_type TEXT NOT NULL DEFAULT 'daily',
                    chat_id INTEGER NOT NULL,
                    message_id INTEGER,
                    days_remaining INTEGER NOT NULL,
                    status TEXT NOT NULL DEFAULT 'success',
                    error_message TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)
            cursor.execute("""
                CREATE INDEX IF NOT EXISTS idx_posting_history_date_chat
                ON posting_history(post_date, chat_id)
            """)

            # Milestone messages sent tracking
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS milestones_sent (
                    days_remaining INTEGER PRIMARY KEY,
                    chat_id INTEGER NOT NULL,
                    message_id INTEGER,
                    sent_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)

            # Bot Administrators table
            cursor.execute("""
                CREATE TABLE IF NOT EXISTS admin_users (
                    user_id INTEGER PRIMARY KEY,
                    username TEXT,
                    added_by INTEGER,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)

            logger.info("Database initialized successfully at %s", self.db_path)

    # -------------------------------------------------------------
    # Settings Management
    # -------------------------------------------------------------
    def get_setting(self, key: str, default: Optional[str] = None) -> Optional[str]:
        """Retrieve a setting by key."""
        with self._connection() as conn:
            row = conn.execute(
                "SELECT value FROM settings WHERE key = ?", (key,)
            ).fetchone()
            if row:
                return row["value"]
            return default

    def set_setting(self, key: str, value: Any) -> None:
        """Store or update a setting."""
        with self._connection() as conn:
            conn.execute(
                """
                INSERT INTO settings (key, value, updated_at)
                VALUES (?, ?, CURRENT_TIMESTAMP)
                ON CONFLICT(key) DO UPDATE SET
                    value = excluded.value,
                    updated_at = CURRENT_TIMESTAMP
                """,
                (key, str(value)),
            )

    def get_all_settings(self) -> dict[str, str]:
        """Retrieve all configuration key-value pairs."""
        with self._connection() as conn:
            rows = conn.execute("SELECT key, value FROM settings").fetchall()
            return {row["key"]: row["value"] for row in rows}

    def get_configured_group_id(self) -> Optional[int]:
        """Get the configured Telegram group chat ID."""
        val = self.get_setting("telegram_group_id")
        if val:
            try:
                return int(val)
            except ValueError:
                return None
        return None

    def set_configured_group_id(self, group_id: int) -> None:
        """Set the configured Telegram group chat ID."""
        self.set_setting("telegram_group_id", group_id)

    def is_paused(self) -> bool:
        """Check if automatic daily postings are paused."""
        val = self.get_setting("is_paused", "0")
        return val in ("1", "true", "True", "yes")

    def set_paused(self, paused: bool) -> None:
        """Pause or resume automatic daily postings."""
        self.set_setting("is_paused", "1" if paused else "0")

    def get_event_date_str(self, default: str = "2027-01-05") -> str:
        """Get configured event date string (YYYY-MM-DD)."""
        return self.get_setting("event_date", default) or default

    def set_event_date_str(self, event_date_str: str) -> None:
        """Set event date string (YYYY-MM-DD)."""
        self.set_setting("event_date", event_date_str)

    def get_post_time_str(self, default: str = "09:00") -> str:
        """Get configured post time (HH:MM)."""
        return self.get_setting("post_time", default) or default

    def set_post_time_str(self, post_time_str: str) -> None:
        """Set configured post time (HH:MM)."""
        self.set_setting("post_time", post_time_str)

    def get_timezone_str(self, default: str = "Africa/Addis_Ababa") -> str:
        """Get configured timezone."""
        return self.get_setting("timezone", default) or default

    def set_timezone_str(self, tz_str: str) -> None:
        """Set configured timezone."""
        self.set_setting("timezone", tz_str)

    def get_promo_image(self) -> Optional[str]:
        """Get promo banner image URL or file path."""
        return self.get_setting("promo_image")

    def set_promo_image(self, image_url_or_path: Optional[str]) -> None:
        """Set promo banner image URL or file path."""
        if image_url_or_path:
            self.set_setting("promo_image", image_url_or_path)
        else:
            with self._connection() as conn:
                conn.execute("DELETE FROM settings WHERE key = 'promo_image'")

    # -------------------------------------------------------------
    # Posting History & Duplicate Prevention
    # -------------------------------------------------------------
    def has_posted_today(self, post_date: str, chat_id: int) -> bool:
        """
        Check if a successful daily or milestone post has already been sent
        to this chat on the specified calendar date (in Ethiopian time).
        """
        with self._connection() as conn:
            row = conn.execute(
                """
                SELECT id FROM posting_history
                WHERE post_date = ? AND chat_id = ? AND status = 'success'
                LIMIT 1
                """,
                (post_date, chat_id),
            ).fetchone()
            return row is not None

    def record_post(
        self,
        post_date: str,
        chat_id: int,
        days_remaining: int,
        post_type: str = "daily",
        message_id: Optional[int] = None,
        status: str = "success",
        error_message: Optional[str] = None,
    ) -> int:
        """Record a posting attempt into history."""
        with self._connection() as conn:
            cursor = conn.execute(
                """
                INSERT INTO posting_history (
                    post_date, post_type, chat_id, message_id,
                    days_remaining, status, error_message
                ) VALUES (?, ?, ?, ?, ?, ?, ?)
                """,
                (
                    post_date,
                    post_type,
                    chat_id,
                    message_id,
                    days_remaining,
                    status,
                    error_message,
                ),
            )
            return cursor.lastrowid or 0

    def get_last_successful_post(self, chat_id: Optional[int] = None) -> Optional[dict]:
        """Retrieve the most recent successful post."""
        with self._connection() as conn:
            if chat_id:
                row = conn.execute(
                    """
                    SELECT * FROM posting_history
                    WHERE chat_id = ? AND status = 'success'
                    ORDER BY id DESC LIMIT 1
                    """,
                    (chat_id,),
                ).fetchone()
            else:
                row = conn.execute(
                    """
                    SELECT * FROM posting_history
                    WHERE status = 'success'
                    ORDER BY id DESC LIMIT 1
                    """
                ).fetchone()
            return dict(row) if row else None

    # -------------------------------------------------------------
    # Milestones Management
    # -------------------------------------------------------------
    def is_milestone_sent(self, days_remaining: int) -> bool:
        """Check if a specific milestone countdown has already been recorded as sent."""
        with self._connection() as conn:
            row = conn.execute(
                "SELECT days_remaining FROM milestones_sent WHERE days_remaining = ?",
                (days_remaining,),
            ).fetchone()
            return row is not None

    def record_milestone_sent(
        self, days_remaining: int, chat_id: int, message_id: Optional[int] = None
    ) -> None:
        """Record a milestone message as sent."""
        with self._connection() as conn:
            conn.execute(
                """
                INSERT INTO milestones_sent (days_remaining, chat_id, message_id, sent_at)
                VALUES (?, ?, ?, CURRENT_TIMESTAMP)
                ON CONFLICT(days_remaining) DO UPDATE SET
                    chat_id = excluded.chat_id,
                    message_id = excluded.message_id,
                    sent_at = CURRENT_TIMESTAMP
                """,
                (days_remaining, chat_id, message_id),
            )

    # -------------------------------------------------------------
    # Administrator Management
    # -------------------------------------------------------------
    def is_admin(self, user_id: int) -> bool:
        """Check if a Telegram user ID is an authorized administrator in SQLite."""
        with self._connection() as conn:
            row = conn.execute(
                "SELECT user_id FROM admin_users WHERE user_id = ?", (user_id,)
            ).fetchone()
            return row is not None

    def add_admin(
        self, user_id: int, username: Optional[str] = None, added_by: Optional[int] = None
    ) -> None:
        """Add an administrator."""
        with self._connection() as conn:
            conn.execute(
                """
                INSERT OR IGNORE INTO admin_users (user_id, username, added_by)
                VALUES (?, ?, ?)
                """,
                (user_id, username, added_by),
            )

    def remove_admin(self, user_id: int) -> bool:
        """Remove an administrator. Returns True if removed."""
        with self._connection() as conn:
            cursor = conn.execute(
                "DELETE FROM admin_users WHERE user_id = ?", (user_id,)
            )
            return cursor.rowcount > 0

    def get_all_admins(self) -> list[dict]:
        """List all registered administrators."""
        with self._connection() as conn:
            rows = conn.execute("SELECT * FROM admin_users ORDER BY created_at ASC").fetchall()
            return [dict(r) for r in rows]
