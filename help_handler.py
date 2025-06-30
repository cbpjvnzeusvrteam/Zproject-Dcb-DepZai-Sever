def handle_help(bot, message):
    reply = (
        "<b>📖 Lệnh hỗ trợ:</b>\n\n"
        "<code>/start</code> - Bắt Đầu\n"
        "<code>/ask</code> – Hỏi AI\n"
        "<code>/tts văn bản</code> – Chuyển văn bản thành giọng nói\n"
        "<code>/about</code> – Giới thiệu về bot\n"
        "<code>/noti</code> - Thông Báo All Sever ( Admin )\n"
        "<code>/dataall</code> – Thống kê người dùng ( Admin )\n"
        "<code>/time</code> – Thời gian uptime"
    )
    bot.reply_to(message, reply, parse_mode="HTML")