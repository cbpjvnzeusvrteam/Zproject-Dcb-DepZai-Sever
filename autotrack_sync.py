import os, json, time, threading, requests

SYNC_URL = "https://zcode.x10.mx/save_group.php"
SENT_FILE = "synced_ids.json"
SENT_IDS = set()

def get_all_ids():
    ids = set()
    for f in os.listdir():
        if f.startswith("memory_") and f.endswith(".json"):
            uid = f.replace("memory_", "").replace(".json", "")
            if uid.isdigit():
                ids.add(int(uid))
    if os.path.exists("groups.json"):
        try:
            groups = json.load(open("groups.json"))
            ids.update(groups)
        except:
            pass
    return ids

def load_sent_ids():
    global SENT_IDS
    if os.path.exists(SENT_FILE):
        SENT_IDS = set(json.load(open(SENT_FILE)))

def save_sent_ids():
    json.dump(list(SENT_IDS), open(SENT_FILE, "w"))

def sync_loop():
    while True:
        try:
            all_ids = get_all_ids()
            new_ids = all_ids - SENT_IDS
            for gid in new_ids:
                try:
                    payload = {
                        "group_id": gid,
                        "group_name": f"ID {gid}" if gid < 0 else "Người dùng",
                        "username": ""
                    }
                    requests.post(SYNC_URL, json=payload, timeout=5)
                    print(f"[SYNC] + {gid}")
                    SENT_IDS.add(gid)
                except Exception as e:
                    print(f"[SYNC] ⚠️ {gid}: {e}")
            save_sent_ids()
        except Exception as e:
            print(f"[SYNC] Lỗi: {e}")
        time.sleep(1)

def start_auto_sync():
    load_sent_ids()
    threading.Thread(target=sync_loop, daemon=True).start()