def handle_about(bot, message):
    reply = (
        "<b>🤖 ZProject Bot</b>\n\n"
        "Được phát triển bởi <b>Zproject</b> & <i>Duong Cong Bang</i>.\n"
        "Hỗ trợ AI WormGPT – thông minh & đáng yêu 😻\n\n"
        "Liên hệ admin: <a href='https://t.me/zproject2'>@zproject2</a>"
    )
    bot.reply_to(message, reply, parse_mode="HTML")