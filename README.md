
# TickPick Ticket Sniper Bot

This bot scrapes TickPick every 38 seconds for NCAA basketball tickets in sideline sections. It sends the cheapest ticket per tier (lower, mid, upper) to your Telegram via bot alerts.

## 🚀 Setup

### 1. GitHub

- Create a new repo on GitHub (e.g. `tickpick-sniper`)
- Upload all 3 files: `tickpick_bot.py`, `requirements.txt`, and `README.md`

### 2. Render Setup

- Go to [https://dashboard.render.com/](https://dashboard.render.com/)
- Click **New → Background Worker**
- Connect your GitHub repo
- Fill in:
  - **Build Command:** (leave blank)
  - **Start Command:**  
    ```
    python3 tickpick_bot.py
    ```

### 3. Environment Variables

Add the following two variables:

| Name                | Value                            |
|---------------------|----------------------------------|
| `TELEGRAM_BOT_TOKEN`| Your bot token                   |
| `TELEGRAM_CHAT_ID`  | Your Telegram user or group ID   |

### 4. Deploy

- Click **Manual Deploy → Deploy latest commit**
- Open the **Logs** tab to confirm it’s scraping and sending alerts

You're done 🎉
