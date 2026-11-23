"""Countdown command handler for Aelafat Countdown Bot."""

from telegram import Update
from telegram.constants import ParseMode
from telegram.ext import ContextTypes
from config import Config
from countdown import calculate_countdown
from database import Database
from messages import format_countdown_message


async def countdown_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle /countdown command: calculate and display live countdown details."""
    db: Database = context.bot_data["db"]
    cfg: Config = context.bot_data["config"]

    target_date_str = db.get_event_date_str(cfg.event_date_str)
    tz_str = db.get_timezone_str(cfg.timezone_name)
    language = db.get_setting("default_language", cfg.default_language) or "both"

    info = calculate_countdown(target_date_str=target_date_str, timezone_name=tz_str)
    message_text = format_countdown_message(info=info, language=language)

    # Append live exact hours/minutes counter if in future
    if not info.is_event_day and not info.is_past:
        extra_counter = (
            f"\n\n⏱️ <b>ትክክለኛ ሰዓት ቆጣሪ / Exact Timer:</b>\n"
            f"<code>{info.days_remaining} ቀናት (Days) : "
            f"{info.hours_remaining} ሰዓታት (Hours) : "
            f"{info.minutes_remaining} ደቂቃዎች (Mins)</code>"
        )
        message_text += extra_counter

    promo_image = db.get_promo_image() or cfg.promo_image_url

    if update.effective_message:
        if promo_image:
            try:
                await update.effective_message.reply_photo(
                    photo=promo_image,
                    caption=message_text,
                    parse_mode=ParseMode.HTML,
                )
                return
            except Exception:
                # If image fails to load or send, fallback gracefully to text
                pass

        await update.effective_message.reply_text(
            message_text, parse_mode=ParseMode.HTML
        )
