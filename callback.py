from ask_handler import handle_ask
from types import SimpleNamespace
from gtts import gTTS
from pydub import AudioSegment
import uuid, os, re

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

def handle_tts_button(bot, call):
    try:
        parts = call.data.split("|")
        uid = parts[1]
        reply_id = parts[2]

        answer = bot.voice_map.get(reply_id)
        if not answer:
            return bot.answer_callback_query(call.id, "❌ Không tìm thấy dữ liệu giọng nói.")

        # 🧼 Làm sạch nội dung: bỏ <code>...</code> và tag HTML
        clean = re.sub(r"<code>.*?</code>", "", answer, flags=re.DOTALL)
        clean = re.sub(r"<[^>]+>", "", clean)
        text = clean.strip()

        if not text or len(text) < 5:
            return bot.answer_callback_query(call.id, "❗ Nội dung quá ngắn để chuyển voice.")

        filename = f"zprojectxdcb_{reply_id}.mp3"

        # 🎙️ Tạo voice gốc bằng gTTS
        tts = gTTS(text=text, lang="vi", slow=False, tld="com.vn")
        tts.save(filename)

        # ⚡ Tăng tốc độ bằng pydub (speedup 1.25x)
        sound = AudioSegment.from_file(filename)
        faster = sound.speedup(playback_speed=1.25)
        faster.export(filename, format="mp3")

        with open(filename, "rb") as f:
            bot.send_voice(call.message.chat.id, f, caption="🗣️ Đây là voice của Zproject:)")
        os.remove(filename)
        bot.answer_callback_query(call.id, "🎧 Đã gửi voice!")
    except Exception as e:
        bot.answer_callback_query(call.id, "⚠️ Lỗi tạo voice.")
        print(f"[TTS] ❌ {e}")