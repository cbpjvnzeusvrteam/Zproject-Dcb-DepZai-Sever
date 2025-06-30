from memory import load_groups
from datetime import datetime

def handle_noti(bot, message):
    ADMIN_ID = 5819094246  # Thay bằng Telegram user_id của bạn để hạn chế quyền
    if message.from_user.id != ADMIN_ID:
        return bot.reply_to(message, "🚫 Lệnh này chỉ dành cho admin.")

    text = message.text.replace("/noti", "").strip()
    if not text:
        return bot.reply_to(message, "⚠️ Bạn chưa nhập nội dung thông báo.")

    # Nội dung mẫu
    now = datetime.now().strftime("%H:%M:%S - %d/%m/%Y")
    notice = (
        "<b>📢 <== THÔNG BÁO TỪ ADMIN ==></b>\n\n"
        "<b>👤 Từ Admin:</b> <a href='https://t.me/zproject2'>@Zproject</a> 💌\n"
        f"<blockquote><b>🗒️ Thông báo:</b> {text}</blockquote>\n"
        f"<b>🕒 Thời gian:</b> {now}\n\n"
        "💬 <i>Reply vào tin nhắn này để phản hồi lại admin 🎉</i>"
    )

    groups = load_groups()
    success, failed = 0, 0

    for chat_id in groups:
        try:
            bot.send_message(chat_id, notice, parse_mode="HTML", disable_web_page_preview=True)
            success += 1
        except Exception as e:
            print(f"[❌] Không gửi được tới {chat_id} → {e}")
            failed += 1

    bot.reply_to(message, f"✅ Đã gửi tới {success} nhóm/user.\n❌ Gửi lỗi: {failed}")