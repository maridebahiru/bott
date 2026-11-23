"""Message generator and spiritual reflections collection for Aelafat Countdown Bot.

Crafted with Ethiopian Orthodox Christian reverence, spiritual joy, and bilingual support.
Contains over 30 verified Amharic motivational reflections on mezmur, praise, and unity.
"""

import html
from typing import Optional
from countdown import CountdownInfo

# ---------------------------------------------------------------------------
# 35+ Authentic Amharic Reflections on Praise, Mezmur, Unity & Spiritual Joy
# ---------------------------------------------------------------------------
DAILY_REFLECTIONS_AMHARIC = [
    "በአንድ ልብ ሆነን ፈጣሪያችንን በዝማሬ እና በምስጋና የምናከብርበት የተባረከ ቀን እየቀረበ ነው!",
    "ዝማሬ የልብ ጸሎት፣ የነፍስ ምስጋና ነው፤ ለእለተ በዓሉ ልባችንን በንጽህና እናዘጋጅ።",
    "እግዚአብሔርን በቅድስናው ስፍራ ማመስገን ታላቅ ክብር እና በረከት ነው፤ ቀናቱን በደስታ እንጠብቅ!",
    "የአእላፋት ዝማሬ—በሰማያዊ ህብረት የእግዚአብሔርን ታላቅነት በጋራ የምናውጅበት ድንቅ መድረክ ነው።",
    "ምስጋና ለሚገባው አምላክ ክብርን እንስጥ፤ በደስታ እና በዝማሬ ወደ አደባባዩ ለመድረስ እንዘጋጅ።",
    "መንፈሳዊ ዝማሬ ልብን ያረጋጋል፣ ነፍስንም በሰማያዊ ጸጋ ይሞላል፤ ቀናችንን በምስጋና እንጀምር።",
    "የአባቶቻችን እና የእናቶቻችን የቅዳሴ እና የዝማሬ ውርስ በልባችን ያበራል፤ ያ ታላቅ ቀን እየቀረበ ነው።",
    "በፍቅር እና በአንድነት ሆነን ዝማሬያችንን ወደ ሰማያት የምናሳርግበት ልዩ ቀን ይጠብቀናል።",
    "ለእግዚአብሔር ምስጋናን ማቅረብ የሕይወታችን ታላቁ ደስታ ነው፤ በዝግጅት እና በጸሎት እንጠብቅ።",
    "የአእላፋት ማኅበር በአንድ ቃል ድምፁን ከፍ አድርጎ ጌታውን የሚያመሰግንበት ሰዓት እየደረሰ ነው።",
    "ከልብ የሚወጣ ምስጋና በሰማይ ተቀባይነት አለው፤ ነፍሳችን በዝማሬው ረቂቅ ጸጋ እንድትታደስ እንመኛለን።",
    "የመዝሙር ድምፅ ሰላምን ያወርሳል፣ ልብን ያስደስታል፤ ይህን የተቀደሰ ጉባኤ በጉጉት እንጠብቃለን።",
    "በደስታ እና በእልልታ የአምላካችንን ቸርነት የምናወድስበት ታላቅ መድረክ ተዘጋጅቷል!",
    "የአእላፋት ዝማሬ የፍቅር፣ የህብረት እና የበረከት ማዕድ ነው፤ ሁላችንም በጸሎት እንዘጋጅ።",
    "ስለ ተደረገልን ቸርነት ሁሉ ምስጋና ይገባል፤ በዝማሬ ወደ እግዚአብሔር ቤት ለመግባት ቀናት ቀርተዋል።",
    "የነፍስ እረፍት በዝማሬ እና በጸሎት ውስጥ ይገኛል፤ ያንን የተባረከ ቀን በናፍቆት እንጠባበቃለን።",
    "በቅዱሳን አምላክ ፊት ቆመን ምስጋናን ማቅረብ መታደል ነው፤ በደስታ እና በቅን ልብ እንጠብቅ።",
    "የአእላፋት ዝማሬ የመንፈሳዊ አንድነታችን መገለጫ ነው፤ እግዚአብሔር ጉባኤያችንን ይባርክልን።",
    "በበገና፣ በመሰንቆ፣ በጸናጽል እና በከበሮ የታጀበውን ያማረ ዝማሬ የምናደምጥበት ሰዓት ቀርቧል።",
    "ለታላቁ ጉባኤ ልባችንን በይቅርታ፣ በሰላም እና በንጹሕ ፍቅር እናዘጋጅ።",
    "ዝማሬያችን ወደ ዙፋኑ ደርሶ የተወደደ መሥዋዕት እንዲሆን በጸሎት እንትጋ።",
    "የአእላፋት ቅዱሳን ማኅበር ተሰብስበው የሚዘምሩት ዝማሬ በልባችን መንፈሳዊ ብርሃንን ያበራል።",
    "እግዚአብሔርን ማመስገን ከሁሉ የላቀ ሥራ ነው፤ ቀኑ እስኪደርስ በጉጉት እና በምስጋና እንጠብቅ።",
    "የተመረቀ እና የተባረከ ቀን እንዲሆንልን ሁላችንም በጸሎት እናስብ።",
    "የደስታ እና የምስጋና ድምፅ በቤተክርስቲያናችን አደባባይ የሚሞላበት ታላቁ ቀን እየቀረበ ነው።",
    "የአእላፋት ድምፅ በአንድ ላይ ሲስተጋባ ታላቅ ሰማያዊ ጸጋ ይወርዳል፤ በደስታ እንጠባበቅ!",
    "ለፈጣሪያችን ክብርንና ምስጋናን የምናቀርብበት ሰዓት ጥቂት ቀናት ብቻ ቀርተውታል።",
    "በመልካም ዝግጅት እና በደስታ ልብ ያንን የተቀደሰ ቀን በጋራ እንቀበል።",
    "ዝማሬ የነፍስ ምግብ፣ የህሊና ብርሃን ነው፤ የተባረከ የመንፈስ ጉባኤ ይሁንልን።",
    "የአእላፋት ዝማሬ ታላቁ መንፈሳዊ ጉባኤ በሰላም እና በፍቅር እንዲጠናቀቅ በጸሎት እንቁም።",
    "በአንድነት ተሰብስበን ስሙን የምንቀድስበት፣ ክብሩን የምንገልጽበት ቀን እየቀረበ ነው!",
    "በእግዚአብሔር ፊት የቀረበ እውነተኛ ምስጋና በረከትን ያዘንባል፤ በጉጉት እንጠብቅ!",
    "የአእላፋት መዘምራን ድምፅ ከመላእክት ምስጋና ጋር የሚተባበርበት ድንቅ ቀን ደርሷል።",
    "በፍቅር፣ በትህትና እና በደስታ ወደ አምላካችን አደባባይ የምንገባበት ጊዜ አሁን ነው።",
    "የአእላፋት ዝማሬ የደስታችን፣ የተስፋችን እና የጽናታችን ማሳያ ነው፤ እንኳን አደረሳችሁ!",
]

DAILY_REFLECTIONS_ENGLISH = [
    "The blessed day of gathering in unity and praise is approaching!",
    "Hymns are prayers of the heart; let us prepare our hearts in holiness.",
    "Praising the Almighty in unity brings immense spiritual joy and blessings.",
    "Aelafat Zimare—a heavenly assembly to magnify the Lord's greatness together.",
    "Let us offer gratitude to the Creator and await the joyful day with hope.",
    "Sacred hymns bring tranquility to our spirits and divine grace to our lives.",
    "The sacred heritage of hymn and praise shines brightly as the great day nears.",
    "A unique day to lift our voices to the heavens in genuine love and fellowship.",
    "Giving thanks is our highest calling; let us prepare in prayer and devotion.",
    "The moment when thousands unite in one voice to praise the Almighty is coming.",
    "Praise originating from a pure heart finds grace before God's heavenly throne.",
    "The resonance of spiritual hymns brings profound peace and radiant happiness.",
    "A monumental platform prepared to magnify God's goodness with triumph and joy!",
    "Aelafat Zimare is a banquet of faith, fellowship, and divine blessings.",
    "Countless blessings deserve heartfelt thanksgiving; days remain to gather in praise.",
    "Spiritual sanctuary and peace are discovered in heartfelt hymns and prayer.",
    "Standing together before the Almighty to give praise is a sacred privilege.",
    "Aelafat Zimare embodies our collective spiritual unity; may God bless this assembly.",
    "The resonant rhythm of traditional Ethiopian sacred instruments will soon echo.",
    "Let us adorn our hearts with forgiveness, peace, and love for this great gathering.",
    "May our hymns ascend as an acceptable, pleasing incense before the throne.",
    "The unified hymns of thousands will illuminate our souls with celestial light.",
    "Praising God is the finest work of life; let us wait with spiritual joy.",
    "May this forthcoming assembly be fruitful, blessed, and full of grace.",
    "The festive day when hymns of rejoicing fill the gathering place is almost here.",
    "When thousands lift up their voices together, abundant heavenly grace descends.",
    "Only a little time remains before we gather to give honor and Thanksgiving.",
    "Let us welcome this sanctified day with joyous hearts and diligent preparation.",
    "Spiritual mezmur is nourishment for the soul and light for the conscience.",
    "May Aelafat Zimare conclude in lasting peace, mutual love, and divine grace.",
    "The hour draws near to convene as one and sanctify His glorious name!",
    "Pure praise poured out before the Creator brings everlasting blessing.",
    "A wonderful day where voices of thousands join in celestial harmony.",
    "Now is the season to approach God's sanctuary with humility, reverence, and joy.",
    "Aelafat Zimare is a testament to our enduring faith, hope, and joy!",
]


# ---------------------------------------------------------------------------
# Milestone Messages
# ---------------------------------------------------------------------------
MILESTONE_MESSAGES = {
    30: {
        "am": (
            "🌟 <b>ልዩ ማስታወቂያ: 30 ቀናት (1 ወር) ብቻ ቀሩን!</b> 🌟\n\n"
            "የአእላፋት ዝማሬ ታላቁ መንፈሳዊ ጉባኤ ሊደርስ የቀረው አንድ ወር ብቻ ነው!\n"
            "በመዝሙር፣ በምስጋና እና በሰማያዊ ደስታ የምንሰበሰብበት ሰዓት በፍጥነት እየቀረበ ነው።\n"
            "ልባችንን በፍቅር እና በዝግጅት እናንጻ!"
        ),
        "en": (
            "🌟 <b>Milestone: Exactly 30 Days (1 Month) Remaining!</b> 🌟\n\n"
            "Only one month remains until the historic Aelafat Zimare spiritual gathering!\n"
            "The hour to unite in hymns, thanksgiving, and heavenly joy is fast approaching."
        ),
    },
    14: {
        "am": (
            "⏳ <b>ልዩ ማስታወቂያ: 14 ቀናት (2 ሳምንታት) ብቻ ቀሩን!</b> ⏳\n\n"
            "ቀናቱ እየተቆጠሩ ሁለት ሳምንታት ብቻ ቀርተውናል!\n"
            "የአእላፋት ድምፅ በአንድነት የሚያስተጋባበት ታላቅ ቀን በደጃችን ደርሷል።\n"
            "ሁላችንም በጸሎት እና በናፍቆት እንዘጋጅ!"
        ),
        "en": (
            "⏳ <b>Milestone: Exactly 14 Days (2 Weeks) Remaining!</b> ⏳\n\n"
            "The countdown reaches just two weeks!\n"
            "The grand occasion where thousands lift their voices together is right at our doorstep."
        ),
    },
    7: {
        "am": (
            "🔔 <b>ልዩ ማስታወቂያ: 7 ቀናት (1 ሳምንት) ብቻ ቀሩን!</b> 🔔\n\n"
            "የመጨረሻው ሳምንት ቆጠራ ተጀምሯል!\n"
            "የአእላፋት ዝማሬ ታላቁ ቀን ሊደርስ 7 ቀናት ብቻ ቀሩት።\n"
            "በሰማያዊ ዝማሬ አምላካችንን ለማመስገን ዝግጁ ናችሁን?"
        ),
        "en": (
            "🔔 <b>Milestone: Just 7 Days (1 Week) Remaining!</b> 🔔\n\n"
            "The final week countdown has begun!\n"
            "Only 7 days remain until Aelafat Zimare begins.\n"
            "Are you ready to join in heavenly praise?"
        ),
    },
    3: {
        "am": (
            "🔥 <b>ልዩ ማስታወቂያ: 3 ቀናት ብቻ ቀሩን!</b> 🔥\n\n"
            "የቆጠራው ማብቂያ ተቃርቧል—3 ቀናት ብቻ!\n"
            "የመንፈስ ደስታችን፣ የጋራ ዝማሬያችን ወደ መፈጸሙ እየደረሰ ነው።\n"
            "በእልልታ እና በጉጉት እንጠብቅ!"
        ),
        "en": (
            "🔥 <b>Milestone: Only 3 Days Left!</b> 🔥\n\n"
            "The final stretch is here—just 3 days!\n"
            "Our collective spiritual joy and hymns are almost upon us.\n"
            "Let us rejoice in anticipation!"
        ),
    },
    2: {
        "am": (
            "⚡ <b>ልዩ ማስታወቂያ: 2 ቀናት ብቻ ቀሩን!</b> ⚡\n\n"
            "ቀናቱ አለቁ—ከበዓሉ መድረክ የቀረን 2 ቀናት ብቻ!\n"
            "ሁላችሁም ወዳጆቻችሁን ጋብዙ፤ የታላቁ ጉባኤ ተሳታፊ እንሁን!"
        ),
        "en": (
            "⚡ <b>Milestone: Only 2 Days Remaining!</b> ⚡\n\n"
            "Almost there—only 2 days remain!\n"
            "Invite your loved ones to partake in this historic day of worship and fellowship!"
        ),
    },
    1: {
        "am": (
            "🌅 <b>ልዩ ማስታወቂያ: ነገ ነው! 1 ቀን ብቻ ቀረን!</b> 🌅\n\n"
            "የናፈቅነው፣ የጠበቅነው ታላቁ የአእላፋት ዝማሬ ነገ ይካሄዳል!\n"
            "እግዚአብሔር በቸርነቱ ያደረሰን ይህን የተባረከ ቀን በደስታ እና በምስጋና እንቀበል።\n"
            "ነገ በዝማሬ አደባባይ እንገናኝ!"
        ),
        "en": (
            "🌅 <b>Milestone: Tomorrow is the Day! 1 Day Left!</b> 🌅\n\n"
            "The day we prayed and longed for arrives tomorrow!\n"
            "God in His infinite mercy has brought us to this blessed threshold.\n"
            "See you tomorrow at the sacred gathering of Aelafat Zimare!"
        ),
    },
    0: {
        "am": (
            "🎉✨ <b>ዛሬ ታላቁ ቀን የአእላፋት ዝማሬ ደረሰ!</b> ✨🎉\n\n"
            "✝️ <i>«በእልልታና በዝማሬ ወደ አምላካችን አደባባይ እንግባ!»</i>\n\n"
            "የምንናፍቀው፣ የምንጠብቀው ታላቁ መንፈሳዊ ጉባኤ ዛሬ ደርሷል!\n"
            "የአእላፋት ድምፅ ወደ ሰማያት የሚረግበት፣ በምስጋና እና በፍቅር የምንሞላበት ቀን ዛሬ ነው!\n\n"
            "🕊️ <b>የተባረከ እና የተቀደሰ የበዓል ቀን ይሁንልን! መልካም የአእላፋት ዝማሬ!</b>"
        ),
        "en": (
            "🎉✨ <b>Today is the Glorious Day of Aelafat Zimare!</b> ✨🎉\n\n"
            "✝️ <i>\"Enter into His presence with singing and thanksgiving!\"</i>\n\n"
            "The sacred spiritual assembly we have eagerly anticipated is finally here today!\n"
            "May thousands of voices ascend together in worship, love, and spiritual triumph!\n\n"
            "🕊️ <b>Wishing everyone a deeply blessed and joyful Aelafat Zimare!</b>"
        ),
    },
}


def get_daily_reflection(days_remaining: int) -> tuple[str, str]:
    """
    Get a deterministic, daily-rotating motivational reflection based on days_remaining
    so messages stay fresh and don't repeat consecutively.
    """
    index = abs(days_remaining) % len(DAILY_REFLECTIONS_AMHARIC)
    return (
        DAILY_REFLECTIONS_AMHARIC[index],
        DAILY_REFLECTIONS_ENGLISH[index],
    )


def format_countdown_message(
    info: CountdownInfo,
    language: str = "both",
    event_name: str = "የአእላፋት ዝማሬ",
    custom_reflection: Optional[str] = None,
) -> str:
    """
    Build a beautifully styled Telegram HTML countdown message.

    :param info: CountdownInfo dataclass.
    :param language: "am" (Amharic), "en" (English), or "both" (Bilingual).
    :param event_name: Display title for the event.
    :param custom_reflection: Optional custom reflection text.
    """
    event_date_display = info.target_datetime.strftime("%B %d, %Y")

    # 1. Past Event Handling
    if info.is_past:
        if language == "en":
            return (
                f"✨ <b>{html.escape(event_name)} (Aelafat Zimare)</b> ✨\n\n"
                f"🙏 <i>The sacred event took place on {event_date_display}.</i>\n\n"
                "❤️ May the spiritual blessings and peace of the hymns remain with us all!"
            )
        elif language == "am":
            return (
                f"✨ <b>{html.escape(event_name)}</b> ✨\n\n"
                f"🙏 <i>ይህ ታላቅ መንፈሳዊ ጉባኤ በ{event_date_display} በታላቅ በረከት ተከናውኗል!</i>\n\n"
                "❤️ የእግዚአብሔር በረከት፣ ሰላም እና ፍቅር ከሁላችን ጋር ይሁን።"
            )
        else:
            return (
                f"✨ <b>{html.escape(event_name)} (Aelafat Zimare)</b> ✨\n\n"
                f"🙏 <i>ይህ ታላቅ መንፈሳዊ ጉባኤ በ{event_date_display} በታላቅ በረከት ተከናውኗል!</i>\n"
                f"<i>The sacred gathering took place on {event_date_display} with great blessings.</i>\n\n"
                "❤️ የእግዚአብሔር በረከት ከሁላችን ጋር ይሁን! / May God's peace abide with all of us!"
            )

    # 2. Event Day Celebration Handling
    if info.is_event_day:
        celebration = MILESTONE_MESSAGES[0]
        if language == "am":
            return celebration["am"]
        elif language == "en":
            return celebration["en"]
        else:
            return f"{celebration['am']}\n\n━━━━━━━━━━━━━━━━━━━━\n\n{celebration['en']}"

    # 3. Check for Special Milestone Messages
    milestone = None
    if info.days_remaining in MILESTONE_MESSAGES:
        milestone = MILESTONE_MESSAGES[info.days_remaining]

    # Get spiritual reflection
    am_reflection, en_reflection = get_daily_reflection(info.days_remaining)
    if custom_reflection:
        am_reflection = custom_reflection

    days_str = str(info.days_remaining)

    # 4. Construct messages according to language preference
    if language == "am":
        msg_lines = [
            f"✨ <b>{html.escape(event_name)}</b> ✨",
            "",
            "🎉 <b>ታላቁ ቀን እየቀረበ ነው!</b>",
            "",
            f"⏳ <b>ቀሪ {days_str} ቀናት ብቻ!</b>",
        ]
        if milestone:
            msg_lines.extend(["", milestone["am"]])
        else:
            msg_lines.extend(["", f"🙏 <i>{am_reflection}</i>"])

        msg_lines.extend(
            [
                "",
                f"📅 <b>ቀን፦</b> {event_date_display}",
                "",
                "❤️ <b>በደስታ እና በዝግጅት እንጠብቅ!</b>",
            ]
        )
        return "\n".join(msg_lines)

    elif language == "en":
        msg_lines = [
            f"✨ <b>{html.escape(event_name)} Countdown</b> ✨",
            "",
            "🎉 <b>The Grand Day is Drawing Near!</b>",
            "",
            f"⏳ <b>Only {days_str} Days Remaining!</b>",
        ]
        if milestone:
            msg_lines.extend(["", milestone["en"]])
        else:
            msg_lines.extend(["", f"🙏 <i>{en_reflection}</i>"])

        msg_lines.extend(
            [
                "",
                f"📅 <b>Date:</b> {event_date_display}",
                "",
                "❤️ <b>Let us await with joy and spiritual devotion!</b>",
            ]
        )
        return "\n".join(msg_lines)

    else:
        # Bilingual format (Amharic primary + English secondary)
        msg_lines = [
            f"✨ <b>{html.escape(event_name)} | Aelafat Zimare</b> ✨",
            "",
            "🎉 <b>ታላቁ ቀን እየቀረበ ነው! | The Grand Day is Approaching!</b>",
            "",
            f"⏳ <b>ቀሪ {days_str} ቀናት ብቻ! | Only {days_str} Days Remaining!</b>",
        ]
        if milestone:
            msg_lines.extend(["", milestone["am"], "", milestone["en"]])
        else:
            msg_lines.extend(
                [
                    "",
                    f"🙏 <i>{am_reflection}</i>",
                    f"<i>{en_reflection}</i>",
                ]
            )

        msg_lines.extend(
            [
                "",
                f"📅 <b>ቀን / Date:</b> {event_date_display}",
                "",
                "❤️ <b>በደስታ እንጠብቅ! | Awaiting in Joy and Unity!</b>",
            ]
        )
        return "\n".join(msg_lines)
