from ask_handler import handle_ask
from types import SimpleNamespace
from gtts import gTTS
import uuid, os
import re

# 🔁 Xử lý nút Trả lời lại
def handle_retry_button(bot, call):
    try:
        _, uid, question = call.data.split("|", 2)
        if str(call.from_user.id) != uid:
            return bot.answer_callback_query(call.id, "🚫 Không phải câu hỏi của bạn nha!")

        msg = SimpleNamespace()
        msg.chat = call.message.chat
        msg.message_id = call.message.message_id
        msg.text = "/ask " + question
        msg.from_user = call.from_user
        msg.reply_to_message = None

        bot.answer_callback_query(call.id, "🔁 Đang trả lời lại...")
        handle_ask(bot, msg)
    except Exception as e:
        bot.answer_callback_query(call.id, "⚠️ Lỗi retry!")
        print(f"[RETRY] ❌ {e}")

# 🔊 Xử lý nút chuyển voice
def handle_tts_button(bot, call):
    try:
        parts = call.data.split("|")
        uid = parts[1]
        reply_id = parts[2]

        answer = bot.voice_map.get(reply_id)
        if not answer:
            return bot.answer_callback_query(call.id, "❌ Không tìm thấy dữ liệu giọng nói.")

        # 🧼 Loại bỏ phần <code>...</code> và tag HTML khác
        clean = re.sub(r"<code>.*?</code>", "", answer, flags=re.DOTALL)
        clean = re.sub(r"<[^>]+>", "", clean)
        text = clean.strip()

        if not text or len(text) < 5:
            return bot.answer_callback_query(call.id, "❗ Nội dung quá ngắn hoặc rỗng để chuyển voice.")

        filename = f"zprojectxdcb_{reply_id}.mp3"
        tts = gTTS(text=text, lang="vi", slow=False)
        tts.save(filename)

        with open(filename, "rb") as f:
            bot.send_voice(call.message.chat.id, f, caption="🗣️ Đây là bản đọc giọng ZProject!")
        os.remove(filename)
        bot.answer_callback_query(call.id, "🎧 Voice đã được gửi!")
    except Exception as e:
        bot.answer_callback_query(call.id, "⚠️ Lỗi tạo voice.")
        print(f"[TTS] ❌ {e}")