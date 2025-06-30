import requests

SYNC_URL = "https://zcode.x10.mx/save_group.php"
SENT_CACHE = set()

def sync_id_if_new(chat):
    chat_id = chat.id
    if chat_id in SENT_CACHE:
        return

    group_name = getattr(chat, 'title', '') or f"ID {chat_id}"
    username = getattr(chat, 'username', '') or ""

    try:
        requests.post(SYNC_URL, json={
            "group_id": chat_id,
            "group_name": group_name,
            "username": username
        }, timeout=5)
        print(f"📡 Synced: {chat_id} - {group_name}")
        SENT_CACHE.add(chat_id)
    except Exception as e:
        print(f"❌ Sync ID {chat_id} lỗi: {e}")