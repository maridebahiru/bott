"""About and Help command handlers for Aelafat Countdown Bot."""

from telegram import Update
from telegram.constants import ParseMode
from telegram.ext import ContextTypes


async def about_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle /about command: provides context on the Aelafat Zimare event."""
    about_text = (
        "✨ <b>የአእላፋት ዝማሬ (Aelafat Zimare)</b> ✨\n\n"
        "🕊️ <b>የዝግጅቱ ዓላማ / Purpose:</b>\n"
        "የአእላፋት ዝማሬ በኢትዮጵያ ኦርቶዶክስ ተዋሕዶ ቤተክርስቲያን መንፈሳዊ ሥርዓት መሠረት "
        "በአንድ ልብ እና በአንድ ቃል ሆነን ፈጣሪያችንን በዝማሬ፣ በምስጋና እና በጸሎት "
        "የምናከብርበት ታላቅ እና ታሪካዊ መንፈሳዊ ጉባኤ ነው።\n\n"
        "📅 <b>ቀን / Date:</b> January 5, 2027 (ታህሳስ 27 ቀን)\n"
        "🌍 <b>ቦታ / Timezone:</b> አዲስ አበባ፣ ኢትዮጵያ (Africa/Addis_Ababa, UTC+3)\n"
        "🎵 <b>ተሳታፊዎች:</b> በርካታ የመዘምራን አባላት፣ አባቶች፣ ካህናት እና ምዕመናን በአንድነት\n\n"
        "<i>«አእላፋት» ማለት እልፍ አእላፍ፣ ቁጥር የሌላቸው ምእመናን እና መላእክት "
        "በአንድነት ለእግዚአብሔር ክብር የሚሰጡበትን ሰማያዊ ምስጋና ያመለክታል።</i>\n\n"
        "❤️ <b>ሁላችሁም ተጋብዛችኋል!</b>"
    )

    if update.effective_message:
        await update.effective_message.reply_text(
            about_text, parse_mode=ParseMode.HTML
        )


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Handle /help command: list public and admin commands."""
    help_text = (
        "📖 <b>የቦቱ የትዕዛዛት ዝርዝር / Available Commands</b>\n\n"
        "<b>የህዝብ ትዕዛዛት / Public Commands:</b>\n"
        "• /start - የቦቱ መግቢያ እና ሰላምታ\n"
        "• /countdown - የቀረውን ትክክለኛ የቆጠራ ጊዜ ማሳያ\n"
        "• /preview - የቀጣዩን ቀን መልእክት አስቀድሞ ማየት\n"
        "• /about - ስለ «የአእላፋት ዝማሬ» ዝግጅት መረጃ\n"
        "• /help - ይህን የእርዳታ መመሪያ ማሳያ\n\n"
        "<b>የአስተዳዳሪ ትዕዛዛት / Admin Commands:</b>\n"
        "• /setgroup - መልእክቱ የሚለጠፍበትን ግሩፕ መወሰኛ\n"
        "• /status - የቦቱን እና የጊዜ ሰሌዳውን ሁኔታ መመልከቻ\n"
        "• /testpost - የሙከራ መልእክት ወደ ግሩፑ መላኪያ\n"
        "• /pause - እለታዊ መልእክቶችን ማቆሚያ\n"
        "• /resume - እለታዊ መልእክቶችን ማስቀጠያ\n"
        "• /setdate [YYYY-MM-DD] - የበዓሉን ቀን ማስተካከያ\n"
        "• /settime [HH:MM] - የሚለጠፍበትን ሰዓት ማስተካከያ\n"
        "• /setimage [URL] - የበዓሉን ምስል ማስተካከያ"
    )

    if update.effective_message:
        await update.effective_message.reply_text(
            help_text, parse_mode=ParseMode.HTML
        )
