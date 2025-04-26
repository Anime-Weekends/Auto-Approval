from pymongo import MongoClient
from datetime import datetime
from pyrogram import filters
from configs import cfg

# === MongoDB Client Setup ===
client = MongoClient(cfg.MONGO_URI)

# === Database & Collections ===
db = client['main']
users = db['users']
groups = db['groups']
admins = db['admins']
logs = db['logs']  # For logging actions like /acceptall, /rejectall
counters = db['command_counters']  # For tracking command usage count
approvals = db['approvals']  # For tracking approved users

# === New Collections for Banned Users and Banned Channels ===
banned_users = db['banned_users']  # For tracking banned users
banned_channels = db['banned_channels']  # For tracking banned channels 

# === MongoDB Connection Management ===
def close_db_connection():
    client.close()
    print("MongoDB connection closed.")

def reconnect_db():
    global client, db, users, groups, admins, logs, counters, approvals
    client = MongoClient(cfg.MONGO_URI)
    db = client['main']
    users = db['users']
    groups = db['groups']
    admins = db['admins']
    logs = db['logs']
    counters = db['command_counters']
    approvals = db['approvals']
    print("MongoDB connection re-established.")

# === Users ===
def already_db(user_id):
    return bool(users.find_one({"user_id": str(user_id)}))

def add_user(user_id):
    if not already_db(user_id):
        users.insert_one({
            "user_id": str(user_id),
            "joined_at": datetime.utcnow().isoformat()
        })

def remove_user(user_id):
    if already_db(user_id):
        users.delete_one({"user_id": str(user_id)})

def all_users():
    return users.count_documents({})

# === Groups ===
def already_dbg(chat_id):
    return bool(groups.find_one({"chat_id": str(chat_id)}))

def add_group(chat_id):
    if not already_dbg(chat_id):
        groups.insert_one({
            "chat_id": str(chat_id),
            "joined_at": datetime.utcnow().isoformat()
        })

def all_groups():
    return groups.count_documents({})

# === Admins ===
def is_admin(user_id):
    return bool(admins.find_one({"user_id": int(user_id)}))

def add_admin_db(user_id):
    if not is_admin(user_id):
        admins.insert_one({"user_id": int(user_id)})

def remove_admin_db(user_id):
    admins.delete_one({"user_id": int(user_id)})

def list_admins_db():
    return [admin["user_id"] for admin in admins.find()]

# === Logging Actions ===
def log_action(user_id, chat_id, action_type):
    logs.insert_one({
        "user_id": int(user_id),
        "chat_id": int(chat_id),
        "action": action_type,
        "timestamp": datetime.utcnow().isoformat()
    })

# === Command Counter ===
def increment_command_count(command_name):
    counters.update_one(
        {"command": command_name},
        {"$inc": {"count": 1}},
        upsert=True
    )

def get_command_count(command_name):
    cmd = counters.find_one({"command": command_name})
    return cmd["count"] if cmd else 0

# === Sudo Checker ===
def is_sudo():
    return filters.create(lambda _, __, m: m.from_user and (
        m.from_user.id in cfg.SUDO or is_admin(m.from_user.id)
    ))

# === Approvals Tracker ===
def log_approval(user_id, chat_id):
    approvals.insert_one({
        "user_id": int(user_id),
        "chat_id": int(chat_id),
        "timestamp": datetime.utcnow()
    })

def get_total_approvals():
    return approvals.count_documents({})

# === Approval + Logging Wrapper ===
async def approve_and_log(bot, chat_id, user_id):
    await bot.approve_chat_join_request(chat_id, user_id)
    log_approval(user_id, chat_id)

# === Banned Users ===
banned_users = db['banned_users']

def ban_user(user_id):
    if not is_banned_user(user_id):
        banned_users.insert_one({
            "user_id": int(user_id),
            "banned_at": datetime.utcnow().isoformat()
        })

def unban_user(user_id):
    banned_users.delete_one({"user_id": int(user_id)})

def is_banned_user(user_id):
    return bool(banned_users.find_one({"user_id": int(user_id)}))

def all_banned_users():
    return [doc["user_id"] for doc in banned_users.find()]

# === Banned Channels ===
banned_channels = db['banned_channels']

def ban_channel(chat_id):
    if not is_banned_channel(chat_id):
        banned_channels.insert_one({
            "chat_id": int(chat_id),
            "banned_at": datetime.utcnow().isoformat()
        })

def unban_channel(chat_id):
    banned_channels.delete_one({"chat_id": int(chat_id)})

def is_banned_channel(chat_id):
    return bool(banned_channels.find_one({"chat_id": int(chat_id)}))

def all_banned_channels():
    return [doc["chat_id"] for doc in banned_channels.find()]
