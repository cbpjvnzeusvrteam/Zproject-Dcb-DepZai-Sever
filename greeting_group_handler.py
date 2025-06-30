import requests
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton

def handle_bot_added(bot, message):
    if message.new_chat_members:
        for member in message.new_chat_members:
            if member.id == bot.get_me().id:
                chat_id = message.chat.id
                title = message.chat.title or "Không rõ"
                username = message.chat.username or ""

                # ✅ Gửi greeting kèm nút
                markup = InlineKeyboardMarkup()
                markup.add(
                    InlineKeyboardButton("📢 Kênh Thông Báo", url="https://t.me/zproject3"),
                    InlineKeyboardButton("💬 Kênh Chat", url="https://t.me/zproject4")
                )

                greeting = (
                    "<b>🖖 Xin Chào Mọi Người!</b>\n\n"
                    "<i>Tôi là ZProject và WormGpt V3</i>, được phát triển bởi <b>Zproject X Duong Cong Bang</b>.\n"
                    "Telegram của nhà phát triển tôi: <a href='https://t.me/zproject2'>@duongcongbang.dev</a>\n\n"
                    "<blockquote>Hãy tham gia ngay cộng đồng ZProject để cập nhật thông tin mới nhất!</blockquote>\n\n"
                    "👉 Bạn có thể nhấn 2 nút bên dưới để theo dõi kênh & trò chuyện cùng chúng tôi 💖"
                )

                bot.send_message(chat_id, greeting, parse_mode="HTML", reply_markup=markup)

                # ✅ Đồng bộ lên server
                try:
                    requests.post("https://zcode.x10.mx/save_group.php", json={
                        "group_id": chat_id,
                        "group_name": title,
                        "username": username
                    }, timeout=5)
                    print(f"📡 Đã sync nhóm {chat_id} lên server!")
                except Exception as e:
                    print(f"❌ Sync group lỗi: {e}")