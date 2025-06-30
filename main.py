import os, threading, datetime
from flask import Flask, request
import telebot

from ask_handler import handle_ask
from utils import auto_group_greeting
from memory import load_groups, save_groups
from start_handler import handle_start
from dataall_handler import handle_dataall
from greeting_group_handler import handle_bot_added
from help_handler import handle_help
from tts_handler import handle_tts
from about_handler import handle_about
from callback import handle_retry_button, handle_tts_button
from noti_handler import handle_noti
from xoso_autosend import auto_send_xoso, get_xsmb_text
from track_interactions import sync_group_locally

TOKEN = "7053031372:AAGGOnE72JbZat9IaXFqa-WRdv240vSYjms"
APP_URL = "https://sever-zproject.onrender.com"
bot = telebot.TeleBot(TOKEN)
app = Flask(__name__)
START_TIME = datetime.datetime.now()
GROUP_FILE = "groups.json"

GROUPS = load_groups()

@app.route("/")
def home():
    return "<h3>🤖 ZProject đang hoạt động!</h3>"

@app.route(f"/{TOKEN}", methods=["POST"])
def webhook():
    update = telebot.types.Update.de_json(request.get_data().decode("utf-8"))
    bot.process_new_updates([update])
    return "!", 200
# ===== LỆNH =====

@bot.message_handler(commands=["start"])
def start_cmd(message):
    sync_group_locally(message.chat)
    handle_start(bot, message)

@bot.message_handler(commands=["help"])
def help_command(message):
    sync_group_locally(message.chat)
    handle_help(bot, message)

@bot.message_handler(commands=["about"])
def about_command(message):
    sync_group_locally(message.chat)
    handle_about(bot, message)

@bot.message_handler(commands=["ask"])
def ask_command(message):
    sync_group_locally(message.chat)
    handle_ask(bot, message)

@bot.message_handler(commands=["tts"])
def tts_command(message):
    sync_group_locally(message.chat)
    handle_tts(bot, message)

@bot.message_handler(commands=["dataall"])
def dataall_command(message):
    sync_group_locally(message.chat)
    handle_dataall(bot, message)

@bot.message_handler(commands=["noti"])
def noti_cmd(msg):
    sync_group_locally(msg.chat)  # ← Dùng đúng tên biến
    handle_noti(bot, msg)
    
@bot.message_handler(commands=["time"])
def uptime(message):
    sync_group_locally(message.chat)
    uptime = datetime.datetime.now() - START_TIME
    bot.reply_to(message, f"⏳ Bot đã chạy: {str(uptime).split('.')[0]}")
    
# ===== NÚT CALLBACK =====

@bot.callback_query_handler(func=lambda call: call.data.startswith("retry|"))
def retry_button(call):
    handle_retry_button(bot, call)

@bot.callback_query_handler(func=lambda call: call.data.startswith("tts|"))
def tts_button(call):
    handle_tts_button(bot, call)

@bot.callback_query_handler(func=lambda call: call.data == "export_stats")
def export_stats_txt(call):
    from dataall_handler import export_stats_txt
    export_stats_txt(bot, call)

# ===== GHI NHẬN KHI BOT ĐƯỢC MỜI VÀO NHÓM =====

@bot.message_handler(func=lambda m: m.new_chat_members)
def greet_group_joined(message):
    handle_bot_added(bot, message)

# ===== GHI NHẬN BẤT KỲ AI CHAT VỚI BOT (PRIVATE + GROUP) =====

@bot.message_handler(func=lambda msg: True)
def track_all_chats(msg):
    if msg.chat.type in ['group', 'supergroup']:
        GROUPS.add(msg.chat.id)
        save_groups(GROUPS)
    sync_id_if_new(msg.chat)

# ===== KHỞI CHẠY =====

if __name__ == "__main__":
    bot.remove_webhook()
    bot.set_webhook(url=f"{APP_URL}/{TOKEN}")

    # 🧠 Load danh sách người dùng & nhóm để gửi xổ số
    ALL_USERS = set()
    for f in os.listdir():
        if f.startswith("memory_") and f.endswith(".json"):
            uid = f.replace("memory_", "").replace(".json", "")
            if uid.isdigit():
                ALL_USERS.add(int(uid))

    ALL_GROUPS = load_groups()
    ALL_RECIPIENTS = ALL_USERS.union(ALL_GROUPS)

    # ⏰ Gửi chào nhóm + xổ số mỗi chiều
    threading.Thread(target=auto_group_greeting, args=(bot, GROUPS)).start()
    auto_send_xoso(bot, ALL_RECIPIENTS)

    # 🚀 Chạy Flask
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 10000)))