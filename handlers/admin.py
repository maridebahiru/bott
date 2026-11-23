"""Administrative command handlers for Aelafat Countdown Bot.

Handles authorization, group configuration, status monitoring, manual testing,
and scheduling controls.
"""

import html
import logging
from datetime import datetime
from telegram import Update
from telegram.constants import ChatMemberStatus, ParseMode
from telegram.ext import ContextTypes

from config import Config
from countdown import calculate_countdown
from database import Database
from messages import format_countdown_message

logger = logging.getLogger(__name__)


async def is_user_authorized_admin(
    update: Update, context: ContextTypes.DEFAULT_TYPE
) -> bool:
    """
    Verify whether the requesting user is an authorized administrator.

    Authorized users are:
    1. Users listed in config.BOT_OWNER_ID
    2. Users saved in SQLite admin_users table
    3. Telegram group creators or administrators (when run inside a group)
    """
    user = update.effective_user
    if not user:
        return False

    user_id = user.id
    cfg: Config = context.bot_data["config"]
    db: Database = context.bot_data["db"]

    # 1. Configured bot owners
    if user_id in cfg.owner_ids:
        return True

    # 2. Database registered admins
    if db.is_admin(user_id):
        return True

    # 3. Check group administrator status if inside a group or supergroup
    chat = update.effective_chat
    if chat and chat.type in ("group", "supergroup"):
        try:
            member = await chat.get_member(user_id)
            if member.status in (
                ChatMemberStatus.ADMINISTRATOR,
                ChatMemberStatus.OWNER,
            ):
                return True
        except Exception as exc:
            logger.warning("Error checking chat member status: %s", exc)

    return False


async def setgroup_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle /setgroup command to configure the destination group for daily countdown posts."""
    if not await is_user_authorized_admin(update, context):
        if update.effective_message:
            await update.effective_message.reply_text(
                "⛔ <b>ይቅርታ፣ ይህን ትዕዛዝ ለመጠቀም የአስተዳዳሪ ፈቃድ ያስፈልጋል።</b>\n"
                "<i>Unauthorized: Administrator privileges required.</i>",
                parse_mode=ParseMode.HTML,
            )
        return

    db: Database = context.bot_data["db"]
    chat = update.effective_chat

    # Check if a custom chat ID was provided as an argument: e.g. /setgroup -100123456789
    target_chat_id = None
    target_chat_title = None

    if context.args and len(context.args) > 0:
        try:
            target_chat_id = int(context.args[0])
            target_chat_title = f"Chat ID: {target_chat_id}"
        except ValueError:
            if update.effective_message:
                await update.effective_message.reply_text(
                    "⚠️ እባክዎ ትክክለኛ የቁጥር Chat ID ያስገቡ። ምሳሌ፦ <code>/setgroup -1001234567890</code>",
                    parse_mode=ParseMode.HTML,
                )
            return
    elif chat:
        target_chat_id = chat.id
        target_chat_title = chat.title or f"Chat {chat.id}"

    if target_chat_id is None:
        if update.effective_message:
            await update.effective_message.reply_text(
                "⚠️ ግሩፑን ማግኘት አልተቻለም። እባክዎ በትዕዛዙ ላይ Chat ID ያክሉ።",
                parse_mode=ParseMode.HTML,
            )
        return

    db.set_configured_group_id(target_chat_id)
    logger.info("Configured countdown group set to %s (%s)", target_chat_id, target_chat_title)

    if update.effective_message:
        await update.effective_message.reply_text(
            f"✅ <b>የመለጠፊያ ግሩፕ በተሳካ ሁኔታ ተስተካክሏል!</b>\n\n"
            f"📢 <b>ግሩፕ፦</b> {html.escape(target_chat_title or str(target_chat_id))}\n"
            f"🆔 <b>Group ID፦</b> <code>{target_chat_id}</code>\n\n"
            "ከእንግዲህ እለታዊ የቆጠራ መልእክቶች በየቀኑ በኢትዮጵያ ሰዓት አቆጣጠር ጠዋት 3:00 (09:00 AM) "
            "በዚህ ግሩፕ ውስጥ በራስ-ሰር ይለጠፋሉ።",
            parse_mode=ParseMode.HTML,
        )


async def status_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle /status command: comprehensive overview of bot health and schedule."""
    db: Database = context.bot_data["db"]
    cfg: Config = context.bot_data["config"]

    target_date_str = db.get_event_date_str(cfg.event_date_str)
    tz_str = db.get_timezone_str(cfg.timezone_name)
    post_time_str = db.get_post_time_str(cfg.post_time_str)
    configured_group = db.get_configured_group_id() or cfg.default_group_id
    is_paused = db.is_paused()

    info = calculate_countdown(target_date_str=target_date_str, timezone_name=tz_str)
    last_post = db.get_last_successful_post(configured_group)
    promo_img = db.get_promo_image() or cfg.promo_image_url

    group_display = f"<code>{configured_group}</code>" if configured_group else "<i>አልተዋቀረም (Not Configured)</i>"
    pause_status = "⏸️ <b>ቆሟል (Paused)</b>" if is_paused else "▶️ <b>ንቁ (Active)</b>"
    promo_status = "🖼️ <b>ተዘጋጅቷል (Configured)</b>" if promo_img else "<i>የለም (None)</i>"

    last_post_display = "<i>እስካሁን አልተለጠፈም (None)</i>"
    if last_post:
        last_post_display = (
            f"📅 {last_post['post_date']} ({last_post['days_remaining']} ቀናት ቀርተውት)"
        )

    status_text = (
        "📊 <b>የአእላፋት ቆጣሪ ቦት ሁኔታ / Bot Status</b> 📊\n\n"
        f"🔘 <b>የመርሐግብር ሁኔታ / Schedule:</b> {pause_status}\n"
        f"📅 <b>የበዓሉ ቀን / Event Date:</b> <code>{target_date_str}</code>\n"
        f"⏳ <b>ቀሪ ቀናት / Days Remaining:</b> <b>{info.days_remaining} ቀናት</b>\n"
        f"🌍 <b>የሰዓት ሰቅ / Timezone:</b> <code>{tz_str}</code>\n"
        f"⏰ <b>የመለጠፊያ ሰዓት / Daily Post Time:</b> <code>{post_time_str}</code> (Addis Ababa Time)\n"
        f"📢 <b>የተመረጠው ግሩፕ / Target Group:</b> {group_display}\n"
        f"🖼️ <b>የበዓሉ ምስል / Promo Image:</b> {promo_status}\n"
        f"📬 <b>የመጨረሻው የተለጠፈበት / Last Post:</b> {last_post_display}\n\n"
        "💡 <i>ግሩፑን ለመቀየር በግሩፑ ውስጥ <code>/setgroup</code> ብለው ይጻፉ።</i>"
    )

    if update.effective_message:
        await update.effective_message.reply_text(
            status_text, parse_mode=ParseMode.HTML
        )


async def preview_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle /preview command: preview upcoming daily countdown message."""
    db: Database = context.bot_data["db"]
    cfg: Config = context.bot_data["config"]

    target_date_str = db.get_event_date_str(cfg.event_date_str)
    tz_str = db.get_timezone_str(cfg.timezone_name)
    language = db.get_setting("default_language", cfg.default_language) or "both"

    info = calculate_countdown(target_date_str=target_date_str, timezone_name=tz_str)
    message_text = format_countdown_message(info=info, language=language)

    header = "👁️ <b>የቀጣዩ እለታዊ መልእክት ቅድመ-ዕይታ (Preview):</b>\n━━━━━━━━━━━━━━━━━━━━\n\n"
    full_message = header + message_text

    promo_image = db.get_promo_image() or cfg.promo_image_url

    if update.effective_message:
        if promo_image:
            try:
                await update.effective_message.reply_photo(
                    photo=promo_image,
                    caption=full_message,
                    parse_mode=ParseMode.HTML,
                )
                return
            except Exception:
                pass

        await update.effective_message.reply_text(
            full_message, parse_mode=ParseMode.HTML
        )


async def testpost_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle /testpost command: immediately send a test countdown message to configured group."""
    if not await is_user_authorized_admin(update, context):
        if update.effective_message:
            await update.effective_message.reply_text(
                "⛔ <b>ይቅርታ፣ ይህን ትዕዛዝ ለመጠቀም የአስተዳዳሪ ፈቃድ ያስፈልጋል።</b>\n"
                "<i>Unauthorized: Administrator privileges required.</i>",
                parse_mode=ParseMode.HTML,
            )
        return

    db: Database = context.bot_data["db"]
    cfg: Config = context.bot_data["config"]

    group_id = db.get_configured_group_id() or cfg.default_group_id
    if not group_id:
        if update.effective_message:
            await update.effective_message.reply_text(
                "⚠️ <b>የመለጠፊያ ግሩፕ እስካሁን አልተዋቀረም!</b>\n"
                "እባክዎ መጀመሪያ በግሩፑ ውስጥ <code>/setgroup</code> በማለት ግሩፑን ያስተካክሉ።",
                parse_mode=ParseMode.HTML,
            )
        return

    target_date_str = db.get_event_date_str(cfg.event_date_str)
    tz_str = db.get_timezone_str(cfg.timezone_name)
    language = db.get_setting("default_language", cfg.default_language) or "both"

    info = calculate_countdown(target_date_str=target_date_str, timezone_name=tz_str)
    message_text = format_countdown_message(info=info, language=language)

    promo_image = db.get_promo_image() or cfg.promo_image_url

    try:
        sent_msg = None
        if promo_image:
            try:
                sent_msg = await context.bot.send_photo(
                    chat_id=group_id,
                    photo=promo_image,
                    caption=message_text,
                    parse_mode=ParseMode.HTML,
                )
            except Exception as img_err:
                logger.warning("Failed sending photo in testpost, sending text: %s", img_err)

        if sent_msg is None:
            sent_msg = await context.bot.send_message(
                chat_id=group_id,
                text=message_text,
                parse_mode=ParseMode.HTML,
            )

        # Record test post into database
        today_str = info.current_datetime.strftime("%Y-%m-%d")
        db.record_post(
            post_date=today_str,
            chat_id=group_id,
            days_remaining=info.days_remaining,
            post_type="test",
            message_id=sent_msg.message_id if sent_msg else None,
            status="success",
        )

        if update.effective_message:
            await update.effective_message.reply_text(
                f"✅ <b>የሙከራ መልእክት በተሳካ ሁኔታ ወደ ግሩፑ ተልኳል!</b>\n"
                f"Target Group ID: <code>{group_id}</code>\n"
                f"Message ID: <code>{sent_msg.message_id}</code>",
                parse_mode=ParseMode.HTML,
            )
    except Exception as exc:
        logger.error("Failed to send testpost to %s: %s", group_id, exc)
        if update.effective_message:
            await update.effective_message.reply_text(
                f"❌ <b>መልእክቱን ወደ ግሩፑ መላክ አልተቻለም።</b>\n"
                f"የስህተት ዝርዝር፦ <code>{html.escape(str(exc))}</code>\n\n"
                "<i>እባክዎ ቦቱ በግሩፑ ውስጥ መኖሩንና መልእክት የመጻፍ ፈቃድ (Administrator) እንዳለው ያረጋግጡ።</i>",
                parse_mode=ParseMode.HTML,
            )


async def pause_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle /pause command: pause scheduled daily postings."""
    if not await is_user_authorized_admin(update, context):
        if update.effective_message:
            await update.effective_message.reply_text(
                "⛔ <b>ይቅርታ፣ ይህን ትዕዛዝ ለመጠቀም የአስተዳዳሪ ፈቃድ ያስፈልጋል።</b>",
                parse_mode=ParseMode.HTML,
            )
        return

    db: Database = context.bot_data["db"]
    db.set_paused(True)
    logger.info("Automatic countdown messages paused by user %s", update.effective_user)

    if update.effective_message:
        await update.effective_message.reply_text(
            "⏸️ <b>እለታዊ ራስ-ሰር የቆጠራ መልእክቶች ቆመዋል (Paused)።</b>\n"
            "እንደገና ለማስጀመር <code>/resume</code> የሚለውን ትዕዛዝ ይጠቀሙ።",
            parse_mode=ParseMode.HTML,
        )


async def resume_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle /resume command: resume scheduled daily postings."""
    if not await is_user_authorized_admin(update, context):
        if update.effective_message:
            await update.effective_message.reply_text(
                "⛔ <b>ይቅርታ፣ ይህን ትዕዛዝ ለመጠቀም የአስተዳዳሪ ፈቃድ ያስፈልጋል።</b>",
                parse_mode=ParseMode.HTML,
            )
        return

    db: Database = context.bot_data["db"]
    db.set_paused(False)
    logger.info("Automatic countdown messages resumed by user %s", update.effective_user)

    if update.effective_message:
        await update.effective_message.reply_text(
            "▶️ <b>እለታዊ ራስ-ሰር የቆጠራ መልእክቶች እንደገና ቀጥለዋል (Resumed)።</b>\n"
            "መልእክቶች በየቀኑ በኢትዮጵያ ሰዓት አቆጣጠር ጠዋት 3:00 (09:00 AM) ይለጠፋሉ።",
            parse_mode=ParseMode.HTML,
        )


async def setdate_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle /setdate command to dynamically change the event date without editing code."""
    if not await is_user_authorized_admin(update, context):
        if update.effective_message:
            await update.effective_message.reply_text(
                "⛔ <b>የአስተዳዳሪ ፈቃድ ያስፈልጋል።</b>", parse_mode=ParseMode.HTML
            )
        return

    if not context.args or len(context.args) == 0:
        if update.effective_message:
            await update.effective_message.reply_text(
                "⚠️ እባክዎ ቀኑን በ YYYY-MM-DD ፎርማት ያስገቡ። ምሳሌ፦ <code>/setdate 2027-01-05</code>",
                parse_mode=ParseMode.HTML,
            )
        return

    new_date_str = context.args[0].strip()
    try:
        datetime.strptime(new_date_str, "%Y-%m-%d")
    except ValueError:
        if update.effective_message:
            await update.effective_message.reply_text(
                "❌ ልክ ያልሆነ የቀን ፎርማት! እባክዎ በ YYYY-MM-DD ያስገቡ። ምሳሌ፦ <code>/setdate 2027-01-05</code>",
                parse_mode=ParseMode.HTML,
            )
        return

    db: Database = context.bot_data["db"]
    db.set_event_date_str(new_date_str)

    if update.effective_message:
        await update.effective_message.reply_text(
            f"✅ <b>የበዓሉ ቀን በተሳካ ሁኔታ ተቀይሯል!</b>\n"
            f"አዲሱ ቀን፦ <code>{new_date_str}</code>",
            parse_mode=ParseMode.HTML,
        )


async def settime_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle /settime command to change daily posting time (HH:MM in Africa/Addis_Ababa)."""
    if not await is_user_authorized_admin(update, context):
        if update.effective_message:
            await update.effective_message.reply_text(
                "⛔ <b>የአስተዳዳሪ ፈቃድ ያስፈልጋል።</b>", parse_mode=ParseMode.HTML
            )
        return

    if not context.args or len(context.args) == 0:
        if update.effective_message:
            await update.effective_message.reply_text(
                "⚠️ እባክዎ ሰዓቱን በ 24-ሰዓት HH:MM ፎርማት ያስገቡ። ምሳሌ፦ <code>/settime 09:00</code>",
                parse_mode=ParseMode.HTML,
            )
        return

    time_str = context.args[0].strip()
    try:
        parts = time_str.split(":")
        h, m = int(parts[0]), int(parts[1])
        if not (0 <= h < 24 and 0 <= m < 60):
            raise ValueError
    except Exception:
        if update.effective_message:
            await update.effective_message.reply_text(
                "❌ ልክ ያልሆነ የሰዓት ፎርማት! እባክዎ በ 00:00 እስከ 23:59 መካከል ያስገቡ።",
                parse_mode=ParseMode.HTML,
            )
        return

    db: Database = context.bot_data["db"]
    db.set_post_time_str(time_str)

    if update.effective_message:
        await update.effective_message.reply_text(
            f"✅ <b>የመለጠፊያ ሰዓት በተሳካ ሁኔታ ተቀይሯል!</b>\n"
            f"አዲሱ ሰዓት፦ <code>{time_str}</code> (የኢትዮጵያ ሰዓት አቆጣጠር)",
            parse_mode=ParseMode.HTML,
        )


async def setimage_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle /setimage command to set or clear promotional image URL."""
    if not await is_user_authorized_admin(update, context):
        if update.effective_message:
            await update.effective_message.reply_text(
                "⛔ <b>የአስተዳዳሪ ፈቃድ ያስፈልጋል።</b>", parse_mode=ParseMode.HTML
            )
        return

    db: Database = context.bot_data["db"]

    if not context.args or len(context.args) == 0:
        # Clear image
        db.set_promo_image(None)
        if update.effective_message:
            await update.effective_message.reply_text(
                "🗑️ <b>የበዓሉ ምስል ተሰርዟል። መልእክቶች በጽሑፍ ብቻ ይለጠፋሉ።</b>",
                parse_mode=ParseMode.HTML,
            )
        return

    image_url = context.args[0].strip()
    db.set_promo_image(image_url)

    if update.effective_message:
        await update.effective_message.reply_text(
            f"✅ <b>የበዓሉ ምስል በተሳካ ሁኔታ ተቀምጧል!</b>\n"
            f"Image URL: <code>{html.escape(image_url)}</code>",
            parse_mode=ParseMode.HTML,
        )
