import os
import json
import requests
from datetime import datetime
from memory import load_groups

# 🔧 Nếu bạn có API lưu nhóm (tùy chọn), set lại URL bên dưới
SYNC_URL = "https://zcode.x10.mx/groups.php"

def get_all_user_ids():
    return [int(f.replace("memory_", "").replace(".json", ""))
            for f in os.listdir() if f.startswith("memory_")]

def get_group_ids_from_server():
    try:
        r = requests.get("https://zcode.x10.mx/groups_db.json", timeout=5)
        return [g["group_id"] for g in r.json()]
    except Exception as e:
        print(f"[Groups] ❌ {e}")
        return []

def handle_noti(bot, message):
    if message.from_user.id != 5819094246:
        return bot.reply_to(message, "🚫 Chỉ admin.")

    text = message.text.replace("/noti", "").strip()
    if not text:
        return bot.reply_to(message, "⚠️ Nhập nội dung đi bạn!")

    now = datetime.now().strftime("%H:%M:%S %d/%m/%Y")
    notice = (
        "<b>📢 THÔNG BÁO TỪ ADMIN</b>\n\n"
        f"<b>🗒️ Nội dung:</b> {text}\n"
        f"<b>🕒 Thời gian:</b> {now}"
    )

    ids = set(get_all_user_ids()).union(get_group_ids_from_server())
    ok, fail = 0, 0
    for cid in ids:
        try:
            bot.send_message(cid, notice, parse_mode="HTML")
            ok += 1
        except:
            fail += 1
    bot.reply_to(message, f"✅ Gửi thành công: {ok}\n❌ Thất bại: {fail}")