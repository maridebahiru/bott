"""Start command handler for Aelafat Countdown Bot."""

from telegram import Update
from telegram.constants import ParseMode
from telegram.ext import ContextTypes


async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle /start command with a warm, reverent welcome message."""
    user = update.effective_user
    first_name = user.first_name if user else "ወዳጃችን"

    welcome_text = (
        f"✝️ <b>እንኳን ወደ የአእላፋት ዝማሬ ቆጣሪ ቦት በደህና መጡ!</b> ✝️\n"
        f"<i>Welcome {first_name} to the Aelafat Zimare Countdown Bot!</i>\n\n"
        "🕊️ ይህ ቦት ለታላቁ መንፈሳዊ ጉባኤ <b>«የአእላፋት ዝማሬ»</b> የተዘጋጀ ይፋዊ የቆጠራ ቦት ነው።\n"
        "በየእለቱ ጠዋት 3:00 (9:00 AM) የደስታ እና የበረከት መልእክቶችን ወደ ግሩፓችን ያደርሳል።\n\n"
        "📌 <b>ዋና ዋና ትዕዛዛት / Main Commands:</b>\n"
        "• /countdown - የቀረውን ትክክለኛ ጊዜ አሁኑኑ ይመልከቱ\n"
        "• /preview - የቀጣዩን እለታዊ መልእክት ቅድመ-ዕይታ ይመልከቱ\n"
        "• /about - ስለ ዝግጅቱ እና አዘጋጆች ዝርዝር መረጃ\n"
        "• /help - የትዕዛዛት ዝርዝር መመሪያ\n"
        "• /status - የቦቱን እና የቆጠራውን ሁኔታ ይመልከቱ\n\n"
        "<i>«እግዚአብሔርን በደስታ እና በዝማሬ እናመስግነው!»</i>\n\n"
        "✨ <b>January 5, 2027</b> በናፍቆት እንጠብቅ!"
    )

    if update.effective_message:
        await update.effective_message.reply_text(
            welcome_text, parse_mode=ParseMode.HTML
        )
