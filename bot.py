"""Aelafat Countdown Telegram Bot.

Production-ready Telegram countdown bot for የአእላፋት ዝማሬ (Aelafat Zimare).
Calculates and announces daily countdown messages in Africa/Addis_Ababa timezone.
"""

import logging
import sys
from telegram import Update
from telegram.ext import (
    Application,
    ApplicationBuilder,
    CommandHandler,
    ContextTypes,
)

from config import Config, get_config
from database import Database
from handlers.about import about_command, help_command
from handlers.admin import (
    pause_command,
    preview_command,
    resume_command,
    setdate_command,
    setgroup_command,
    setimage_command,
    settime_command,
    status_command,
    testpost_command,
)
from handlers.countdown import countdown_command
from handlers.start import start_command
from scheduler import setup_scheduler


def setup_logging(log_level: str = "INFO") -> None:
    """Configure structured logging."""
    logging.basicConfig(
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        level=getattr(logging, log_level, logging.INFO),
        handlers=[
            logging.StreamHandler(sys.stdout),
        ],
    )
    # Silence noisy HTTP connection logs
    logging.getLogger("httpx").setLevel(logging.WARNING)
    logging.getLogger("httpcore").setLevel(logging.WARNING)


async def global_error_handler(update: object, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Log errors caused by Updates securely without leaking secrets."""
    logger = logging.getLogger("AelafatBot.ErrorHandler")
    logger.error("Exception while handling an update:", exc_info=context.error)

    if isinstance(update, Update) and update.effective_message:
        try:
            await update.effective_message.reply_text(
                "⚠️ <b>አንድ ችግር አጋጥሟል! እባክዎ ጥቂት ቆይተው እንደገና ይሞክሩ።</b>\n"
                "<i>An internal error occurred. Please try again shortly.</i>",
                parse_mode="HTML",
            )
        except Exception:
            pass


def main() -> None:
    """Main application entry point."""
    config = get_config()
    setup_logging(config.log_level)
    logger = logging.getLogger("AelafatBot")

    logger.info("Initializing Aelafat Countdown Bot...")

    if not config.bot_token:
        logger.critical(
            "FATAL: TELEGRAM_BOT_TOKEN is not configured! "
            "Please create a .env file based on .env.example with your bot token."
        )
        sys.exit(1)

    # Initialize persistent SQLite Database
    db = Database(config.database_path)

    # Seed owners as admins if provided
    for owner_id in config.owner_ids:
        db.add_admin(owner_id, username="BotOwner")

    # Build Telegram Bot Application
    application: Application = (
        ApplicationBuilder()
        .token(config.bot_token)
        .concurrent_updates(True)
        .build()
    )

    # Store shared dependencies in bot_data
    application.bot_data["config"] = config
    application.bot_data["db"] = db

    # Register Public Commands
    application.add_handler(CommandHandler("start", start_command))
    application.add_handler(CommandHandler("countdown", countdown_command))
    application.add_handler(CommandHandler("preview", preview_command))
    application.add_handler(CommandHandler("about", about_command))
    application.add_handler(CommandHandler("help", help_command))

    # Register Admin Commands
    application.add_handler(CommandHandler("setgroup", setgroup_command))
    application.add_handler(CommandHandler("status", status_command))
    application.add_handler(CommandHandler("testpost", testpost_command))
    application.add_handler(CommandHandler("pause", pause_command))
    application.add_handler(CommandHandler("resume", resume_command))
    application.add_handler(CommandHandler("setdate", setdate_command))
    application.add_handler(CommandHandler("settime", settime_command))
    application.add_handler(CommandHandler("setimage", setimage_command))

    # Register Error Handler
    application.add_error_handler(global_error_handler)

    # Setup JobQueue Scheduler if job queue is available
    if application.job_queue:
        setup_scheduler(application.job_queue, config, db)
    else:
        logger.warning(
            "JobQueue is not initialized! Ensure python-telegram-bot[job-queue] is installed."
        )

    logger.info("Aelafat Countdown Bot started successfully. Listening for events...")

    # Start Polling
    application.run_polling(
        allowed_updates=Update.ALL_TYPES,
        drop_pending_updates=True,
    )


if __name__ == "__main__":
    main()
