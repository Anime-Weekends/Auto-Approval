from pymongo import MongoClient
from datetime import datetime
from configs import cfg

client = MongoClient(cfg.MONGO_URI)

db = client['main']
users = db['users']
groups = db['groups']
admins = db['admins']  # Collection for custom admins


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

# === Sudo Checker ===
from pyrogram import filters

def is_sudo():
    return filters.create(lambda _, __, m: m.from_user and (
        m.from_user.id in cfg.SUDO or is_admin(m.from_user.id)
    ))
