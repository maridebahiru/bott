"""Scheduler and automated daily job runner for Aelafat Countdown Bot.

Runs every day at 09:00 AM Africa/Addis_Ababa time, delivering the countdown message
to the configured Telegram group with strict duplicate prevention and milestone detection.
"""

import logging
from datetime import datetime, time
from zoneinfo import ZoneInfo
from telegram.constants import ParseMode
from telegram.ext import ContextTypes

from config import Config
from countdown import calculate_countdown
from database import Database
from messages import format_countdown_message

logger = logging.getLogger(__name__)


async def send_daily_countdown(
    context: ContextTypes.DEFAULT_TYPE, is_catchup: bool = False
) -> bool:
    """
    Execute daily countdown posting to the configured group.

    :param context: Telegram ContextTypes instance with bot_data.
    :param is_catchup: True if triggered by post-startup catch-up check.
    :return: True if a message was posted, False otherwise.
    """
    db: Database = context.bot_data["db"]
    cfg: Config = context.bot_data["config"]

    # 1. Verify if bot is paused
    if db.is_paused():
        logger.info("Automatic daily posting skipped: bot is paused.")
        return False

    # 2. Get target group
    group_id = db.get_configured_group_id() or cfg.default_group_id
    if not group_id:
        logger.warning(
            "Automatic daily posting skipped: No group configured. "
            "Use /setgroup in the target group."
        )
        return False

    # 3. Calculate countdown in Africa/Addis_Ababa timezone
    target_date_str = db.get_event_date_str(cfg.event_date_str)
    tz_str = db.get_timezone_str(cfg.timezone_name)
    language = db.get_setting("default_language", cfg.default_language) or "both"

    info = calculate_countdown(target_date_str=target_date_str, timezone_name=tz_str)
    today_str = info.current_datetime.strftime("%Y-%m-%d")

    # 4. Do not post daily countdowns if event is in the past
    if info.is_past:
        logger.info("Event '%s' is in the past. Daily posting completed.", target_date_str)
        return False

    # 5. Prevent duplicate posts on the same calendar day
    if db.has_posted_today(today_str, group_id):
        logger.info(
            "Daily countdown for date %s already sent to chat %s. Skipping duplicate.",
            today_str,
            group_id,
        )
        return False

    # 6. Format message
    message_text = format_countdown_message(info=info, language=language)
    promo_image = db.get_promo_image() or cfg.promo_image_url

    post_type = "milestone" if info.is_milestone else "daily"

    try:
        sent_message = None
        if promo_image:
            try:
                sent_message = await context.bot.send_photo(
                    chat_id=group_id,
                    photo=promo_image,
                    caption=message_text,
                    parse_mode=ParseMode.HTML,
                )
            except Exception as img_err:
                logger.warning(
                    "Failed to send promo photo, falling back to text: %s", img_err
                )

        if sent_message is None:
            sent_message = await context.bot.send_message(
                chat_id=group_id,
                text=message_text,
                parse_mode=ParseMode.HTML,
            )

        message_id = sent_message.message_id if sent_message else None

        # Record in database
        db.record_post(
            post_date=today_str,
            chat_id=group_id,
            days_remaining=info.days_remaining,
            post_type=post_type,
            message_id=message_id,
            status="success",
        )

        if info.is_milestone:
            db.record_milestone_sent(
                days_remaining=info.days_remaining,
                chat_id=group_id,
                message_id=message_id,
            )

        trigger_type = "Catch-up" if is_catchup else "Scheduled"
        logger.info(
            "%s daily countdown posted successfully to chat %s (message_id=%s, days_remaining=%d)",
            trigger_type,
            group_id,
            message_id,
            info.days_remaining,
        )
        return True

    except Exception as exc:
        logger.error(
            "Failed to send daily countdown message to chat %s: %s", group_id, exc
        )
        db.record_post(
            post_date=today_str,
            chat_id=group_id,
            days_remaining=info.days_remaining,
            post_type=post_type,
            status="failed",
            error_message=str(exc),
        )
        return False


async def scheduled_daily_job(context: ContextTypes.DEFAULT_TYPE) -> None:
    """Entry point for python-telegram-bot JobQueue daily schedule."""
    await send_daily_countdown(context, is_catchup=False)


async def check_startup_catchup(context: ContextTypes.DEFAULT_TYPE) -> None:
    """
    Executed a few seconds after bot startup.
    If today's post time has already passed in Ethiopia time and no post has
    been made today, send the post now.
    """
    db: Database = context.bot_data["db"]
    cfg: Config = context.bot_data["config"]

    tz_str = db.get_timezone_str(cfg.timezone_name)
    try:
        tz = ZoneInfo(tz_str)
    except Exception:
        tz = ZoneInfo("Africa/Addis_Ababa")

    now = datetime.now(tz)
    post_time_str = db.get_post_time_str(cfg.post_time_str)
    parts = post_time_str.split(":")
    sched_hour = int(parts[0])
    sched_min = int(parts[1])

    # Check if current time is at or past scheduled post time today
    if (now.hour > sched_hour) or (now.hour == sched_hour and now.minute >= sched_min):
        group_id = db.get_configured_group_id() or cfg.default_group_id
        today_str = now.strftime("%Y-%m-%d")
        if group_id and not db.has_posted_today(today_str, group_id):
            logger.info("Executing catch-up daily countdown post for today (%s)...", today_str)
            await send_daily_countdown(context, is_catchup=True)


def setup_scheduler(job_queue, config: Config, database: Database) -> None:
    """
    Configure JobQueue with daily 09:00 AM Africa/Addis_Ababa schedule and startup check.
    """
    post_time_str = database.get_post_time_str(config.post_time_str)
    parts = post_time_str.split(":")
    post_time = time(int(parts[0]), int(parts[1]), tzinfo=config.tz)

    logger.info(
        "Registering daily job at %s in timezone %s",
        post_time_str,
        config.timezone_name,
    )

    # Register repeating daily job
    job_queue.run_daily(
        scheduled_daily_job,
        time=post_time,
        name="daily_aelafat_countdown",
    )

    # Register one-off catchup check 10 seconds after startup
    job_queue.run_once(
        check_startup_catchup,
        when=10,
        name="startup_aelafat_catchup",
    )
