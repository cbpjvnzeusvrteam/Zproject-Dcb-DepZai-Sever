from gtts import gTTS
import uuid, os

def handle_tts(bot, message):
    text = message.text.replace("/tts", "").strip()
    if not text:
        return bot.reply_to(message, "🔊 Bạn chưa nhập văn bản!")

    tts = gTTS(text=text, lang="vi", slow=False)
    filename = f"zprojectxdcb_{uuid.uuid4().hex[:6]}.mp3"
    tts.save(filename)

    with open(filename, "rb") as f:
        bot.send_voice(message.chat.id, f, caption="🗣️ ZProject đọc cho bạn nè!")
    os.remove(filename)