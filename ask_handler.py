import requests, base64, uuid, json, re
from io import BytesIO
from PIL import Image
from datetime import datetime
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton

from memory import load_user_memory, save_user_memory
from formatter import format_html
from gtts import gTTS
import os

GEMINI_API_KEY = "AIzaSyDpmTfFibDyskBHwekOADtstWsPUCbIrzE"
GEMINI_URL = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent?key={GEMINI_API_KEY}"
REMOTE_PROMPT_URL = "https://zcode.x10.mx/prompt.json"
REMOTE_LOG_HOST = "https://zcode.x10.mx/save.php"

# Tạo nút
def build_reply_button(user_id, question, reply_id=None):
    safe_q = re.sub(r"[^\w\s]", "", question.strip())[:50]
    markup = InlineKeyboardMarkup()
    markup.row(
        InlineKeyboardButton("🔁 Trả lời lại", callback_data=f"retry|{user_id}|{safe_q}"),
        InlineKeyboardButton("🔊 Chuyển sang Voice", callback_data=f"tts|{user_id}|{reply_id}") if reply_id else None
    )
    return markup

# Hàm chính
def handle_ask(bot, message):
    prompt = message.text.replace("/ask", "").strip()
    if not prompt:
        return bot.reply_to(message, "❓ Bạn chưa nhập câu hỏi rồi đó!")

    msg_status = bot.reply_to(message, "🤖")

    user_id = message.from_user.id
    user_name = message.from_user.first_name
    memory = load_user_memory(user_id)

    # Load prompt
    try:
        prompt_data = requests.get(REMOTE_PROMPT_URL, timeout=5).json()
        system_prompt = prompt_data.get("prompt", "Bạn là AI thông minh vui vẻ.")
    except:
        system_prompt = "Bạn là AI thông minh vui vẻ."

    # Ghép 5 câu cũ
    history_block = ""
    if memory:
        for item in memory[-5:]:
            history_block += f"Người dùng hỏi: {item['question']}\nAI: {item['answer']}\n"

    full_prompt = f"{system_prompt}\n\n[Ngữ cảnh trước đó với {user_name}]\n{history_block}\nNgười dùng hiện tại hỏi: {prompt}"

    headers = {"Content-Type": "application/json"}
    parts = [{"text": full_prompt}]
    image_attached = False

    # Ảnh nếu có
    if message.reply_to_message and message.reply_to_message.photo:
        try:
            photo = message.reply_to_message.photo[-1]
            file_info = bot.get_file(photo.file_id)
            downloaded = bot.download_file(file_info.file_path)
            image = Image.open(BytesIO(downloaded))
            buffer = BytesIO()
            image.save(buffer, format="JPEG")
            base64_img = base64.b64encode(buffer.getvalue()).decode()
            parts.insert(0, {
                "inline_data": {
                    "mime_type": "image/jpeg",
                    "data": base64_img
                }
            })
            image_attached = True
        except Exception as e:
            print(f"[ẢNH] Lỗi xử lý: {e}")

    data = {"contents": [{"parts": parts}]}
    try:
        res = requests.post(GEMINI_URL, headers=headers, json=data)
        res.raise_for_status()
        result = res.json()["candidates"][0]["content"]["parts"][0]["text"]
    except Exception as e:
        return bot.edit_message_text(
            f"❌ API lỗi:\n<pre>{e}</pre>",
            msg_status.chat.id,
            msg_status.message_id,
            parse_mode="HTML"
        )

    # Lưu lại
    entry = {
        "question": prompt,
        "answer": result,
        "created": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "with_image": image_attached,
        "name": user_name
    }
    memory.append(entry)
    save_user_memory(user_id, memory)

    try:
        requests.post(
            f"{REMOTE_LOG_HOST}?uid={user_id}",
            data=json.dumps(memory, ensure_ascii=False),
            headers={"Content-Type": "application/json"},
            timeout=5
        )
    except:
        pass

    # Format văn bản
    try:
        formatted = format_html(result)
    except:
        formatted = result.replace("<", "&lt;").replace(">", "&gt;")

    reply_id = uuid.uuid4().hex[:6]
    markup = build_reply_button(user_id, prompt, reply_id)

    # Gửi voice nếu nhấn
    bot.voice_map = getattr(bot, "voice_map", {})
    bot.voice_map[reply_id] = result

    if len(formatted) > 4000:
        filename = f"zproject_{reply_id}.html"
        with open(filename, "w", encoding="utf-8") as f:
            f.write(formatted)
        bot.send_document(
            message.chat.id,
            open(filename, "rb"),
            caption="📄 Trả lời dài quá nên gửi file nha!",
            parse_mode="HTML"
        )
    else:
        bot.edit_message_text(
            f"🤖 <i>ZProject [ WORMGPT ] trả lời:</i>\n\n<b>{formatted}</b>",
            msg_status.chat.id,
            msg_status.message_id,
            parse_mode="HTML",
            reply_markup=markup
        )