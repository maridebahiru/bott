# ✝️ የአእላፋት ዝማሬ (Aelafat Zimare) - Telegram Countdown Bot

[![Python 3.12+](https://img.shields.io/badge/python-3.12%2B-blue.svg)](https://www.python.org/)
[![python-telegram-bot 22+](https://img.shields.io/badge/python--telegram--bot-22.8-blue.svg)](https://python-telegram-bot.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-gold.svg)](LICENSE)
[![Deploy to Render](https://render.com/images/deploy-to-render-button.svg)](https://render.com)

A production-ready Telegram countdown bot designed with Ethiopian Orthodox Christian reverence for the sacred spiritual gathering **«የአእላፋት ዝማሬ» (Aelafat Zimare)** on **January 5, 2027**.

- **Bot Username:** [@Aelafat_ZimareBot](https://t.me/Aelafat_ZimareBot)
- **Target Event Date:** January 5, 2027 (ታህሳስ 27)
- **Timezone:** `Africa/Addis_Ababa` (UTC+3)
- **Schedule:** Daily at 9:00 AM Ethiopian Time (ጠዋት 3:00)
- **Primary Language:** Amharic (አማርኛ)
- **Secondary Language:** English

---

## 🌟 Key Features

1. **Dynamic Real-Time Countdown:**
   - Accurately calculates remaining days, hours, and minutes in the `Africa/Addis_Ababa` timezone.
   - Never uses hardcoded countdown values.
   - Automatically handles leap years, date boundaries, and daylight saving neutrality.

2. **Special Milestone Messages:**
   - Dedicated celebration announcements for:
     - 30 days remaining (1 month)
     - 14 days remaining (2 weeks)
     - 7 days remaining (1 week)
     - 3 days, 2 days, and 1 day remaining
     - **Event Day (Day 0):** Exciting celebration message that the sacred day has arrived!
     - **Post-Event:** Graceful completion notice.

3. **35+ Rotating Amharic Spiritual Reflections:**
   - Authentic and reverent reflections focused on mezmur, praise, unity, and spiritual preparation.
   - Strictly verified spiritual wording; never invents unauthorized scriptures.
   - Rotates daily so consecutive days never see repetitive messages.

4. **Guaranteed Zero-Duplicate Scheduling:**
   - Persistent SQLite tracking records every post date and chat ID.
   - Server or container restarts will **never** cause duplicate messages to be sent on the same day.
   - Built-in **Startup Catch-Up**: If a restart occurs after 9:00 AM and today's post was missed, it detects and safely delivers today's message once.

5. **Enterprise-Grade Admin Controls:**
   - Full administrative authorization: Telegram group administrators, bot owners, and SQLite-configured admins.
   - Configure target groups dynamically via `/setgroup`.
   - Pause (`/pause`), resume (`/resume`), preview (`/preview`), or test (`/testpost`).
   - Dynamically adjust event date (`/setdate`), post time (`/settime`), or banner image (`/setimage`) without redeploying code.

---

## 📁 Project Architecture

```
aelafat/
├── bot.py                  # Main entry point, Telegram bot setup, signal handling
├── config.py               # Environment configuration loader and validator
├── database.py             # SQLite thread-safe persistence and duplicate prevention
├── countdown.py            # Real-time datetime math in Africa/Addis_Ababa timezone
├── messages.py             # 35+ Amharic reflections, milestones, and bilingual formatters
├── scheduler.py            # Daily JobQueue scheduler and startup catch-up logic
├── handlers/
│   ├── __init__.py
│   ├── start.py            # /start command handler
│   ├── countdown.py        # /countdown live command handler
│   ├── about.py            # /about and /help command handlers
│   └── admin.py            # /setgroup, /status, /testpost, /pause, /resume, etc.
├── tests/
│   ├── __init__.py
│   ├── test_countdown.py   # Tests for date math, milestones, and timezones
│   ├── test_messages.py    # Tests for reflections count, bilingual layout, event day
│   ├── test_database.py    # Tests for SQLite CRUD, duplicate prevention, admins
│   ├── test_admin.py       # Tests for authorization checks
│   └── test_scheduler.py   # Tests for scheduled jobs and skip conditions
├── requirements.txt        # Production dependencies
├── render.yaml             # Render Background Worker infrastructure configuration
├── .env.example            # Environment variables template
├── .gitignore              # Git ignore rules (protecting .env and *.db)
└── README.md               # Complete project documentation
```

---

## 🛠️ Telegram Commands

### 👥 Public Commands

| Command | Description |
|---|---|
| `/start` | Welcome message and bot introduction in Amharic & English |
| `/countdown` | Live real-time countdown showing remaining days, hours, and minutes |
| `/preview` | Preview the upcoming scheduled daily countdown message |
| `/about` | Background and purpose of የአእላፋት ዝማሬ |
| `/help` | Detailed help menu with all available commands |

### 🔐 Administrator Commands

> *Restricted to Bot Owners (`BOT_OWNER_ID`), registered admins, and Telegram Group Admins.*

| Command | Arguments | Description |
|---|---|---|
| `/setgroup` | `[chat_id]` (optional) | Set current chat (or specified ID) as the target group for daily posts |
| `/status` | None | Detailed status report: schedule, date, timezone, group, last post |
| `/testpost` | None | Send an immediate test countdown message to the configured group |
| `/pause` | None | Temporarily pause automatic 9:00 AM daily messages |
| `/resume` | None | Resume automatic 9:00 AM daily messages |
| `/setdate` | `YYYY-MM-DD` | Dynamically update the target event date |
| `/settime` | `HH:MM` | Dynamically update the 24-hr daily post time (Addis Ababa time) |
| `/setimage` | `[image_url]` | Set or clear the promotional banner image for posts |

---

## ⚙️ Environment Variables Reference

Create a `.env` file from `.env.example`:

```bash
cp .env.example .env
```

| Variable | Required | Default | Description |
|---|---|---|---|
| `TELEGRAM_BOT_TOKEN` | **Yes** | — | Bot token from [@BotFather](https://t.me/BotFather) |
| `BOT_OWNER_ID` | Recommended | — | Telegram user ID(s) of superadmin (comma-separated) |
| `TELEGRAM_GROUP_ID` | Optional | — | Fallback group ID where posts are published |
| `EVENT_DATE` | Optional | `2027-01-05` | Target event date (`YYYY-MM-DD`) |
| `TIMEZONE` | Optional | `Africa/Addis_Ababa` | IANA timezone name |
| `POST_TIME` | Optional | `09:00` | Daily post time (24-hr `HH:MM`) |
| `DATABASE_PATH` | Optional | `aelafat.db` | Path to SQLite database (`/var/data/aelafat.db` on Render) |
| `PROMO_IMAGE_URL` | Optional | — | Optional promotional image URL or path |
| `DEFAULT_LANGUAGE` | Optional | `both` | `am` (Amharic), `en` (English), or `both` |
| `LOG_LEVEL` | Optional | `INFO` | Logging level (`DEBUG`, `INFO`, `WARNING`, `ERROR`) |

---

## 💻 Local Development Setup

1. **Clone the repository:**
   ```bash
   git clone https://github.com/<your-username>/aelafat-countdown.git
   cd aelafat-countdown
   ```

2. **Create and activate virtual environment:**
   ```bash
   # Windows (PowerShell)
   python -m venv .venv
   .\.venv\Scripts\Activate.ps1

   # Linux / macOS
   python3 -m venv .venv
   source .venv/bin/activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure your `.env`:**
   ```bash
   cp .env.example .env
   # Edit .env and paste your newly generated TELEGRAM_BOT_TOKEN
   ```

5. **Run the unit test suite:**
   ```bash
   pytest tests/ -v
   ```

6. **Start the bot locally:**
   ```bash
   python bot.py
   ```

---

## 🚀 Production Deployment on Render

The bot is designed to run 24/7 in the cloud as a **Background Worker** on [Render](https://render.com), so it continues running without needing your personal computer.

### Step 1: Push Code to GitHub

1. Create a **Private** or Public repository on GitHub (e.g., `aelafat-countdown`).
2. Add your GitHub remote and push:
   ```bash
   git add .
   git commit -m "Complete production-ready Aelafat Countdown Bot"
   git branch -M main
   git remote add origin https://github.com/<your-username>/aelafat-countdown.git
   git push -u origin main
   ```

### Step 2: Deploy as a Background Worker on Render

1. Log in to your [Render Dashboard](https://dashboard.render.com).
2. Click **New +** and select **Background Worker**.
3. Connect your `aelafat-countdown` repository.
4. Fill in the following details:
   - **Name:** `aelafat-countdown-bot`
   - **Region:** `Frankfurt (EU Central)` *(recommended for lower latency to East Africa)*
   - **Runtime:** `Python 3`
   - **Build Command:** `pip install -r requirements.txt`
   - **Start Command:** `python bot.py`
   - **Instance Type:** `Starter` ($7/mo) or `Standard`

### Step 3: Attach Persistent Disk (For SQLite)

To preserve the database and posting history across container rebuilds:
1. In the service settings, scroll down to **Disks**.
2. Click **Add Disk**:
   - **Name:** `aelafat-data`
   - **Mount Path:** `/var/data`
   - **Size:** `1 GB`

### Step 4: Add Environment Variables in Render

In the **Environment** tab of your Render service, add:

- `TELEGRAM_BOT_TOKEN`: `<Your Bot Token from @BotFather>`
- `BOT_OWNER_ID`: `<Your Telegram User ID>`
- `DATABASE_PATH`: `/var/data/aelafat.db`
- `EVENT_DATE`: `2027-01-05`
- `TIMEZONE`: `Africa/Addis_Ababa`
- `POST_TIME`: `09:00`
- `DEFAULT_LANGUAGE`: `both`
- `LOG_LEVEL`: `INFO`

Click **Save Changes**. Render will automatically build and start the bot!

---

## 📱 Bot Configuration in Telegram

Once your bot is running on Render:

1. **Add the Bot to your Telegram Group:**
   - Search for `@Aelafat_ZimareBot` and add it to your event organizing group.
   - Promote `@Aelafat_ZimareBot` to **Administrator** with permission to send messages.

2. **Bind the Group:**
   - Inside the Telegram group, type:
     ```
     /setgroup
     ```
   - The bot will reply confirming that daily posts will now appear in this group every morning at 9:00 AM Ethiopia time.

3. **Send a Test Post:**
   - Send:
     ```
     /testpost
     ```
   - Verify the formatted Amharic and English countdown message is received in the group.

4. **Check Status:**
   - Send:
     ```
     /status
     ```
   - Verify that status shows `Active`, the target group is configured, and the next countdown date is calculated.

---

## 🔒 Security Best Practices

- **Zero Hardcoded Secrets:** The bot token is never stored in source files.
- **Git Protection:** `.env` and SQLite files (`*.db`) are strictly ignored in `.gitignore`.
- **Admin Verification:** Any administrative change verifies Telegram admin rights or owner credentials before execution.
- **Error Obfuscation:** Global error handlers log details securely in standard output without sending raw system errors or tokens to Telegram users.

---

## 📜 License

This project is licensed under the MIT License - feel free to use and adapt for Ethiopian Orthodox spiritual events and church assemblies.
