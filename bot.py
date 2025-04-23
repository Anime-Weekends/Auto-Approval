# ====================================================
#               PRIVATE AUTO APPROVER BOT
# ----------------------------------------------------
# A Telegram bot that auto-approves users in groups
# and channels upon join requests. Includes support
# for forced subscription, stats, and broadcasting.
# ====================================================

from pyrogram.types import Message, InlineKeyboardButton, InlineKeyboardMarkup, CallbackQuery
from pyrogram import filters, Client, errors, enums
from pyrogram.errors import UserNotParticipant
from pyrogram.errors.exceptions.flood_420 import FloodWait
from pyrogram.enums import ParseMode
from pyrogram.errors import UserDeactivated, UserBlocked
from pyrogram.errors import PeerIdInvalid
from pyrogram.errors import RPCError

from database import add_user, add_group, all_users, all_groups, users, remove_user
from database import add_admin_db, remove_admin_db, list_admins_db, is_admin
from configs import cfg
from database import datetime
from database import is_sudo

import random
import asyncio

# Run as Bot (for inline buttons, messages, commands):
bot_app = Client(
    "bot_session",
    api_id=cfg.API_ID,
    api_hash=cfg.API_HASH,
    bot_token=cfg.BOT_TOKEN
)

# Run as User (for accessing private channels, etc):
user_app = Client(
    "user_session",
    api_id=cfg.API_ID,
    api_hash=cfg.API_HASH,
    session_string=cfg.STRING_SESSION
)

# ====================================================
#                   MAIN PROCESS
# ====================================================

@bot_app.on_chat_join_request(filters.group | filters.channel)
async def approve(_, m: Message):
    chat = m.chat
    user = m.from_user
    try:
        add_group(chat.id)
        await app.approve_chat_join_request(chat.id, user.id)
        
        # Inline buttons layout
        keyboard = InlineKeyboardMarkup(
            [
                [InlineKeyboardButton("⚡", callback_data="popup_action")],  # Button with callback
                [
                    InlineKeyboardButton("Mᴀɪɴ Cʜᴀɴɴᴇʟ", url="https://t.me/EmitingStars_Botz"),
                    InlineKeyboardButton("Sᴜᴘᴘᴏʀᴛ", url="https://t.me/Private_Auto_Approval_Bot")
                ]
            ]
        )

        # Caption with user and chat links
        caption = (
            f"🍁 <b>Hey</b> <a href='tg://user?id={user.id}'>{user.first_name}</a>!\n\n"
            f"Your request has been approved! Welcome to "
            f"<a href='https://t.me/c/{str(chat.id)[4:]}'>{chat.title}</a>\n\n"
            f"<i>By: <a href='https://t.me/EmitingStars_Botz'>Emiting Stars</a></i>"
        )
        
        # Sending a photo with the message and buttons
        await app.send_photo(
            user.id,
            "https://i.ibb.co/F9JM2pq/photo-2025-03-13-19-25-04-7481377376551567376.jpg",
            caption=caption,
            reply_markup=keyboard,
            parse_mode=ParseMode.HTML,
            message_effect_id=5104841245755180586 #🔥
        )
        add_user(user.id)

    except errors.PeerIdInvalid:
        print("User isn't a proper peer (possibly a group)")
    except Exception as err:
        print(str(err))


# Callback query handler for the "⚡" button to show a popup message
@bot_app.on_callback_query(filters.regex("popup_action"))
async def popup_action(_, cb: CallbackQuery):
    # This sends the popup-style alert when the "⚡" button is clicked
    await cb.answer("This is a popup message!", show_alert=True)
    
# ====================================================
#                      START
# ====================================================

from pyrogram.types import InputMediaPhoto


@bot_app.on_message(filters.private & filters.command("start"))
async def start_command(_, m: Message):
    try:
        await app.get_chat_member(cfg.CHID, m.from_user.id)
    except:
        try:
            invite_link = await app.create_chat_invite_link(cfg.CHID)
        except:
            return await m.reply("**Make sure I am an admin in your channel**")

        button = InlineKeyboardMarkup(
            [[
                InlineKeyboardButton("Join Channel", url=invite_link.invite_link),
                InlineKeyboardButton("Try Again", url="https://t.me/Private_Auto_Approval_Bot?start=start")
            ]]
        )

        return await m.reply_photo(
            photo="https://i.ibb.co/C5N2Xhk9/photo-2025-04-19-18-11-35-7496424313436766224.jpg",
            caption="⚠️ <b>Access Denied!</b>\n\nYou must join the required channel first. Please do so and try again.",
            reply_markup=button,
            parse_mode=ParseMode.HTML
        )

    add_user(m.from_user.id)

    keyboard = InlineKeyboardMarkup([
        [
            InlineKeyboardButton("Main Channel", url="https://t.me/EmitingStars_Botz"),
            InlineKeyboardButton("Support", url="https://t.me/+HZuPVe0l-F1mM2Jl")
        ],
        [
            InlineKeyboardButton("⤬ Kidnapp Me Baby ⤬", url="http://t.me/Private_Auto_Approval_Bot?startchannel=true")
        ]
    ])

    await m.reply_photo(
        "https://i.ibb.co/v6J0JM80/photo-2025-03-13-18-50-40-7481368571868610580.jpg",
        caption=(
            f"🍁 <b>Hello</b> <a href='tg://user?id={m.from_user.id}'>{m.from_user.first_name}</a>!\n\n"
            "I'm an auto-approve bot. Add me to your chat and promote me to admin "
            "with <b>Add Members</b> permission."
        ),
        reply_markup=keyboard,
        parse_mode=ParseMode.HTML,
        message_effect_id=5104841245755180586 #🔥
    )

# ====================================================
#                   CALLBACK CHECK
# ====================================================

@bot_app.on_callback_query(filters.regex("chk"))
async def chk_callback(_, cb: CallbackQuery):
    try:
        await app.get_chat_member(cfg.CHID, cb.from_user.id)
    except:
        return await cb.answer(
            "You haven't joined our channel yet. Please join and try again!",
            show_alert=True
        )

    keyboard = InlineKeyboardMarkup([
        [
            InlineKeyboardButton("Main Channel", url="https://t.me/EmitingStars_Botz"),
            InlineKeyboardButton("Support", url="https://t.me/+HZuPVe0l-F1mM2Jl")
        ],
        [
            InlineKeyboardButton("⤬ Kidnapp Me Baby ⤬", url="http://t.me/Private_Auto_Approval_Bot?startchannel=true")
        ]
    ])

    add_user(cb.from_user.id)

    await cb.edit_message_text(
        f"🍁 <b>Hello</b> {cb.from_user.mention()}!\n\n"
        "I'm an <b>auto-approve bot</b>. Add me to your chat and promote me to admin "
        "with <b>Add Members</b> permission.",
        reply_markup=keyboard,
        parse_mode=ParseMode.HTML
    )

# ====================================================
#                      INFO CMD
# ====================================================

@bot_app.on_message(filters.command("users") & is_sudo())
async def dbtool(_, m: Message):
    total_users = all_users()
    total_groups = all_groups()
    total = total_users + total_groups

    user_percent = (total_users / total) * 100 if total else 0
    group_percent = (total_groups / total) * 100 if total else 0

    keyboard = InlineKeyboardMarkup([
        [InlineKeyboardButton("✖ Close", callback_data="close_stats")]
    ])

    timestamp = datetime.now().strftime("%d %b %Y • %I:%M %p")

    caption = (
        f"**📊 Chat Statistics**\n\n"
        f"👤 Users: `{total_users}` ({user_percent:.1f}%)\n"
        f"👥 Groups: `{total_groups}` ({group_percent:.1f}%)\n"
        f"📦 Total Chats: `{total}`\n\n"
        f"🕒 Last Updated: `{timestamp}`"
    )

    await m.reply_photo(
        photo="https://i.ibb.co/F9JM2pq/photo-2025-03-13-19-25-04-7481377376551567376.jpg",
        caption=caption,
        reply_markup=keyboard,
        parse_mode=ParseMode.MARKDOWN
    )
    
@bot_app.on_callback_query(filters.regex("close_stats"))
async def close_stats(_, cb: CallbackQuery):
    await cb.message.delete()
    await cb.answer("Closed!", show_alert=True)
    
# ====================================================
#                 BROADCAST (COPY)
# ====================================================

@bot_app.on_message(filters.command("bcast") & is_sudo())
async def bcast(_, m: Message):
    global canceled
    canceled = False

    # Sending the initial message with photo and inline buttons
    lel = await m.reply_photo(
        "https://i.ibb.co/F9JM2pq/photo-2025-03-13-19-25-04-7481377376551567376.jpg",
        caption="`⚡️ Processing...`",
        reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton("Cancel", callback_data="cancel_bcast"),
                    InlineKeyboardButton("Close", callback_data="close_bcast")
                ]
            ]
        )
    )

    # Get total number of users from the database
    total_users = users.count_documents({})
    stats = {"success": 0, "failed": 0, "deactivated": 0, "blocked": 0}

    # Loop through all users and broadcast the message
    for idx, u in enumerate(users.find(), 1):
        if canceled:
            await lel.edit(
                "❌ Broadcast process has been canceled.",
                reply_markup=InlineKeyboardMarkup(
                    [[InlineKeyboardButton("Close", callback_data="close_bcast")]]
                )
            )
            break

        # Calculate progress for the broadcast
        progress = int((idx / total_users) * 100)
        bars = int(progress / 5)
        progress_bar = f"[{'█' * bars}{'—' * (20 - bars)}] {progress}%"

        # Update the user with the progress
        await lel.edit(
            f"📣 Broadcasting...\n\n"
            f"{progress_bar}\n\n"
            f"✅ Success: `{stats['success']}` | ❌ Failed: `{stats['failed']}`\n"
            f"👻 Deactivated: `{stats['deactivated']}` | 🚫 Blocked: `{stats['blocked']}`",
            reply_markup=InlineKeyboardMarkup(
                [[
                    InlineKeyboardButton("Cancel", callback_data="cancel_bcast"),
                    InlineKeyboardButton("Close", callback_data="close_bcast")
                ]]
            )
        )

        # Try to forward the message to the user
        try:
            await m.reply_to_message.copy(int(u["user_id"]))
            stats["success"] += 1
        except UserDeactivated:
            stats["deactivated"] += 1
            # Remove the user from the database if they are deactivated
            users.delete_one({"user_id": u["user_id"]})
        except UserBlocked:
            stats["blocked"] += 1
        except Exception as e:
            stats["failed"] += 1
            print(f"Error with user {u['user_id']}: {e}")

        # To prevent rate limiting, give some time between messages
        await asyncio.sleep(0.1)

    # After the broadcast is done, update the user on the status
    if not canceled:
        await lel.edit(
            f"✅ Broadcast finished!\n\n"
            f"✅ Successful: `{stats['success']}`\n"
            f"❌ Failed: `{stats['failed']}`\n"
            f"👾 Blocked: `{stats['blocked']}`\n"
            f"👻 Deactivated: `{stats['deactivated']}`",
            reply_markup=InlineKeyboardMarkup(
                [[InlineKeyboardButton("Close", callback_data="close_bcast")]]
            )
        )

# === Cancel Button Callback ===
@bot_app.on_callback_query(filters.regex("cancel_bcast"))
async def cancel_bcast(_, cb):
    global canceled
    canceled = True
    await cb.answer("Broadcast has been canceled.")
    await cb.message.edit(
        "❌ Broadcast process has been canceled.",
        reply_markup=InlineKeyboardMarkup(
            [[InlineKeyboardButton("Close", callback_data="close_bcast")]]
        )
    )

# === Close Button Callback ===
@bot_app.on_callback_query(filters.regex("close_bcast"))
async def close_bcast(_, cb):
    await cb.message.delete()
    await cb.answer()

# ====================================================
#               BROADCAST (FORWARD)
# ====================================================

@bot_app.on_message(filters.command("fcast") & is_sudo())
async def fcast(_, m: Message):
    global canceled
    canceled = False

    lel = await m.reply_photo(
        "https://i.ibb.co/F9JM2pq/photo-2025-03-13-19-25-04-7481377376551567376.jpg",
        caption="`⚡️ Processing...`",
        reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton("Cancel", callback_data="cancel_fcast"),
                    InlineKeyboardButton("Close", callback_data="close_fcast")
                ]
            ]
        )
    )

    total_users = users.count_documents({})
    stats = {"success": 0, "failed": 0, "deactivated": 0, "blocked": 0}

    for idx, u in enumerate(users.find(), 1):
        if canceled:
            await lel.edit(
                "❌ Broadcast process has been canceled.",
                reply_markup=InlineKeyboardMarkup(
                    [[InlineKeyboardButton("Close", callback_data="close_fcast")]]
                )
            )
            break

        progress = int((idx / total_users) * 100)
        bars = int(progress / 5)
        progress_bar = f"[{'█' * bars}{'—' * (20 - bars)}] {progress}%"

        await lel.edit(
            f"📣 Broadcasting...\n\n"
            f"{progress_bar}\n\n"
            f"✅ Success: `{stats['success']}` | ❌ Failed: `{stats['failed']}`\n"
            f"👻 Deactivated: `{stats['deactivated']}` | 🚫 Blocked: `{stats['blocked']}`",
            reply_markup=InlineKeyboardMarkup(
                [[
                    InlineKeyboardButton("Cancel", callback_data="cancel_fcast"),
                    InlineKeyboardButton("Close", callback_data="close_fcast")
                ]]
            )
        )

        try:
            await m.reply_to_message.forward(int(u["user_id"]))
            stats["success"] += 1
        except FloodWait as e:
            await asyncio.sleep(e.value)
        except errors.InputUserDeactivated:
            stats["deactivated"] += 1
            remove_user(u["user_id"])  # Remove deactivated user
        except errors.UserIsBlocked:
            stats["blocked"] += 1
        except Exception:
            stats["failed"] += 1

        await asyncio.sleep(0.1)

    if not canceled:
        await lel.edit(
            f"✅ Broadcast finished!\n\n"
            f"✅ Successful: `{stats['success']}`\n"
            f"❌ Failed: `{stats['failed']}`\n"
            f"👾 Blocked: `{stats['blocked']}`\n"
            f"👻 Deactivated: `{stats['deactivated']}`",
            reply_markup=InlineKeyboardMarkup(
                [[InlineKeyboardButton("Close", callback_data="close_fcast")]]
            )
        )

# === Cancel Button Callback ===
@bot_app.on_callback_query(filters.regex("cancel_fcast"))
async def cancel_fcast(_, cb):
    global canceled
    canceled = True
    await cb.answer("Broadcast has been canceled.")
    await cb.message.edit(
        "❌ Broadcast process has been canceled.",
        reply_markup=InlineKeyboardMarkup(
            [[InlineKeyboardButton("Close", callback_data="close_fcast")]]
        )
    )

# === Close Button Callback ===
@bot_app.on_callback_query(filters.regex("close_fcast"))
async def close_fcast(_, cb):
    await cb.message.delete()
    await cb.answer()

# ====================================================
#                    HELP CENTER
# ====================================================

@bot_app.on_message(filters.private & filters.command("help"))
async def help_command(_, m: Message):
    keyboard = InlineKeyboardMarkup([
        [InlineKeyboardButton("🛠 Bot Guide", url="https://t.me/YourBotGuide")],  # Row 1
        [
            InlineKeyboardButton("👨‍💻 Support", url="https://t.me/YourSupportChannel"),
            InlineKeyboardButton("📢 Main Channel", url="https://t.me/YourMainChannel")
        ],  # Row 2
        [InlineKeyboardButton("✖ Close", callback_data="close_help")]  # Row 3
    ])

    await m.reply_photo(
        "https://i.ibb.co/F9JM2pq/photo-2025-03-13-19-25-04-7481377376551567376.jpg",
        caption=(
            "<b>How to use the bot:</b>\n\n"
            "• Use the guide for full instructions.\n"
            "• Join our support and main channels.\n"
            "• Click close to dismiss this message."
        ),
        reply_markup=keyboard,
        parse_mode=ParseMode.HTML
    )

@bot_app.on_callback_query(filters.regex("close_help"))
async def close_help(_, cb: CallbackQuery):
    await cb.message.delete()

# ====================================================
#                    ADMIMS
# ====================================================

@bot_app.on_message(filters.command("addadmin") & filters.user(cfg.SUDO))
async def addadmin(_, m: Message):
    if len(m.command) < 2 or not all(x.isdigit() for x in m.command[1:]):
        return await m.reply(
            "Yᴏᴜ ɴᴇᴇᴅ ᴛᴏ ᴀᴅᴅ Aᴅᴍɪɴ ɪᴅs\n"
            "<b><blockquote>EXAMPLE:</b>\n"
            "/addadmin 123456789 — ᴀᴅᴅ ᴏɴᴇ ᴜsᴇʀ\n"
            "/addadmin 123456789 987654321 — ᴀᴅᴅ ᴍᴜʟᴛɪᴘʟᴇ ᴜsᴇʀs</blockquote>",
            parse_mode=ParseMode.HTML,
            reply_markup=InlineKeyboardMarkup(
                [[InlineKeyboardButton("✖️ Close", callback_data="close_msg")]]
            )
        )

    added = []
    for user_id in m.command[1:]:
        uid = int(user_id)
        if not is_admin(uid):
            add_admin_db(uid)
            added.append(uid)

    if not added:
        return await m.reply(
            "All provided users are already admins.",
            parse_mode=ParseMode.HTML,
            reply_markup=InlineKeyboardMarkup(
                [[InlineKeyboardButton("✖️ Close", callback_data="close_msg")]]
            )
        )

    added_text = "\n".join([f"• <a href='tg://user?id={uid}'>{uid}</a>" for uid in added])
    await m.reply(
        f"✅ The following user(s) were added as admins:\n{added_text}",
        parse_mode=ParseMode.HTML,
        reply_markup=InlineKeyboardMarkup(
            [[InlineKeyboardButton("✖️ Close", callback_data="close_msg")]]
        )
    )


@bot_app.on_message(filters.command("removeadmin") & filters.user(cfg.SUDO))
async def removeadmin(_, m: Message):
    args = m.command[1:]

    if not args:
        return await m.reply(
            "⁉️ Pʟᴇᴀsᴇ, Pʀᴏᴠɪᴅᴇ ᴠᴀʟɪᴅ ɪᴅs ᴏʀ ᴀʀɢᴜᴍᴇɴᴛs\n\n"
            "<b><blockquote>EXAMPLES:</b>\n"
            "/removeadmin 123456789 — ᴛᴏ ᴅᴇʟᴇᴛᴇ ᴏɴᴇ sᴘᴇᴄɪғɪᴇᴅ ɪᴅ\n"
            "/removeadmin 123456789 987654321 — ᴛᴏ ᴅᴇʟᴇᴛᴇ ᴍᴜʟᴛɪᴘʟᴇ sᴘᴇᴄɪғɪᴇᴅ ɪᴅs\n"
            "/removeadmin all — ᴛᴏ ᴅᴇʟᴇᴛᴇ ᴀʟʟ ᴀᴅᴍɪɴs</blockquote>",
            parse_mode=ParseMode.HTML,
            reply_markup=InlineKeyboardMarkup(
                [[InlineKeyboardButton("✖️ Close", callback_data="close_msg")]]
            )
        )

    if args[0].lower() == "all":
        all_admins = list_admins_db()
        if not all_admins:
            return await m.reply("No admins found to remove.")
        for admin in all_admins:
            remove_admin_db(admin)
        return await m.reply(
            "✅ All admins have been removed.",
            parse_mode=ParseMode.HTML,
            reply_markup=InlineKeyboardMarkup(
                [[InlineKeyboardButton("✖️ Close", callback_data="close_msg")]]
            )
        )

    if not all(x.isdigit() for x in args):
        return await m.reply("❌ Please enter valid numeric user IDs.")

    removed = []
    for user_id in args:
        uid = int(user_id)
        if is_admin(uid):
            remove_admin_db(uid)
            removed.append(uid)

    if not removed:
        return await m.reply(
            "No admin found with the provided IDs.",
            parse_mode=ParseMode.HTML,
            reply_markup=InlineKeyboardMarkup(
                [[InlineKeyboardButton("✖️ Close", callback_data="close_msg")]]
            )
        )

    removed_text = "\n".join([f"• <a href='tg://user?id={uid}'>{uid}</a>" for uid in removed])
    await m.reply(
        f"✅ The following admin(s) were removed:\n{removed_text}",
        parse_mode=ParseMode.HTML,
        reply_markup=InlineKeyboardMarkup(
            [[InlineKeyboardButton("✖️ Close", callback_data="close_msg")]]
        )
    )


@bot_app.on_message(filters.command("listadmin") & is_sudo())
async def listadmin(_, m: Message):
    admin_ids = list_admins_db()
    if not admin_ids:
        return await m.reply(
            "No admins found.",
            parse_mode=ParseMode.HTML,
            reply_markup=InlineKeyboardMarkup(
                [[InlineKeyboardButton("✖️ Close", callback_data="close_msg")]]
            )
        )

    text = "<b>🤖 𝗕𝗢𝗧 𝗔𝗗𝗠𝗜𝗡𝗦 𝗟𝗜𝗦𝗧 :</b>\n\n"
    for uid in admin_ids:
        try:
            user = await _.get_users(uid)
            name = user.mention(style="html")
        except:
            name = f"<a href='tg://user?id={uid}'>Unknown</a>"
        text += f"{name}\nID: <code>{uid}</code>\n\n"

    await m.reply_photo(
        photo="https://i.ibb.co/F9JM2pq/photo-2025-03-13-19-25-04-7481377376551567376.jpg",
        caption=text,
        parse_mode=ParseMode.HTML,
        reply_markup=InlineKeyboardMarkup(
            [[InlineKeyboardButton("✖️ Close", callback_data="close_msg")]]
        )
    )


@bot_app.on_callback_query(filters.regex("close_msg"))
async def close_msg_cb(_, cb):
    await cb.message.delete()
    await cb.answer()
    
def is_sudo():
    return filters.create(lambda _, __, m: m.from_user and (m.from_user.id in cfg.SUDO or is_admin(m.from_user.id)))

# ====================================================
#                   TESTING PURPOSE
# ====================================================

@user_app.on_message(filters.command("acceptall"))
async def accept_all(_, m: Message):
    try:
        async for req in app.get_chat_join_requests(m.chat.id):
            await app.approve_chat_join_request(m.chat.id, req.user.id)
        await m.reply("✅ All pending requests have been accepted successfully.")
    except PeerIdInvalid:
        await m.reply("❌ Invalid group/channel ID.")
    except RPCError as err:
        await m.reply(f"⚠️ Telegram Error: {err}")
    except Exception as err:
        await m.reply(f"⚠️ Unexpected Error: {err}")


# Reject All Join Requests with Confirmation
@user_app.on_message(filters.command("rejectall"))
async def reject_all(_, m: Message):
    keyboard = InlineKeyboardMarkup([
        [InlineKeyboardButton("✅ Yes", callback_data="reject_all_confirm"),
         InlineKeyboardButton("❌ No", callback_data="reject_all_cancel")]
    ])
    await m.reply("Are you sure you want to reject all pending join requests?", reply_markup=keyboard)


# Confirm rejection
@user_app.on_callback_query(filters.regex("reject_all_confirm"))
async def reject_all_confirm(_, cb: CallbackQuery):
    try:
        async for req in app.get_chat_join_requests(cb.message.chat.id):
            await app.decline_chat_join_request(cb.message.chat.id, req.user.id)
        await cb.answer("All requests rejected.", show_alert=True)
        await cb.message.edit("❌ All pending join requests have been rejected.")
    except PeerIdInvalid:
        await cb.answer("Invalid chat ID.", show_alert=True)
    except RPCError as err:
        await cb.answer(f"Telegram Error: {err}", show_alert=True)
    except Exception as err:
        await cb.answer(f"Unexpected Error: {err}", show_alert=True)


# Cancel rejection
@user_app.on_callback_query(filters.regex("reject_all_cancel"))
async def reject_all_cancel(_, cb: CallbackQuery):
    await cb.answer("Action cancelled.", show_alert=True)
    await cb.message.edit("❎ Rejection of pending join requests has been cancelled.")

# ====================================================
#                    BOT START
# ====================================================

print("I'm Alive Now!")
app.run()
