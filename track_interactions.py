import json

GROUPS_FILE = "groups.json"
TEMP_GROUPS = set()

def sync_group_locally(chat):
    if chat.type not in ["group", "supergroup"]:
        return

    group_id = chat.id
    if group_id in TEMP_GROUPS:
        return

    TEMP_GROUPS.add(group_id)
    try:
        with open(GROUPS_FILE, "w") as f:
            json.dump(list(TEMP_GROUPS), f)
        print(f"📝 Lưu nhóm local: {group_id}")
    except Exception as e:
        print(f"❌ Ghi group.json lỗi: {e}")