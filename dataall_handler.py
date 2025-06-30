import os
import json
import requests
from datetime import datetime, timedelta
from collections import Counter
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton

ADMIN_ID = 5819094246  # Thay bằng ID admin thật
EXPORT_PREFIX = "zprojectxdcb_thongke_lanthu_"

def get_groups_from_server():
    try:
        r = requests.get("https://zcode.x10.mx/groups_db.json", timeout=5)
        data = r.json()
        return data if isinstance(data, list) else []
    except:
        return []

def handle_dataall(bot, message):
    if message.from_user.id != ADMIN_ID:
        return bot.reply_to(message, "🚫 Lệnh này chỉ dành cho admin.")

    users = [f for f in os.listdir() if f.startswith("memory_") and f.endswith(".json")]
    total_users = len(users)

    groups = get_groups_from_server()
    total_groups = len(groups)

    today = datetime.now().date()
    yesterday = today - timedelta(days=1)

    today_ask = 0
    yesterday_ask = 0
    hourly_count = Counter()
    user_count = Counter()
    user_name_map = {}
    with_image = 0
    without_image = 0

    for user_file in users:
        user_id = user_file.replace("memory_", "").replace(".json", "")
        try:
            with open(user_file, "r", encoding="utf-8") as f:
                data = json.load(f)
                for item in data:
                    created = item.get("created")
                    if not created:
                        continue
                    try:
                        dt = datetime.strptime(created, "%Y-%m-%d %H:%M:%S") + timedelta(hours=7)
                        hour = dt.strftime("%H:00")
                        date = dt.date()
                        hourly_count[hour] += 1
                        user_count[user_id] += 1
                        if "name" in item:
                            user_name_map[user_id] = item["name"]
                        if item.get("with_image"):
                            with_image += 1
                        else:
                            without_image += 1
                        if date == today:
                            today_ask += 1
                        elif date == yesterday:
                            yesterday_ask += 1
                    except:
                        continue
        except:
            continue

    diff = today_ask - yesterday_ask
    trend = "🔺 Tăng" if diff > 0 else ("🔻 Giảm" if diff < 0 else "⏸ Không đổi")

    top_users = sorted(user_count.items(), key=lambda x: x[1], reverse=True)[:5]
    top_text = "\n".join([
        f"👤 <b>{user_name_map.get(uid, 'ID ' + uid)}</b>: {count} lần"
        for uid, count in top_users
    ]) or "Chưa có dữ liệu"

    hour_table = "\n".join([
        f"{hour}: {count} lượt"
        for hour, count in sorted(hourly_count.items())
    ]) or "Không có dữ liệu"

    stat_html = f"""
<b>📊 ZProject Thống kê Dữ Liệu</b>\n\n
👥 <b>Tổng người dùng:</b> {total_users}\n
🏘️ <b>Tổng nhóm:</b> {total_groups}\n
📨 <b>Lượt dùng hôm nay:</b> {today_ask}\n
📆 <b>So với hôm qua:</b> {diff:+d} ({trend})\n
🖼️ Có ảnh: <b>{with_image}</b> • ❌ Không ảnh: <b>{without_image}</b>\n\n
<b>🏆 Top người dùng:</b>\n{top_text}\n\n
<b>⏰ Hoạt động theo giờ (VN):</b>\n<code>{hour_table}</code>
"""

    markup = InlineKeyboardMarkup()
    markup.add(InlineKeyboardButton("📄 Xuất thống kê .txt", callback_data="export_stats"))

    bot.send_message(message.chat.id, stat_html, parse_mode="HTML", reply_markup=markup)

def export_stats_txt(bot, call):
    if call.from_user.id != ADMIN_ID:
        return bot.answer_callback_query(call.id, "🚫 Không có quyền!")

    index = 0
    while os.path.exists(f"{EXPORT_PREFIX}{index}.txt"):
        index += 1

    filename = f"{EXPORT_PREFIX}{index}.txt"
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    total_users = len([f for f in os.listdir() if f.startswith("memory_")])
    groups = get_groups_from_server()
    total_groups = len(groups)

    content = f"""📊 ZProject Thống kê #{index}
Thời gian: {now}
Tổng người dùng: {total_users}
Tổng nhóm: {total_groups}
"""

    with open(filename, "w", encoding="utf-8") as f:
        f.write(content)

    bot.send_document(call.message.chat.id, open(filename, "rb"), caption=f"📄 Thống kê #{index}")
    os.remove(filename)
    bot.answer_callback_query(call.id, "✅ Đã gửi file thống kê!")