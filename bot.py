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

from database import add_user, add_group, all_users, all_groups, users, remove_user
from configs import cfg

import random
import asyncio

# Initialize Bot Client
app = Client(
    "approver",
    api_id=cfg.API_ID,
    api_hash=cfg.API_HASH,
    bot_token=cfg.BOT_TOKEN
)

# ====================================================
#                   MAIN PROCESS
# ====================================================

@app.on_chat_join_request(filters.group | filters.channel)
async def approve(_, m: Message):
    chat = m.chat
    user = m.from_user
    try:
        add_group(chat.id)
        await app.approve_chat_join_request(chat.id, user.id)
        await app.send_photo(
            user.id,
            "https://i.ibb.co/F9JM2pq/photo-2025-03-13-19-25-04-7481377376551567376.jpg",
            caption=f"**🍁 Hᴇʏ {user.mention}!\n\nʏᴏᴜʀ ʀᴇǫᴜᴇsᴛ ʜᴀs ʙᴇᴇɴ ᴀᴘᴘʀᴏᴠᴇᴅ!.. ᴡᴇʟᴄᴏᴍᴇ ᴛᴏ  {chat.title}\n\n__<blockquote>ʙʏ: <a href=https://t.me/EmitingStars_Botz>Eᴍɪᴛɪɴɢ Sᴛᴀʀs</blockquote></a>__**"
        )
        add_user(user.id)
    except errors.PeerIdInvalid:
        print("User isn't a proper peer (possibly a group)")
    except Exception as err:
        print(str(err))

# ====================================================
#                      START
# ====================================================

@app.on_message(filters.private & filters.command("start"))
async def start_command(_, m: Message):
    try:
        await app.get_chat_member(cfg.CHID, m.from_user.id)
    except:
        try:
            invite_link = await app.create_chat_invite_link(cfg.CHID)
        except:
            return await m.reply("**Make Sure I Am Admin In Your Channel**")

        button = InlineKeyboardMarkup(
            [[
                InlineKeyboardButton("Jᴏɪɴ ᴄʜᴀɴɴᴇʟ", url=invite_link.invite_link),
                InlineKeyboardButton("ᴛʀʏ ᴀɢᴀɪɴ!", url="https://t.me/Private_Auto_Approval_Bot?start=start")
            ]]
        )
        return await m.reply_text(
            "**<blockquote>⚠️ Aᴄᴄᴇss ᴅᴇɴɪᴇᴅ! ⚠️\n\nYou must join the required channel first. Please do so and try again.</blockquote>**",
            reply_markup=button
        )

    add_user(m.from_user.id)
    keyboard = InlineKeyboardMarkup([
        [
            InlineKeyboardButton("Mᴀɪɴ Cʜᴀɴɴᴇʟ", url="https://t.me/EmitingStars_Botz"),
            InlineKeyboardButton("Sᴜᴘᴘᴏʀᴛ", url="https://t.me/+HZuPVe0l-F1mM2Jl")
        ],
        [
            InlineKeyboardButton("⤬ Kɪᴅɴᴀᴘᴘ Mᴇ Bᴀʙʏ ⤬", url="http://t.me/Private_Auto_Approval_Bot?startchannel=true")
        ]
    ])

    await m.reply_photo(
        "https://i.ibb.co/v6J0JM80/photo-2025-03-13-18-50-40-7481368571868610580.jpg",
        caption=f"**<blockquote>🍁 ʜᴇʟʟᴏ {m.from_user.mention}!</blockquote>\n<blockquote expandable>ɪ'ᴍ ᴀɴ ᴀᴜᴛᴏ ᴀᴘᴘʀᴏᴠᴇ ʙᴏᴛ. ᴀᴅᴅ ᴍᴇ ᴛᴏ ʏᴏᴜʀ ᴄʜᴀᴛ ᴀɴᴅ ᴘʀᴏᴍᴏᴛᴇ ᴍᴇ ᴛᴏ ᴀᴅᴍɪɴ ᴡɪᴛʜ ᴀᴅᴅ ᴍᴇᴍʙᴇʀs ᴘᴇʀᴍɪssɪᴏɴ.</blockquote>__**",
        reply_markup=keyboard
    )

# ====================================================
#                   CALLBACK CHECK
# ====================================================

@app.on_callback_query(filters.regex("chk"))
async def chk_callback(_, cb: CallbackQuery):
    try:
        await app.get_chat_member(cfg.CHID, cb.from_user.id)
    except:
        return await cb.answer(
            "Yᴏᴜ ʜᴀᴠᴇɴ'ᴛ ᴊᴏɪɴᴇᴅ ᴏᴜʀ ᴄʜᴀɴɴᴇʟ ʏᴇᴛ. Pʟᴇᴀsᴇ ᴊᴏɪɴ ᴀɴᴅ ᴛʀʏ ᴀɢᴀɪɴ..!",
            show_alert=True
        )

    keyboard = InlineKeyboardMarkup([
        [
            InlineKeyboardButton("Mᴀɪɴ Cʜᴀɴɴᴇʟ", url="https://t.me/EmitingStars_Botz"),
            InlineKeyboardButton("Sᴜᴘᴘᴏʀᴛ", url="https://t.me/+HZuPVe0l-F1mM2Jl")
        ],
        [
            InlineKeyboardButton("⤬ Kɪᴅɴᴀᴘᴘ Mᴇ Bᴀʙʏ ⤬", url="http://t.me/Private_Auto_Approval_Bot?startchannel=true")
        ]
    ])
    add_user(cb.from_user.id)
    await cb.edit_text(
        f"**<blockquote>🍁 ʜᴇʟʟᴏ {cb.from_user.mention}!</blockquote>\n<blockquote expandable>ɪ'ᴍ ᴀɴ ᴀᴜᴛᴏ ᴀᴘᴘʀᴏᴠᴇ ʙᴏᴛ...</blockquote>__**",
        reply_markup=keyboard
    )

# ====================================================
#                      INFO CMD
# ====================================================

@app.on_message(filters.command("users") & filters.user(cfg.SUDO))
async def dbtool(_, m: Message):
    total_users = all_users()
    total_groups = all_groups()
    total = total_users + total_groups
    await m.reply_text(
        f"🍀 **Chats Stats** 🍀\n"
        f"🙋‍♂️ Users : `{total_users}`\n"
        f"👥 Groups : `{total_groups}`\n"
        f"🚧 Total : `{total}`"
    )

# ====================================================
#                 BROADCAST (COPY)
# ====================================================

@app.on_message(filters.command("bcast") & filters.user(cfg.SUDO))
async def bcast(_, m: Message):
    lel = await m.reply("`⚡️ Processing...`")
    stats = {"success": 0, "failed": 0, "deactivated": 0, "blocked": 0}
    
    for u in users.find():
        try:
            await m.reply_to_message.copy(int(u["user_id"]))
            stats["success"] += 1
        except FloodWait as e:
            await asyncio.sleep(e.value)
        except errors.InputUserDeactivated:
            stats["deactivated"] += 1
            remove_user(u["user_id"])
        except errors.UserIsBlocked:
            stats["blocked"] += 1
        except:
            stats["failed"] += 1

    await lel.edit(
        f"✅ Successful: `{stats['success']}`\n"
        f"❌ Failed: `{stats['failed']}`\n"
        f"👾 Blocked: `{stats['blocked']}`\n"
        f"👻 Deactivated: `{stats['deactivated']}`"
    )

# ====================================================
#               BROADCAST (FORWARD)
# ====================================================

@app.on_message(filters.command("fcast") & filters.user(cfg.SUDO))
async def fcast(_, m: Message):
    lel = await m.reply("`⚡️ Processing...`")
    stats = {"success": 0, "failed": 0, "deactivated": 0, "blocked": 0}
    
    for u in users.find():
        try:
            await m.reply_to_message.forward(int(u["user_id"]))
            stats["success"] += 1
        except FloodWait as e:
            await asyncio.sleep(e.value)
        except errors.InputUserDeactivated:
            stats["deactivated"] += 1
            remove_user(u["user_id"])
        except errors.UserIsBlocked:
            stats["blocked"] += 1
        except:
            stats["failed"] += 1

    await lel.edit(
        f"✅ Successful: `{stats['success']}`\n"
        f"❌ Failed: `{stats['failed']}`\n"
        f"👾 Blocked: `{stats['blocked']}`\n"
        f"👻 Deactivated: `{stats['deactivated']}`"
    )

# ====================================================
#                    BOT START
# ====================================================

print("I'm Alive Now!")
app.run()
