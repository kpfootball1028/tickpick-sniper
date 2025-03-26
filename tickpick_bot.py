# TickPick Ticket Sniping Bot - Safe Start with Telegram Alerts

import os
import time
import requests
from bs4 import BeautifulSoup
from datetime import datetime

print("✅ TickPick scraper bot starting (safe start mode)...", flush=True)

try:
    TELEGRAM_BOT_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')
    TELEGRAM_CHAT_ID = os.getenv('TELEGRAM_CHAT_ID')

    if not TELEGRAM_BOT_TOKEN or not TELEGRAM_CHAT_ID:
        raise ValueError("Missing TELEGRAM_BOT_TOKEN or TELEGRAM_CHAT_ID")

    print("✅ Telegram credentials loaded", flush=True)

    TICKPICK_URL = "https://www.tickpick.com/ncaa-mens-basketball-east-regional-tickets/"

    SECTION_KEYWORDS = {
        'lower': ['8', '9', '10', '18', '19', '20', '21'],
        'mid': ['108', '109', '110', '120', '121', '122'],
        'upper': ['208', '209', '210', '220', '221', '222']
    }

    HEADERS = {
        'User-Agent': 'Mozilla/5.0'
    }

    def send_telegram(message):
        try:
            url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
            payload = {
                'chat_id': TELEGRAM_CHAT_ID,
                'text': message,
                'parse_mode': 'Markdown'
            }
            response = requests.post(url, data=payload)
            if response.status_code != 200:
                print(f"⚠️ Telegram error: {response.text}", flush=True)
        except Exception as e:
            print(f"⚠️ Telegram send failed: {e}", flush=True)

    def determine_tier(section):
        for tier, keywords in SECTION_KEYWORDS.items():
            if section in keywords:
                return tier
        return None

    def scrape_tickpick():
        print(f"[{datetime.now()}] 🔍 Scraping TickPick for tickets...", flush=True)
        try:
            response = requests.get(TICKPICK_URL, headers=HEADERS)
            soup = BeautifulSoup(response.text, 'html.parser')
        except Exception as e:
            print(f"🔥 Error loading TickPick page: {e}", flush=True)
            return

        ticket_blocks = soup.select('div.ticket')
        print(f"Found {len(ticket_blocks)} ticket blocks", flush=True)

        best_matches = {'lower': None, 'mid': None, 'upper': None}

        for block in ticket_blocks:
            try:
                section = block.get('data-section', '').strip()
                row = block.get('data-row', '').strip()
                quantity = int(block.get('data-quantity', '1'))
                price = float(block.get('data-price', '0'))

                if not section or quantity < 2:
                    continue

                tier = determine_tier(section)
                if not tier:
                    continue

                current_best = best_matches[tier]
                if not current_best or price < current_best['price']:
                    best_matches[tier] = {
                        'section': section,
                        'row': row,
                        'price': price,
                        'quantity': quantity
                    }
            except Exception as e:
                print(f"⚠️ Ticket parse error: {e}", flush=True)

        for tier, match in best_matches.items():
            if match:
                msg = (
                    f"🎟️ *Cheapest {tier.capitalize()} Tier Ticket on TickPick*\n"
                    f"Section {match['section']} Row {match['row']}\n"
                    f"*Price:* ${match['price']} per ticket\n"
                    f"*Quantity:* {match['quantity']}\n"
                    f"👉 [View Tickets]({TICKPICK_URL})"
                )
                print(f"[{datetime.now()}] ✅ Alert: {tier} tier — ${match['price']}", flush=True)
                send_telegram(msg)
            else:
                print(f"[{datetime.now()}] ⚠️ No tickets found for {tier} tier", flush=True)

    while True:
        try:
            scrape_tickpick()
        except Exception as e:
            print(f"🔥 Error in main loop: {e}", flush=True)
        time.sleep(38)

except Exception as outer_e:
    print(f"🔥 Startup failure: {outer_e}", flush=True)
