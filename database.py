from pymongo import MongoClient, errors
from datetime import datetime
from pyrogram import filters
from configs import cfg

# === MongoDB Client Setup ===
client = MongoClient(cfg.MONGO_URI, serverSelectionTimeoutMS=5000)

# === Database & Collections ===
db = client['main']
users = db['users']
groups = db['groups']
admins = db['admins']
logs = db['logs']  # For logging actions like /acceptall, /rejectall
counters = db['command_counters']  # For tracking command usage count
approvals = db['approvals']  # For tracking approved users

# === MongoDB Connection Management ===
def close_db_connection():
    """Close the MongoDB connection."""
    try:
        client.close()
        print("MongoDB connection closed.")
    except errors.PyMongoError as e:
        print(f"Error closing MongoDB connection: {e}")

def reconnect_db():
    """Re-establish the MongoDB connection."""
    global client, db, users, groups, admins, logs, counters, approvals
    try:
        client = MongoClient(cfg.MONGO_URI, serverSelectionTimeoutMS=5000)
        db = client['main']
        users = db['users']
        groups = db['groups']
        admins = db['admins']
        logs = db['logs']
        counters = db['command_counters']
        approvals = db['approvals']
        print("MongoDB connection re-established.")
    except Exception as e:
        print(f"Error reconnecting to MongoDB: {e}")

# === Users ===
def already_db(user_id):
    """Check if a user exists in the database."""
    return bool(users.find_one({"user_id": user_id}))  # Use int for consistency

def add_user(user_id):
    """Add a new user to the database."""
    try:
        if not already_db(user_id):
            users.insert_one({
                "user_id": user_id,
                "joined_at": datetime.utcnow()
            })
    except errors.PyMongoError as e:
        print(f"Error adding user {user_id}: {e}")

def remove_user(user_id):
    """Remove a user from the database."""
    try:
        if already_db(user_id):
            users.delete_one({"user_id": user_id})
    except errors.PyMongoError as e:
        print(f"Error removing user {user_id}: {e}")

def all_users():
    """Return the count of all users in the database."""
    return users.estimated_document_count()

# === Groups ===
def already_dbg(chat_id):
    """Check if a group exists in the database."""
    return bool(groups.find_one({"chat_id": chat_id}))  # Use int for consistency

def add_group(chat_id):
    """Add a new group to the database."""
    try:
        if not already_dbg(chat_id):
            groups.insert_one({
                "chat_id": chat_id,
                "joined_at": datetime.utcnow()
            })
    except errors.PyMongoError as e:
        print(f"Error adding group {chat_id}: {e}")

def all_groups():
    """Return the count of all groups in the database."""
    return groups.estimated_document_count()

# === Admins ===
def is_admin(user_id):
    """Check if a user is an admin."""
    return bool(admins.find_one({"user_id": user_id}))

def add_admin_db(user_id):
    """Add a user as an admin to the database."""
    try:
        if not is_admin(user_id):
            admins.insert_one({"user_id": user_id})
    except errors.PyMongoError as e:
        print(f"Error adding admin {user_id}: {e}")

def remove_admin_db(user_id):
    """Remove a user from the admin list in the database."""
    try:
        admins.delete_one({"user_id": user_id})
    except errors.PyMongoError as e:
        print(f"Error removing admin {user_id}: {e}")

def list_admins_db():
    """Return a list of all admin user IDs."""
    return [admin["user_id"] for admin in admins.find()]

# === Logging Actions ===
def log_action(user_id, chat_id, action_type):
    """Log an action performed by a user in a group."""
    try:
        logs.insert_one({
            "user_id": user_id,
            "chat_id": chat_id,
            "action": action_type,
            "timestamp": datetime.utcnow()
        })
    except errors.PyMongoError as e:
        print(f"Error logging action for user {user_id} in group {chat_id}: {e}")

# === Command Counter ===
def increment_command_count(command_name):
    """Increment the count for a specific command."""
    try:
        counters.update_one(
            {"command": command_name},
            {"$inc": {"count": 1}},
            upsert=True
        )
    except errors.PyMongoError as e:
        print(f"Error incrementing count for command {command_name}: {e}")

def get_command_count(command_name):
    """Get the count of a specific command."""
    cmd = counters.find_one({"command": command_name})
    return cmd["count"] if cmd else 0

# === Sudo Checker ===
def is_sudo():
    """Check if a user is a sudo user or admin."""
    return filters.create(lambda _, __, m: m.from_user and (
        m.from_user.id in cfg.SUDO or is_admin(m.from_user.id)
    ))

# === Approvals Tracker ===
def log_approval(user_id, chat_id):
    """Log a user approval in a group."""
    try:
        if not approvals.find_one({"user_id": user_id, "chat_id": chat_id}):
            approvals.insert_one({
                "user_id": user_id,
                "chat_id": chat_id,
                "timestamp": datetime.utcnow()
            })
    except errors.PyMongoError as e:
        print(f"Error logging approval for user {user_id} in group {chat_id}: {e}")

def get_total_approvals():
    """Return the total number of approvals."""
    return approvals.count_documents({})

# === Approval + Logging Wrapper ===
async def approve_and_log(bot, chat_id, user_id):
    """Approve a join request and log the approval."""
    await bot.approve_chat_join_request(chat_id, user_id)
    log_approval(user_id, chat_id)

# === Ensure Indexes ===
def create_indexes():
    """Ensure that indexes are created for commonly queried fields."""
    try:
        users.create_index("user_id")  # Index on user_id for fast lookups
        groups.create_index("chat_id")  # Index on chat_id for fast lookups
        admins.create_index("user_id")  # Index on user_id for admin lookups
        logs.create_index([("user_id", 1), ("chat_id", 1)])  # Compound index for user_id and chat_id
        approvals.create_index([("user_id", 1), ("chat_id", 1)])  # Compound index for user_id and chat_id
        print("Indexes created.")
    except errors.PyMongoError as e:
        print(f"Error creating indexes: {e}")

# Call `create_indexes` when the bot starts to ensure indexes exist
create_indexes()
