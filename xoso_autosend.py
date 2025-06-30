import time
import threading
import requests
from bs4 import BeautifulSoup
from memory import load_groups
from telebot import TeleBot
from datetime import datetime, timedelta
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton

# ⚙️ Giờ gửi
HOUR_MN = 16
MINUTE_MN = 30
HOUR_MB = 18
MINUTE_MB = 30

def get_mb_button():
    markup = InlineKeyboardMarkup()
    markup.add(InlineKeyboardButton("📌 Xổ số Miền Bắc", callback_data="show_xsmb"))
    return markup

def get_xsmb_text():
    try:
        res = requests.get("https://xsmn.me/xsmb-xo-so-mien-bac.html", timeout=10)
        res.encoding = 'utf-8'
        soup = BeautifulSoup(res.text, "html.parser")
        table = soup.select_one("table.kqmb tbody")
        if not table:
            return None

        rows = table.find_all("tr")
        result = "<b>🎯 KẾT QUẢ XỔ SỐ MIỀN BẮC</b>\n\n"
        for row in rows:
            giai = row.select_one("td.txt-giai")
            nums = [span.text.strip() for span in row.select("td span")]
            if giai and nums:
                result += f"<b>{giai.text.strip()}:</b> {' - '.join(nums)}\n"

        now = datetime.now().strftime("%d/%m/%Y %H:%M")
        result += f"\n🕒 <i>Cập nhật lúc {now}</i>\n🎉 Chúc bạn may mắn!"
        return result
    except Exception as e:
        print("[XSMB] Lỗi:", e)
        return None

def get_xsmn_text():
    try:
        url = "https://xsmn.me/"
        res = requests.get(url, timeout=10)
        res.encoding = 'utf-8'
        soup = BeautifulSoup(res.text, "html.parser")
        block = soup.select_one("div#load_kq_mn_0")
        table = block.select_one("table.extendable tbody")
        if not table:
            return None

        provinces = [th.text.strip() for th in table.select("tr.gr-yellow th") if th.text.strip()]
        rows = table.select("tr")[1:]

        result = f"<b>🎯 KẾT QUẢ XỔ SỐ MIỀN NAM</b>\n\n"
        for i, province in enumerate(provinces):
            result += f"<u>🏙️ {province}</u>\n"
            for row in rows:
                cells = row.select("td")
                if len(cells) > i + 1:
                    label = cells[0].text.strip()
                    value = cells[i+1].text.strip()
                    if label and value:
                        result += f"{label}: {value}\n"
            result += "\n"

        now = datetime.now().strftime("%d/%m/%Y %H:%M")
        result += f"🕒 <i>Cập nhật lúc {now}</i>\n📌 Bấm nút để xem xổ số miền Bắc"
        return result
    except Exception as e:
        print("[XSMN] Lỗi:", e)
        return None

def auto_send_xoso(bot: TeleBot, user_ids: set):
    def loop():
        while True:
            now = datetime.now()
            hour, minute = now.hour, now.minute

            if hour == HOUR_MN and minute == MINUTE_MN:
                msg = get_xsmn_text()
                if msg:
                    print("[🎯] Gửi XSMN...")
                    for uid in user_ids:
                        try:
                            bot.send_message(uid, msg, parse_mode="HTML", reply_markup=get_mb_button())
                        except Exception as e:
                            print(f"[⚠️] Lỗi MN gửi cho {uid}: {e}")
                time.sleep(61)

            elif hour == HOUR_MB and minute == MINUTE_MB:
                msg = get_xsmb_text()
                if msg:
                    print("[🎯] Gửi XSMB...")
                    for uid in user_ids:
                        try:
                            bot.send_message(uid, msg, parse_mode="HTML")
                        except Exception as e:
                            print(f"[⚠️] Lỗi MB gửi cho {uid}: {e}")
                time.sleep(61)
            else:
                time.sleep(10)

    threading.Thread(target=loop, daemon=True).start()