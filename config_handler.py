from main import APP_URL

def handle_config(bot, message):
    reply = (
        "<b>⚙️ Cấu hình hệ thống:</b>\n\n"
        f"🌐 Server: {APP_URL}\n"
        "🧠 Model: Zproject 3\n"
        "🔧 Phiên bản: ZProject V4.1"
    )
    bot.reply_to(message, reply, parse_mode="HTML")