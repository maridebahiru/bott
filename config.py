"""Configuration loader and validator for Aelafat Countdown Bot."""

import os
import logging
from dataclasses import dataclass
from datetime import datetime, time
from zoneinfo import ZoneInfo, ZoneInfoNotFoundError
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

logger = logging.getLogger(__name__)


@dataclass(frozen=True)
class Config:
    """Application configuration container."""

    bot_token: str
    owner_ids: list[int]
    default_group_id: int | None
    event_date_str: str
    event_date: datetime
    timezone_name: str
    tz: ZoneInfo
    post_time_str: str
    post_time: time
    database_path: str
    promo_image_url: str | None
    default_language: str
    log_level: str

    @classmethod
    def load(cls) -> "Config":
        """Load and validate configuration from environment variables."""
        token = os.getenv("TELEGRAM_BOT_TOKEN", "").strip()
        if not token:
            logger.warning(
                "TELEGRAM_BOT_TOKEN is not set in environment or .env! "
                "The bot will not start without a valid token."
            )

        # Parse Bot Owners / Admins
        raw_owners = os.getenv("BOT_OWNER_ID", "").strip()
        owner_ids: list[int] = []
        if raw_owners:
            for item in raw_owners.split(","):
                cleaned = item.strip()
                if cleaned:
                    try:
                        owner_ids.append(int(cleaned))
                    except ValueError:
                        logger.warning(f"Invalid BOT_OWNER_ID value '{cleaned}', skipping.")

        # Default Group ID
        raw_group = os.getenv("TELEGRAM_GROUP_ID", "").strip()
        default_group_id: int | None = None
        if raw_group:
            try:
                default_group_id = int(raw_group)
            except ValueError:
                logger.warning(f"Invalid TELEGRAM_GROUP_ID value '{raw_group}', skipping.")

        # Event Date
        event_date_str = os.getenv("EVENT_DATE", "2027-01-05").strip()
        try:
            parsed_date = datetime.strptime(event_date_str, "%Y-%m-%d")
        except ValueError as exc:
            raise ValueError(
                f"Invalid EVENT_DATE '{event_date_str}'. Expected format YYYY-MM-DD."
            ) from exc

        # Timezone
        tz_name = os.getenv("TIMEZONE", "Africa/Addis_Ababa").strip()
        try:
            tz = ZoneInfo(tz_name)
        except ZoneInfoNotFoundError:
            logger.warning(f"Timezone '{tz_name}' not found. Falling back to Africa/Addis_Ababa.")
            tz_name = "Africa/Addis_Ababa"
            tz = ZoneInfo(tz_name)

        # Construct full timezone-aware event datetime at 00:00:00
        event_datetime = datetime(
            parsed_date.year, parsed_date.month, parsed_date.day, 0, 0, 0, tzinfo=tz
        )

        # Post Time (HH:MM)
        post_time_str = os.getenv("POST_TIME", "09:00").strip()
        try:
            t_parts = post_time_str.split(":")
            post_time = time(int(t_parts[0]), int(t_parts[1]))
        except (ValueError, IndexError) as exc:
            raise ValueError(
                f"Invalid POST_TIME '{post_time_str}'. Expected format HH:MM."
            ) from exc

        # Database Path
        database_path = os.getenv("DATABASE_PATH", "aelafat.db").strip()

        # Promo image URL / path
        promo_image_url = os.getenv("PROMO_IMAGE_URL", "").strip() or None

        # Language
        default_language = os.getenv("DEFAULT_LANGUAGE", "both").strip().lower()
        if default_language not in ("am", "en", "both"):
            default_language = "both"

        # Log level
        log_level = os.getenv("LOG_LEVEL", "INFO").strip().upper()

        return cls(
            bot_token=token,
            owner_ids=owner_ids,
            default_group_id=default_group_id,
            event_date_str=event_date_str,
            event_date=event_datetime,
            timezone_name=tz_name,
            tz=tz,
            post_time_str=post_time_str,
            post_time=post_time,
            database_path=database_path,
            promo_image_url=promo_image_url,
            default_language=default_language,
            log_level=log_level,
        )


def get_config() -> Config:
    """Convenience factory function."""
    return Config.load()
