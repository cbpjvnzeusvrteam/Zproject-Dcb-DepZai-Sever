import os
import json
from datetime import datetime

ADMIN_ID = 5819094246
GROUPS_FILE = "groups.json"

def get_all_user_ids():
    return [int(f.replace("memory_", "").replace(".json", ""))
            for f in os.listdir() if f.startswith("memory_")]

def get_group_ids_from_file():
    if os.path.exists(GROUPS_FILE):
        try:
            with open(GROUPS_FILE, "r") as f:
                return json.load(f)
        except:
            pass
    return []

def handle_noti(bot, message):
    if message.from_user.id != ADMIN_ID:
        return bot.reply_to(message, "🚫 Chỉ dành cho admin.")

    text = message.text.replace("/noti", "").strip()
    if not text:
        return bot.reply_to(message, "⚠️ Vui lòng nhập nội dung.")

    now = datetime.now().strftime("%H:%M:%S %d/%m/%Y")
    notice = (
        "<b>📢 THÔNG BÁO TỪ ADMIN</b>\n\n"
        f"<b>🗒️ Nội dung:</b> {text}\n"
        f"<b>🕒 Thời gian:</b> {now}\n\n"
        "<i>Gửi bởi ZProject Bot</i>"
    )

    all_ids = set(get_all_user_ids()).union(get_group_ids_from_file())
    success, fail = 0, 0

    for cid in all_ids:
        try:
            bot.send_message(cid, notice, parse_mode="HTML", disable_web_page_preview=True)
            success += 1
        except:
            fail += 1

    bot.reply_to(message, f"✅ Gửi thành công: {success}\n❌ Thất bại: {fail}")