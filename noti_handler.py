import os
import json
import requests
from datetime import datetime

def get_all_user_ids():
    return [int(f.replace("memory_", "").replace(".json", ""))
            for f in os.listdir() if f.startswith("memory_")]

def get_group_ids_from_server():
    try:
        r = requests.get("https://zcode.x10.mx/groups_db.json", timeout=5)
        text = r.text.strip()
        if not text or text[0] not in ['[', '{']:
            return []
        return [g["group_id"] for g in json.loads(text)]
    except Exception as e:
        print(f"[Groups] ❌ {e}")
        return []

def handle_noti(bot, message):
    if message.from_user.id != 5819094246:
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

    ids = set(get_all_user_ids()).union(get_group_ids_from_server())
    success, fail = 0, 0

    for cid in ids:
        try:
            bot.send_message(cid, notice, parse_mode="HTML", disable_web_page_preview=True)
            success += 1
        except:
            fail += 1

    bot.reply_to(message, f"✅ Gửi thành công: {success}\n❌ Thất bại: {fail}")