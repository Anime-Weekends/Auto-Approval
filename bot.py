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
from pyrogram.enums import ChatMemberStatus, ParseMode
from pyrogram.errors import UserDeactivated, UserIsBlocked as UserBlocked
from pyrogram.errors import PeerIdInvalid
from pyrogram.errors import RPCError
from database import get_total_approvals
from pyrogram.enums import ChatAction

from database import add_user, add_group, all_users, all_groups, users, remove_user, log_approval
from database import add_admin_db, remove_admin_db, list_admins_db, is_admin
from configs import cfg
from database import datetime
from database import is_sudo
from pymongo import MongoClient

# Your MongoDB connection and database setup here...
from database import close_db_connection, reconnect_db


import random
import asyncio
import time
import sys
import os

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

from pyrogram.types import ChatJoinRequest, InlineKeyboardButton, InlineKeyboardMarkup
from pyrogram.enums import ParseMode

@bot_app.on_chat_join_request(filters.group | filters.channel)
async def approve(_, m):
    chat = m.chat
    user = m.from_user

    try:
        print(f"Approving user {user.id} in chat {chat.id}")

        add_group(chat.id)
        add_user(user.id)

        await _.approve_chat_join_request(chat.id, user.id)
        log_approval(user.id, chat.id)

        keyboard = InlineKeyboardMarkup([
            [InlineKeyboardButton("Mᴀɪɴ Cʜᴀɴɴᴇʟ", url="https://t.me/EmitingStars_Botz")],
            [
                InlineKeyboardButton("Sᴜᴘᴘᴏʀᴛ", url="https://t.me/+HZuPVe0l-F1mM2Jl"),
                InlineKeyboardButton("Cʟɪᴄᴋ ʜᴇʀᴇ", callback_data="popup_action")
            ]
        ])

        caption = (
            f"<b><blockquote>Hᴇʏ sᴡᴇᴇᴛɪᴇ</b> <a href='tg://user?id={user.id}'>{user.first_name}</a> ⭐✨</blockquote>\n\n"
            f"<blockquote>Aᴄᴄᴇss ʜᴀs ʙᴇᴇɴ <b>Gʀᴀɴᴛᴇᴅ</b> — ᴡᴇʟᴄᴏᴍᴇ ᴛᴏ "
            f"<a href='https://t.me/c/{str(chat.id)[4:]}'>{chat.title}</a> !</blockquote>\n"
            f"<i><blockquote>Pʀᴇsᴇɴᴛᴇᴅ ʙʏ <a href='https://t.me/EmitingStars_Botz'>Eᴍɪᴛɪɴɢ Sᴛᴀʀs</a></blockquote></i>"
        )

        try:
            await _.send_photo(
                user.id,
                photo="https://i.ibb.co/kVrCBtyF/photo-2025-04-28-21-31-37-7498479919144370200.jpg",
                caption=caption,
                reply_markup=keyboard,
                parse_mode=ParseMode.HTML, 
                message_effect_id=5046509860389126442
            )
            print(f"Message sent to user {user.id} in PM.")

        except Exception as e:
            print(f"Failed to send PM to user {user.id}: {e}")
            # Do NOTHING if sending PM fails
            pass

    except Exception as err:
        print(f"Error approving user {user.id}: {err}")

@bot_app.on_callback_query(filters.regex("popup_action"))
async def popup_action(_, cb: CallbackQuery):
    await cb.answer(
        "Iғ ɪ ᴄʀᴏssᴇᴅ ɢᴀʟᴀxɪᴇs ᴀɴᴅ ʙᴇɴᴛ ᴛɪᴍᴇ ᴊᴜsᴛ ᴛᴏ ғɪɴᴅ ʏᴏᴜ, ɪᴛ’ᴅ sᴛɪʟʟ ʙᴇ ᴡᴏʀᴛʜ ᴇᴠᴇʀʏ sᴜᴘᴇʀɴᴏᴠᴀ...",
        show_alert=True
    )

# ====================================================
#                      START
# ====================================================

from pyrogram.types import InputMediaPhoto

@bot_app.on_message(filters.private & filters.command("start"))
async def start_command(_, m: Message):
    welcome_text = "<i><blockquote>Wᴇʟᴄᴏᴍᴇ, ʙᴀʙʏ… ɪ’ᴠᴇ ʙᴇᴇɴ ᴄʀᴀᴠɪɴɢ ʏᴏᴜʀ ᴘʀᴇsᴇɴᴄᴇ ғᴇᴇʟs ᴘᴇʀғᴇᴄᴛ ɴᴏᴡ ᴛʜᴀᴛ ʏᴏᴜ’ʀᴇ ʜᴇʀᴇ.</blockquote></i>"

    stickers = [
        "CAACAgUAAxkBAAEOXBhoCoKZ76jevKX-Vc5v5SZhCeQAAXMAAh4KAALJrhlVZygbxFWWTLw2BA"
    ]

    start_pics = [
        "https://i.ibb.co/v6J0JM80/photo-2025-03-13-18-50-40-7481368571868610580.jpg"
    ]
    fsub_pic = start_pics[0]
    user_id = str(m.from_user.id)

    try:
        with open("users.txt", "r") as f:
            users = f.read().splitlines()
    except FileNotFoundError:
        users = []

    if user_id not in users:
        with open("users.txt", "a") as f:
            f.write(user_id + "\n")

    await bot_app.send_chat_action(m.chat.id, ChatAction.TYPING)
    msg = await m.reply_text(welcome_text)
    await asyncio.sleep(0.5)

    await msg.edit_text("<b><i><pre>Sᴛᴀʀᴛɪɴɢ...</pre></i></b>")
    await asyncio.sleep(0.5)
    await msg.delete()

    await bot_app.send_chat_action(m.chat.id, ChatAction.CHOOSE_STICKER)
    await m.reply_sticker(random.choice(stickers))

    # Force Sub Check
    not_joined = []
    for ch_id in cfg.FORCE_SUB_CHANNELS:
        try:
            member = await bot_app.get_chat_member(ch_id, m.from_user.id)
            if member.status in ["kicked", "left"]:
                not_joined.append(ch_id)
        except Exception:
            not_joined.append(ch_id)

    if not_joined:
        buttons = []
        for ch_id in not_joined:
            try:
                invite = await bot_app.create_chat_invite_link(ch_id)
                buttons.append([InlineKeyboardButton("Jᴏɪɴ ʜᴇʀᴇ", url=invite.invite_link)])
            except Exception:
                pass

        buttons.append([InlineKeyboardButton("Rᴇғʀᴇsʜ", url=f"https://t.me/{cfg.BOT_USERNAME}?start=start")])

        await bot_app.send_chat_action(m.chat.id, ChatAction.UPLOAD_PHOTO)
        return await m.reply_photo(
            photo=fsub_pic,
            caption=(
                f"<b><pre><a href='tg://user?id={m.from_user.id}'>{m.from_user.first_name}</a> Esᴛᴇᴇᴍᴇᴅ ɢᴜᴇsᴛ,</pre></b>\n"
                "<blockquote>ᴀᴄᴄᴇss ᴛᴏ ᴍʏ sᴇʀᴠɪᴄᴇs ɪs ʀᴇsᴇʀᴠᴇᴅ ғᴏʀ ᴍᴇᴍʙᴇʀs ᴏғ ᴏᴜʀ ᴜᴘᴅᴀᴛᴇ ᴄʜᴀɴɴᴇʟ.\n"
                "ᴘʟᴇᴀsᴇ ᴊᴏɪɴ ᴀɴᴅ ʀᴇᴛᴜʀɴ ᴛᴏ ᴄᴏɴᴛɪɴᴜᴇ.</blockquote>"
            ),
            reply_markup=InlineKeyboardMarkup(buttons),
            parse_mode=ParseMode.HTML
        )

    # User is all set
    await m.reply_text("<pre>Yᴏᴜ’ʀᴇ ᴀʟʟ sᴇᴛ, ʙᴀʙᴇ… ɴᴏᴡ ɢᴏ ᴏɴ ᴀɴᴅ ᴇɴᴊᴏʏ ᴛʜᴇ ʙᴏᴛ.</pre>")

    keyboard = InlineKeyboardMarkup([
        [
            InlineKeyboardButton("Mᴀɪɴ ᴄʜᴀɴɴᴇʟ", url="https://t.me/EmitingStars_Botz"),
            InlineKeyboardButton("Sᴜᴘᴘᴏʀᴛ", url="https://t.me/+HZuPVe0l-F1mM2Jl")
        ],
        [
            InlineKeyboardButton("⤬ Dᴇᴠᴇʟᴏᴘᴇʀ ⤬", url="http://t.me/RexySama")
        ],
        [
            InlineKeyboardButton("Aʙᴏᴜᴛ", callback_data="about"), 
            InlineKeyboardButton("Cʟᴏsᴇ", callback_data="close_str")
        ]
    ])

    await m.reply_photo(
        photo=random.choice(start_pics),
        caption=(
            f"<pre><b>Hᴇʏᴏ</b> <a href='tg://user?id={m.from_user.id}'>{m.from_user.first_name}</a></pre>\n"
            "<blockquote expandable><b>I'ᴍ ᴀɴ ᴀᴜᴛᴏ ᴀᴘᴘʀᴏᴠᴇ ʙᴏᴛ. ᴀᴅᴅ ᴍᴇ ᴛᴏ ʏᴏᴜʀ ɢʀᴏᴜᴘ ᴀɴᴅ ᴍᴀᴋᴇ ᴍᴇ ᴀɴ ᴀᴅᴍɪɴ ᴡɪᴛʜ ᴀᴅᴅ ᴍᴇᴍʙᴇʀs ᴘᴇʀᴍɪssɪᴏɴ ɪ'ʟʟ ʜᴀɴᴅʟᴇ ᴀᴘᴘʀᴏᴠᴀʟs ᴀᴜᴛᴏᴍᴀᴛɪᴄᴀʟʟʏ sᴏ ʏᴏᴜ ᴅᴏɴ'ᴛ ʜᴀᴠᴇ ᴛᴏ. ʟᴇᴛ ᴍᴇ ᴅᴏ ᴛʜᴇ ʙᴏʀɪɴɢ sᴛᴜғғ.</b></blockquote>\n"
            "<blockquote><a href='http://t.me/Private_Auto_Approval_Bot?startchannel=true'>➜ Aᴅᴅ ᴛᴏ ᴄʜᴀɴɴᴇʟ</a></blockquote>"
        ),
        reply_markup=keyboard,
        parse_mode=ParseMode.HTML, 
        message_effect_id=5104841245755180586
    )

@bot_app.on_callback_query(filters.regex("about"))
async def about_callback(_, cq: CallbackQuery):
    await cq.answer()
    
    about_markup = InlineKeyboardMarkup([
        [
            InlineKeyboardButton("« Bᴀᴄᴋ", callback_data="start_again"),
            InlineKeyboardButton("Cʟᴏsᴇ", callback_data="close_msg")
        ]
    ])

    about_caption = (
        f"<b><blockquote>Sᴀʏ ʏᴇs  <a href='tg://user?id={cq.from_user.id}'>{cq.from_user.first_name}</a>  ɪ’ᴍ ᴀʟʟ ʏᴏᴜʀs.</blockquote></b>\n"
        "<b><blockquote expandable>◈ Oᴡɴᴇʀ :</b> <a href='https://t.me/RexySama'>ᴄʟɪᴄᴋ ʜᴇʀᴇ</a>\n"
        "◈ <b>Dᴇᴠᴇʟᴏᴘᴇʀ :</b> <a href='https://t.me/RexySama'>ᴄʟɪᴄᴋ ʜᴇʀᴇ</a>\n"
        "◈ <b>Mᴀɪɴ Cʜᴀɴɴᴇʟ :</b> <a href='https://t.me/EmitingStars_Botz'>ᴄʟɪᴄᴋ ʜᴇʀᴇ</a>\n"
        "◈ <b>Sᴜᴘᴘᴏʀᴛ Cʜᴀɴɴᴇʟ :</b> <a href='https://t.me/+HZuPVe0l-F1mM2Jl'>ᴄʟɪᴄᴋ ʜᴇʀᴇ</a>\n"
        "◈ <b>Sᴏᴜʀᴄᴇ ᴄᴏᴅᴇ :</b> <a href='https://t.me/RexySama'>ᴄʟɪᴄᴋ ʜᴇʀᴇ</a></blockquote>"
    )
    
    await cq.message.edit_media(
        media=InputMediaPhoto(
            media="https://i.ibb.co/n8DKHRbn/photo-2025-04-28-16-38-45-7498404439389110276.jpg",  # About image link
            caption=about_caption,
            parse_mode=ParseMode.HTML
        ),
        reply_markup=about_markup
    )

@bot_app.on_callback_query(filters.regex("start_again"))
async def back_to_start(_, cq: CallbackQuery):
    await cq.answer()
    keyboard = InlineKeyboardMarkup([
        [
            InlineKeyboardButton("Mᴀɪɴ ᴄʜᴀɴɴᴇʟ", url="https://t.me/EmitingStars_Botz"),
            InlineKeyboardButton("Sᴜᴘᴘᴏʀᴛ", url="https://t.me/+HZuPVe0l-F1mM2Jl")
        ],
        [
            InlineKeyboardButton("⤬ Dᴇᴠᴇʟᴏᴘᴇʀ ⤬", url="http://t.me/RexySama")
        ],
        [
            InlineKeyboardButton("Aʙᴏᴜᴛ", callback_data="about"), 
            InlineKeyboardButton("Cʟᴏsᴇ", callback_data="close_str")
        ]
    ])
    await cq.message.edit_media(
        media=InputMediaPhoto(
            media="https://i.ibb.co/v6J0JM80/photo-2025-03-13-18-50-40-7481368571868610580.jpg",  # Your start image
            caption = (
                f"<pre><b>Hᴇʏᴏ</b> <a href='tg://user?id={cq.from_user.id}'>{cq.from_user.first_name}</a></pre>\n"
                f"<blockquote expandable><b>I'ᴍ ᴀɴ ᴀᴜᴛᴏ ᴀᴘᴘʀᴏᴠᴇ ʙᴏᴛ. ᴀᴅᴅ ᴍᴇ ᴛᴏ ʏᴏᴜʀ ɢʀᴏᴜᴘ ᴀɴᴅ ᴍᴀᴋᴇ ᴍᴇ ᴀɴ ᴀᴅᴍɪɴ ᴡɪᴛʜ ᴀᴅᴅ ᴍᴇᴍʙᴇʀs ᴘᴇʀᴍɪssɪᴏɴ ɪ'ʟʟ ʜᴀɴᴅʟᴇ ᴀᴘᴘʀᴏᴠᴀʟs ᴀᴜᴛᴏᴍᴀᴛɪᴄᴀʟʟʏ sᴏ ʏᴏᴜ ᴅᴏɴ'ᴛ ʜᴀᴠᴇ ᴛᴏ. ʟᴇᴛ ᴍᴇ ᴅᴏ ᴛʜᴇ ʙᴏʀɪɴɢ sᴛᴜғғ.</b></blockquote>\n"
                f"<blockquote><a href='http://t.me/Private_Auto_Approval_Bot?startchannel=true'>➜ Aᴅᴅ ᴛᴏ ᴄʜᴀɴɴᴇʟ</a></blockquote>"
            ), 
            parse_mode=ParseMode.HTML
        ),
        reply_markup=keyboard
    )


@bot_app.on_callback_query(filters.regex("close_msg"))
async def close_message(_, cq: CallbackQuery):
    await cq.answer()
    await cq.message.delete()

@bot_app.on_callback_query(filters.regex("close_str"))
async def close_message(_, cq: CallbackQuery):
    await cq.answer()
    await cq.message.delete()


# ====================================================
#                   CALLBACK CHECK
# ====================================================

@bot_app.on_callback_query(filters.regex("chk"))
async def chk_callback(_, cb: CallbackQuery):
    not_joined = []

    # Check user membership in all required channels
    for ch_id in cfg.FORCE_SUB_CHANNELS:
        try:
            member = await bot_app.get_chat_member(ch_id, cb.from_user.id)
            if member.status not in ["member", "administrator", "creator"]:
                not_joined.append(ch_id)
        except Exception:
            not_joined.append(ch_id)

    # If user hasn't joined all required channels
    if not_joined:
        buttons = []
        for ch_id in not_joined:
            try:
                invite = await bot_app.create_chat_invite_link(ch_id)
                buttons.append([InlineKeyboardButton("Jᴏɪɴ ʜᴇʀᴇ", url=invite.invite_link)])
            except Exception:
                continue

        buttons.append([
            InlineKeyboardButton("🔁 Rᴇᴄʜᴇᴄᴋ", callback_data="chk")
        ])

        try:
            await cb.message.edit_caption(
                caption="**<i>ᴘʟᴇᴀsᴇ ᴊᴏɪɴ ᴀʟʟ ᴛʜᴇ ʀᴇQᴜɪʀᴇᴅ ᴄʜᴀɴɴᴇʟs ᴛᴏ ᴄᴏɴᴛɪɴᴜᴇ.</i>**",
                reply_markup=InlineKeyboardMarkup(buttons),
                parse_mode=ParseMode.HTML
            )
        except Exception:
            await cb.message.edit_text(
                "**<i>ᴘʟᴇᴀsᴇ ᴊᴏɪɴ ᴀʟʟ ᴛʜᴇ ʀᴇQᴜɪʀᴇᴅ ᴄʜᴀɴɴᴇʟs ᴛᴏ ᴄᴏɴᴛɪɴᴜᴇ.</i>**",
                reply_markup=InlineKeyboardMarkup(buttons),
                parse_mode=ParseMode.HTML
            )
        return

    # Passed check: add user and send welcome
    add_user(cb.from_user.id)

    keyboard = InlineKeyboardMarkup([
        [
            InlineKeyboardButton("Mᴀɪɴ ᴄʜᴀɴɴᴇʟ", url="https://t.me/EmitingStars_Botz"),
            InlineKeyboardButton("Sᴜᴘᴘᴏʀᴛ", url="https://t.me/+HZuPVe0l-F1mM2Jl")
        ],
        [
            InlineKeyboardButton("⤬ Dᴇᴠᴇʟᴏᴘᴇʀ ⤬", url="http://t.me/RexySama")
        ],
        [
            InlineKeyboardButton("Aʙᴏᴜᴛ", callback_data="about"), 
            InlineKeyboardButton("Cʟᴏsᴇ", callback_data="close_str")
        ]
    ])

    text = (
        f"<pre><b>Hᴇʏᴏ</b> <a href='tg://user?id={cb.from_user.id}'>{cb.from_user.first_name}</a></pre>\n"
        f"<blockquote expandable><b>I'ᴍ ᴀɴ ᴀᴜᴛᴏ ᴀᴘᴘʀᴏᴠᴇ ʙᴏᴛ. "
        f"Aᴅᴅ ᴍᴇ ᴛᴏ ʏᴏᴜʀ ɢʀᴏᴜᴘ ᴀɴᴅ ᴍᴀᴋᴇ ᴍᴇ ᴀɴ ᴀᴅᴍɪɴ "
        f"ᴡɪᴛʜ ᴀᴅᴅ ᴍᴇᴍʙᴇʀs ᴘᴇʀᴍɪssɪᴏɴ. "
        f"I'ʟʟ ʜᴀɴᴅʟᴇ ᴀᴘᴘʀᴏᴠᴀʟs ᴀᴜᴛᴏᴍᴀᴛɪᴄᴀʟʟʏ.</b></blockquote>\n"
        f"<blockquote><a href='http://t.me/Private_Auto_Approval_Bot?startchannel=true'>➜ Aᴅᴅ ᴛᴏ ᴄʜᴀɴɴᴇʟ</a></blockquote>"
    )

    try:
        await cb.message.edit_text(
            text=text,
            reply_markup=keyboard,
            parse_mode=ParseMode.HTML
        )
    except Exception:
        await cb.message.reply(
            text=text,
            reply_markup=keyboard,
            parse_mode=ParseMode.HTML
        )

# ====================================================
#                      INFO CMD
# ====================================================

@bot_app.on_message(filters.command("status") & is_sudo())
async def dbtool(_, m: Message):

    # Typing action
    await bot_app.send_chat_action(m.chat.id, ChatAction.TYPING)
    # Animation sequence
    welcome_text = "<pre>Pʀᴇᴘᴀʀɪɴɢ sᴛᴀᴛᴜs ʀᴇᴘᴏʀᴛ...</pre>"
    msg = await m.reply_text(welcome_text)
    await asyncio.sleep(0.2)
    await msg.edit_text("<b><i><pre>Dᴏɴᴇ sᴇɴᴅɪɴɢ...</pre></i></b>")
    await asyncio.sleep(0.1)
    await msg.delete()

    await bot_app.send_chat_action(m.chat.id, ChatAction.CHOOSE_STICKER)
    await m.reply_sticker(random.choice(stickers))


    # Collect chat statistics
    total_users = all_users()
    total_groups = all_groups()
    total = total_users + total_groups

    user_percent = (total_users / total) * 100 if total else 0
    group_percent = (total_groups / total) * 100 if total else 0

    # Inline buttons
    keyboard = InlineKeyboardMarkup([
        [InlineKeyboardButton("Dᴇᴠᴇʟᴏᴘᴇʀ", url="https://t.me/RexySama")],
        [InlineKeyboardButton("Sᴜᴘᴘᴏʀᴛ", url="https://t.me/+HZuPVe0l-F1mM2Jl"), InlineKeyboardButton("Cʟᴏsᴇ ✖", callback_data="close_stats")]
    ])

    timestamp = datetime.now().strftime("%d %b %Y • %I:%M %p")

    caption = (
        f"<blockquote><b>➥ 𝗖𝗛𝗔𝗧 𝗦𝗧𝗔𝗧𝗜𝗦𝗧𝗜𝗖𝗦</b></blockquote>\n\n"
        f"<blockquote><b>❏ ᴜsᴇʀs : {total_users} ({user_percent:.1f}%)</b></blockquote>\n"
        f"<blockquote><b>❏ ɢʀᴏᴜᴘs : {total_groups} ({group_percent:.1f}%)</b></blockquote>\n"
        f"<blockquote><b>❏ ᴛᴏᴛᴀʟ ᴄʜᴀᴛs : {total}</blockquote></b>\n"
        f"<blockquote><b>❏ ʟᴀsᴛ ᴜᴘᴅᴀᴛᴇᴅ : {timestamp}</blockquote></b>"
    )

    await m.reply_photo(
        photo="https://i.ibb.co/8LGYrGzn/photo-2025-04-28-21-31-38-7498479936324239364.jpg",
        caption=caption,
        reply_markup=keyboard,
        parse_mode=ParseMode.HTML,
        message_effect_id=5046509860389126442
    )

@bot_app.on_callback_query(filters.regex("close_stats"))
async def close_stats(_, cb: CallbackQuery):
    await cb.message.delete()
    await cb.answer("Closed!", show_alert=True)

stickers = [
        "CAACAgUAAxkBAAEOXBhoCoKZ76jevKX-Vc5v5SZhCeQAAXMAAh4KAALJrhlVZygbxFWWTLw2BA",
    ]
    
# ====================================================
#                 BROADCAST (COPY)
# ====================================================

broadcast_states = {}

UPDATE_DELAY = 5  # seconds between UI updates

# Broadcast function to start the process
@bot_app.on_message(filters.command("broadcast") & is_sudo())
async def bcast(_, m: Message):
    if not m.reply_to_message:
        return await m.reply("Please reply to a message to broadcast.")

    broadcast_id = m.id
    broadcast_states[broadcast_id] = False

    lel = await m.reply_photo(
        "https://i.ibb.co/9m1Rqmv8/photo-2025-04-28-17-06-26-7498411556149919760.jpg",
        caption="<pre>Pʀᴇᴘᴀʀɪɴɢ ʙʀᴏᴀᴅᴄᴀsᴛ...</pre>",
        reply_markup=InlineKeyboardMarkup([
            [InlineKeyboardButton("Cᴀɴᴄᴇʟ", callback_data=f"cancel_bcast:{broadcast_id}"),
             InlineKeyboardButton("Cʟᴏsᴇ", callback_data="close_bcast")]
        ])
    )

    total_users = users.count_documents({})
    if total_users == 0:
        return await lel.edit("No users found in the database.")

    stats = {"success": 0, "failed": 0, "deactivated": 0, "blocked": 0}
    bar_length = 20
    start_time = time.perf_counter()
    last_ui_update = time.perf_counter()

    for idx, u in enumerate(users.find(), 1):
        if broadcast_states.get(broadcast_id):
            break

        try:
            await _.copy_message(chat_id=int(u["user_id"]), from_chat_id=m.chat.id, message_id=m.reply_to_message.id)
            stats["success"] += 1
        except UserDeactivated:
            stats["deactivated"] += 1
            users.delete_one({"user_id": u["user_id"]})
        except UserBlocked:
            stats["blocked"] += 1
        except Exception as e:
            stats["failed"] += 1
            print(f"Error with user {u['user_id']}: {e}")

        now = time.perf_counter()
        percent = idx / total_users
        eta_seconds = ((now - start_time) / percent) - (now - start_time)

        if now - last_ui_update >= UPDATE_DELAY or idx == total_users:
            bar = "●" * int(percent * bar_length) + "○" * (bar_length - int(percent * bar_length))
            eta = f"{int(eta_seconds)//60:02}:{int(eta_seconds)%60:02}"
            await lel.edit(
                f"<blockquote>➥ {'Bʀᴏᴀᴅᴄᴀsᴛɪɴɢ' if not broadcast_states[broadcast_id] else 'Cᴀɴᴄᴇʟᴇᴅ!'}</blockquote>\n\n"
                f"<pre><code>[{bar}] {int(percent * 100)}%</code>\n"
                f"❏ Eᴛᴀ : `{eta}`</pre>\n\n"
                f"<blockquote>❏ Sᴜᴄᴄᴇssғᴜʟ : `{stats['success']}` | ❏ Fᴀɪʟᴇᴅ : `{stats['failed']}`\n"
                f"❏ Dᴇᴀᴄᴛɪᴠᴀᴛᴇᴅ: `{stats['deactivated']}` | ❏ Bʟᴏᴄᴋᴇᴅ : `{stats['blocked']}`</blockquote>",
                reply_markup=InlineKeyboardMarkup([
                    [InlineKeyboardButton("Cᴀɴᴄᴇʟ", callback_data=f"cancel_bcast:{broadcast_id}"),
                     InlineKeyboardButton("Cʟᴏsᴇ", callback_data="close_bcast")]
                ])
            )
            last_ui_update = now

        await asyncio.sleep(0.05)

    # Final Message
    final_bar = "●" * bar_length
    await lel.edit(
        f"<blockquote>➥ {'Bʀᴏᴀᴅᴄᴀsᴛ ᴄᴏᴍᴘʟᴇᴛᴇᴅ' if not broadcast_states[broadcast_id] else 'Bʀᴏᴀᴅᴄᴀsᴛ ᴄᴀɴᴄᴇʟᴇᴅ!'}</blockquote>\n\n"
        f"<pre><code>[{final_bar}] 100%</code></pre>\n\n"
        f"<blockquote>❏ Sᴜᴄᴄᴇssғᴜʟ : `{stats['success']}`\n"
        f"❏ Fᴀɪʟᴇᴅ : `{stats['failed']}`\n"
        f"❏ Bʟᴏᴄᴋᴇᴅ : `{stats['blocked']}`\n"
        f"❏ Dᴇᴀᴄᴛɪᴠᴀᴛᴇᴅ : `{stats['deactivated']}`</blockquote>",
        reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("Cʟᴏsᴇ", callback_data="close_bcast")]])
    )
    broadcast_states.pop(broadcast_id, None)

# Callback handler for canceling the broadcast
@bot_app.on_callback_query(filters.regex(r"cancel_bcast:(\d+)"))
async def cancel_bcast(_, cb):
    broadcast_id = int(cb.matches[0].group(1))
    broadcast_states[broadcast_id] = True
    await cb.answer("Bʀᴏᴀᴅᴄᴀsᴛ ʜᴀs ʙᴇᴇɴ ᴄᴀɴᴄᴇʟᴇᴅ.", show_alert=True)

# Callback handler for closing the broadcast message
@bot_app.on_callback_query(filters.regex("close_bcast"))
async def close_bcast(_, cb):
    await cb.message.delete()
    await cb.answer()

# ====================================================
#                    HELP CENTER
# ====================================================

@bot_app.on_message(filters.private & filters.command("help"))
async def help_command(_, m: Message):

    # Typing action
    await bot_app.send_chat_action(m.chat.id, ChatAction.TYPING)
    
    welcome_text = "<pre>Cʀᴇᴀᴛɪɴɢ ᴍᴇssᴀɢᴇ... </pre>"
    msg = await m.reply_text(welcome_text)
    await asyncio.sleep(0.2)
    await msg.edit_text("<b><i><pre>Dᴏɴᴇ sᴇɴᴅɪɴɢ...</pre></i></b>")
    await asyncio.sleep(0.1)
    await msg.delete()

    await bot_app.send_chat_action(m.chat.id, ChatAction.CHOOSE_STICKER)

    # Random sticker from a predefined list
    stickers = [
        "CAACAgUAAxkBAAEOXBhoCoKZ76jevKX-Vc5v5SZhCeQAAXMAAh4KAALJrhlVZygbxFWWTLw2BA",
        # Add more sticker file_ids as needed
    ]
    await m.reply_sticker(random.choice(stickers))

    keyboard = InlineKeyboardMarkup([
        [InlineKeyboardButton("Dᴇᴠᴇʟᴏᴘᴇʀ", url="https://t.me/RexySama")],
        [
            InlineKeyboardButton("Mᴀɪɴ ᴄʜᴀɴɴᴇʟ", url="https://t.me/EmitingStars_Botz"),
            InlineKeyboardButton("Sᴜᴘᴘᴏʀᴛ", url="https://t.me/+HZuPVe0l-F1mM2Jl")
        ],
        [InlineKeyboardButton("Cʟᴏsᴇ ✖", callback_data="close_help")]
    ])

    await m.reply_photo(
        "https://i.ibb.co/GQhtSDGH/photo-2025-04-28-21-39-52-7498482058038083600.jpg",
        caption=(
            "<blockquote>𝗨𝗦𝗘𝗥 𝗚𝗨𝗜𝗗𝗘</blockquote>\n"
            "<blockquote expandable>➥ Kɪɴᴅʟʏ ᴀᴅᴅ ᴛʜɪs ʙᴏᴛ ᴛᴏ ʏᴏᴜʀ ᴇsᴛᴇᴇᴍᴇᴅ ᴄʜᴀɴɴᴇʟ, ᴀɴᴅ ɪᴛ ᴡɪʟʟ ɢʀᴀᴄᴇғᴜʟʟʏ ʙᴇɢɪɴ ᴀᴘᴘʀᴏᴠɪɴɢ ᴀʟʟ ɴᴇᴡ ᴍᴇᴍʙᴇʀs ᴡɪᴛʜ ᴇғғɪᴄɪᴇɴᴄʏ ᴀɴᴅ ᴄᴀʀᴇ.</blockquote>\n"
        ),
        reply_markup=keyboard,
        parse_mode=ParseMode.HTML,
        message_effect_id=5046509860389126442 #
    )

@bot_app.on_callback_query(filters.regex("close_help"))
async def close_help(_, cb: CallbackQuery):
    await cb.message.delete()

# ====================================================
#                    ADMIMS
# ====================================================

@bot_app.on_message(filters.command("add_admin") & filters.user(cfg.SUDO))
async def addadmin(_, m: Message):
    if len(m.command) < 2 or not all(x.isdigit() for x in m.command[1:]):
        return await m.reply(
            "<pre>⁉️ Yᴏᴜ ɴᴇᴇᴅ ᴛᴏ ᴀᴅᴅ Aᴅᴍɪɴ ɪᴅs</pre>\n"
            "<b><blockquote>EXAMPLE:</b>\n"
            "/addadmin 123456789 — ᴀᴅᴅ ᴏɴᴇ ᴜsᴇʀ\n"
            "/addadmin 123456789 987654321 — ᴀᴅᴅ ᴍᴜʟᴛɪᴘʟᴇ ᴜsᴇʀs</blockquote>",
            parse_mode=ParseMode.HTML,
            reply_markup=InlineKeyboardMarkup(
                [[InlineKeyboardButton("Cʟᴏsᴇ ✖", callback_data="close_msg")]]
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
            "<pre>Aʟʟ ᴘʀᴏᴠɪᴅᴇᴅ ᴜsᴇʀs ᴀʀᴇ ᴀʟʀᴇᴀᴅʏ ᴀᴅᴍɪɴs.</pre>",
            parse_mode=ParseMode.HTML,
            reply_markup=InlineKeyboardMarkup(
                [[InlineKeyboardButton("Cʟᴏsᴇ ✖", callback_data="close_msg")]]
            )
        )

    added_text = "\n".join([f"• <a href='tg://user?id={uid}'>{uid}</a>" for uid in added])
    await m.reply(
        f"<blockquote>Tʜᴇ ғᴏʟʟᴏᴡɪɴɢ ᴜsᴇʀ(s) ᴡᴇʀᴇ ᴀᴅᴅᴇᴅ ᴀs ᴀᴅᴍɪɴs :\n{added_text}</blockquote>",
        message_effect_id=5046509860389126442, 
        parse_mode=ParseMode.HTML,
        reply_markup=InlineKeyboardMarkup(
            [[InlineKeyboardButton("Cʟᴏsᴇ ✖", callback_data="close_msg")]]
        )
    )


@bot_app.on_message(filters.command("remove_admin") & filters.user(cfg.SUDO))
async def removeadmin(_, m: Message):
    args = m.command[1:]

    if not args:
        return await m.reply(
            "<pre>⁉️ Pʟᴇᴀsᴇ, Pʀᴏᴠɪᴅᴇ ᴠᴀʟɪᴅ ɪᴅs ᴏʀ ᴀʀɢᴜᴍᴇɴᴛs</pre>\n"
            "<b><blockquote>EXAMPLES:</b>\n"
            "/removeadmin 123456789 — ᴛᴏ ᴅᴇʟᴇᴛᴇ ᴏɴᴇ sᴘᴇᴄɪғɪᴇᴅ ɪᴅ\n"
            "/removeadmin 123456789 987654321 — ᴛᴏ ᴅᴇʟᴇᴛᴇ ᴍᴜʟᴛɪᴘʟᴇ sᴘᴇᴄɪғɪᴇᴅ ɪᴅs\n"
            "/removeadmin all — ᴛᴏ ᴅᴇʟᴇᴛᴇ ᴀʟʟ ᴀᴅᴍɪɴs</blockquote>",
            parse_mode=ParseMode.HTML,
            reply_markup=InlineKeyboardMarkup(
                [[InlineKeyboardButton("Cʟᴏsᴇ ✖", callback_data="close_msg")]]
            )
        )

    if args[0].lower() == "all":
        all_admins = list_admins_db()
        if not all_admins:
            return await m.reply("<pre>Nᴏ ᴀᴅᴍɪɴs ғᴏᴜɴᴅ ᴛᴏ ʀᴇᴍᴏᴠᴇ.</pre>")
        for admin in all_admins:
            remove_admin_db(admin)
        return await m.reply(
            "<pre>Aʟʟ ᴀᴅᴍɪɴs ʜᴀᴠᴇ ʙᴇᴇɴ ʀᴇᴍᴏᴠᴇᴅ.</pre>",
            parse_mode=ParseMode.HTML,
            reply_markup=InlineKeyboardMarkup(
                [[InlineKeyboardButton("Cʟᴏsᴇ ✖", callback_data="close_msg")]]
            )
        )

    if not all(x.isdigit() for x in args):
        return await m.reply("<pre>Pʟᴇᴀsᴇ ᴇɴᴛᴇʀ ᴠᴀʟɪᴅ ɴᴜᴍᴇʀɪᴄ ᴜsᴇʀ ɪᴅs.</pre>")

    removed = []
    for user_id in args:
        uid = int(user_id)
        if is_admin(uid):
            remove_admin_db(uid)
            removed.append(uid)

    if not removed:
        return await m.reply(
            "<pre>Nᴏ ᴀᴅᴍɪɴ ғᴏᴜɴᴅ ᴡɪᴛʜ ᴛʜᴇ ᴘʀᴏᴠɪᴅᴇᴅ ɪᴅs.</pre>",
            parse_mode=ParseMode.HTML,
            reply_markup=InlineKeyboardMarkup(
                [[InlineKeyboardButton("Cʟᴏsᴇ ✖", callback_data="close_msg")]]
            )
        )

    removed_text = "\n".join([f"• <a href='tg://user?id={uid}'>{uid}</a>" for uid in removed])
    await m.reply(
        f"<blockquote>Tʜᴇ ғᴏʟʟᴏᴡɪɴɢ ᴀᴅᴍɪɴ(s) ᴡᴇʀᴇ ʀᴇᴍᴏᴠᴇᴅ :\n{removed_text}</blockquote>",
        message_effect_id=5046509860389126442, 
        parse_mode=ParseMode.HTML,
        reply_markup=InlineKeyboardMarkup(
            [[InlineKeyboardButton("Cʟᴏsᴇ ✖", callback_data="close_msg")]]
        )
    )

@bot_app.on_message(filters.command("admins_list") & is_sudo())
async def listadmin(_, m: Message):
    # Animated status text
    welcome_text = "<pre>Pʀᴇᴘᴀʀɪɴɢ sᴛᴀᴛᴜs ʀᴇᴘᴏʀᴛ...</pre>"
    msg = await m.reply_text(welcome_text)
    await asyncio.sleep(0.2)
    await msg.edit_text("<b><i><pre>Dᴏɴᴇ sᴇɴᴅɪɴɢ...</pre></i></b>")
    await asyncio.sleep(0.1)
    await msg.delete()

    # Random sticker from list
    stickers = [
        "CAACAgUAAxkBAAEOXBhoCoKZ76jevKX-Vc5v5SZhCeQAAXMAAh4KAALJrhlVZygbxFWWTLw2BA", 
        # Add more if you want variety
    ]
    await m.reply_sticker(random.choice(stickers))

    # Get list of admins from the database
    admin_ids = list_admins_db()
    if not admin_ids:
        return await m.reply(
            "<pre>Nᴏ ᴀᴅᴍɪɴs ғᴏᴜɴᴅ.</pre>",
            parse_mode=ParseMode.HTML,
            message_effect_id=5046509860389126442, 
            reply_markup=InlineKeyboardMarkup(
                [[InlineKeyboardButton("Cʟᴏsᴇ ✖", callback_data="close_msg")]]
            )
        )

    admin_list = ""
    for id in admin_ids:
        await m.reply_chat_action(ChatAction.TYPING)
        try:
            user = await _.get_users(id)
            user_link = f"tg://openmessage?user_id={id}"
            first_name = user.first_name if user.first_name else "No first name!"
            
            admin_list += f"<b><blockquote>NAME: <a href='{user_link}'>{first_name}</a>\n(ID: <code>{id}</code>)</blockquote></b>\n\n"
                
        except Exception as e:
            admin_list += f"<b><blockquote>ɪᴅ: <code>{id}</code>\n<i>ᴜɴᴀʙʟᴇ ᴛᴏ ʟᴏᴀᴅ ᴏᴛʜᴇʀ ᴅᴇᴛᴀɪʟs..</i></blockquote></b>\n\n"

    await m.reply_photo(
        photo="https://i.ibb.co/SDVMgVRk/photo-2025-04-28-21-39-52-7498482040858214428.jpg",
        caption=f"<b>🤖 𝗕𝗢𝗧 𝗔𝗗𝗠𝗜𝗡𝗦 𝗟𝗜𝗦𝗧 :</b>\n\n{admin_list}",
        parse_mode=ParseMode.HTML,
        message_effect_id=5046509860389126442, 
        reply_markup=InlineKeyboardMarkup(
            [[InlineKeyboardButton("Cʟᴏsᴇ ✖", callback_data="close_msg")]]
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
        chat_id = m.chat.id
        requests = [req async for req in user_app.get_chat_join_requests(chat_id)]

        approved = 0
        skipped = 0
        total = len(requests)

        # Send initial progress message
        progress_message = await m.reply(
            f"<pre>➥ Sᴛᴀʀᴛɪɴɢ ᴛᴏ ᴀᴘᴘʀᴏᴠᴇ...</pre>\n<blockquote>❏ Aᴘᴘʀᴏᴠᴇᴅ : {approved}\n❏ Sᴋɪᴘᴘᴇᴅ : {skipped}\n❏ Tᴏᴛᴀʟ : {total}</blockquote>",
            parse_mode=ParseMode.HTML
        )

        async def approve_user(req):
            nonlocal approved, skipped
            try:
                await user_app.approve_chat_join_request(chat_id, req.user.id)
                approved += 1
            except RPCError as e:
                if "USER_CHANNELS_TOO_MUCH" in str(e):
                    skipped += 1
                else:
                    skipped += 1

        batch_size = 20  # approve 20 users at once
        delay_between_batches = 5  # seconds delay after each batch

        for i in range(0, len(requests), batch_size):
            batch = requests[i:i + batch_size]
            await asyncio.gather(*(approve_user(req) for req in batch))
            await asyncio.sleep(delay_between_batches)  # wait after each batch

            # Update progress
            await progress_message.edit_text(
                f"<pre>➥ Aᴘᴘʀᴏᴠɪɴɢ...</pre>\n<blockquote>❏ Aᴘᴘʀᴏᴠᴇᴅ : {approved}\n❏ Sᴋɪᴘᴘᴇᴅ : {skipped}\n❏ Tᴏᴛᴀʟ : {total}</blockquote>",
                parse_mode=ParseMode.HTML
            )

        # Final update
        await progress_message.edit_text(
            f"<b><pre>➥ ᴀʟʟ ᴅᴏɴᴇ !</pre></b>\n<blockquote><b>❏ Aᴘᴘʀᴏᴠᴇᴅ :</b> {approved}\n<b>❏ Sᴋɪᴘᴘᴇᴅ :</b> {skipped}\n<b>❏ Tᴏᴛᴀʟ :</b> {total}</blockquote>",
            parse_mode=ParseMode.HTML,
            reply_markup=InlineKeyboardMarkup(
                [[InlineKeyboardButton("Cʟᴏsᴇ ✖", callback_data="close_msg")]]
            )
        )

    except PeerIdInvalid:
        await m.reply("<blockquote>❌ <b>Iɴᴠᴀʟɪᴅ ɢʀᴏᴜᴘ / ᴄʜᴀɴɴᴇʟ ɪᴅ.</b></blockquote>", parse_mode=ParseMode.HTML)
    except RPCError as err:
        await m.reply(f"<blockquote>⚠️ <b>Tᴇʟᴇɢʀᴀᴍ ᴇʀʀᴏʀ :</b> <code>{err}</code></blockquote>", parse_mode=ParseMode.HTML)
    except Exception as err:
        await m.reply(f"<blockquote>⚠️ <b>Uɴᴇxᴘᴇᴄᴛᴇᴅ ᴇʀʀᴏʀ :</b> <code>{err}</code></blockquote>", parse_mode=ParseMode.HTML)

# ====================================================
#                   USER ID
# ====================================================

@bot_app.on_message(filters.private & filters.command("approveall"))
async def help_command(_, m: Message):

    # Typing action
    await bot_app.send_chat_action(m.chat.id, ChatAction.TYPING)
    # Welcome animation
    welcome_text = "<pre>Hᴏʟᴅ ᴜᴘ, ᴄᴜᴛɪᴇ… ɴᴏᴛ sᴏ ғᴀsᴛ</pre>"
    msg = await m.reply_text(welcome_text)
    await asyncio.sleep(0.2)
    await msg.edit_text("<b><i><pre>Dᴏɴᴇ sᴇɴᴅɪɴɢ...</pre></i></b>")
    await asyncio.sleep(0.1)
    await msg.delete()

    await bot_app.send_chat_action(m.chat.id, ChatAction.CHOOSE_STICKER)

    # Random sticker from a list
    stickers = [
        "CAACAgUAAxkBAAEOXBhoCoKZ76jevKX-Vc5v5SZhCeQAAXMAAh4KAALJrhlVZygbxFWWTLw2BA",
        # Add more sticker file_ids here
    ]
    await m.reply_sticker(random.choice(stickers))

    help_text = (
        "<blockquote>𝗙𝗢𝗟𝗟𝗢𝗪 𝗧𝗛𝗘𝗦𝗘 𝗦𝗧𝗘𝗣𝗦</blockquote>\n"
        "<b><blockquote>➥ Sᴛᴇᴘ 1 :</b> Aᴅᴅ ᴛʜɪs @kaoru_Tono ᴛᴇʟᴇɢʀᴀᴍ ɪᴅ ᴛᴏ ʏᴏᴜʀ ᴄʜᴀɴɴᴇʟ.</blockquote>\n"
        "<b><blockquote>➥ Sᴛᴇᴘ 2 :</b> Mᴀᴋᴇ ᴛʜɪs ɪᴅ ᴀs ᴀᴅᴍɪɴ</blockquote>\n"
        "<b><blockquote>➥ Sᴛᴇᴘ 3 :</b> Sᴇɴᴅ ᴛʜᴇ /acceptall ᴄᴏᴍᴍᴀɴᴅ ɪɴ ʏᴏᴜʀ ᴄʜᴀɴɴᴇʟ ᴛᴏ ᴀᴘᴘʀᴏᴠᴇ ᴀʟʟ ᴘᴇɴᴅɪɴɢ ʀᴇǫᴜᴇsᴛs. ᴏɴᴄᴇ ᴅᴏɴᴇ, ʀᴇᴍᴏᴠᴇ ᴛʜɪs ɪᴅ ғʀᴏᴍ ʏᴏᴜʀ ᴄʜᴀɴɴᴇʟ.</blockquote>"
    )

    image_url = "https://i.ibb.co/sv5mMnvt/photo-2025-04-28-21-39-52-7498482075217952784.jpg"

    buttons = InlineKeyboardMarkup([
        [InlineKeyboardButton("Sᴜᴘᴘᴏʀᴛ", url="https://t.me/+HZuPVe0l-F1mM2Jl")],
        [
            InlineKeyboardButton("Dᴇᴠᴇʟᴏᴘᴇʀ", url="https://t.me/RexySama"),
            InlineKeyboardButton("Cʟᴏsᴇ ✖", callback_data="close_msg")
        ]
    ])

    await m.reply_photo(
        photo=image_url,
        caption=help_text,
        reply_markup=buttons,
        parse_mode=ParseMode.HTML,
        message_effect_id=5046509860389126442
    )

# Optional handlers for the help buttons for future 🔮 use
@bot_app.on_callback_query(filters.regex("first_help"))
async def help_first(_, cq: CallbackQuery):
    await cq.answer("This is the first help button.")

@bot_app.on_callback_query(filters.regex("second_help"))
async def help_second(_, cq: CallbackQuery):
    await cq.answer("This is the second help button.")

@bot_app.on_callback_query(filters.regex("close_msg"))
async def help_close(_, cq: CallbackQuery):
    await cq.answer()
    await cq.message.delete()

# ====================================================
#                   USER ID
# ====================================================

@bot_app.on_message(filters.command("myid") & filters.private)
async def showid(client, message):
    # Animated status text
    welcome_text = "<pre>Fᴇᴛᴄʜɪɴɢ ʏᴏᴜʀ ɪɴғᴏʀᴍᴀᴛɪᴏɴ... </pre>"
    msg = await message.reply_text(welcome_text)
    await asyncio.sleep(0.2)
    await msg.edit_text("<b><i><pre>Dᴏɴᴇ sᴇɴᴅɪɴɢ...</pre></i></b>")
    await asyncio.sleep(0.1)
    await msg.delete()

    # Random sticker from list
    stickers = [
        "CAACAgUAAxkBAAEOXBhoCoKZ76jevKX-Vc5v5SZhCeQAAXMAAh4KAALJrhlVZygbxFWWTLw2BA",
        # Add more stickers if you want variety
    ]
    await message.reply_sticker(random.choice(stickers))

    # User ID display
    user_id = message.chat.id
    photo_url = "https://i.ibb.co/Kj5gSwWG/photo-2025-04-28-21-39-52-7498482032268279812.jpg"

    buttons = InlineKeyboardMarkup([
        [
            InlineKeyboardButton("Dᴇᴠᴇʟᴏᴘᴇʀ", url="https://t.me/RexySama"),
            InlineKeyboardButton("Cʟᴏsᴇ ✖", callback_data="close")
        ]
    ])

    await message.reply_photo(
        photo=photo_url,
        caption=f"<b><blockquote>Yᴏᴜʀ ᴜsᴇʀ ɪᴅ ɪs... <code>{user_id}</code> ʙᴜᴛ ᴏʀ ᴍᴀʏʙᴇ ɪᴛ'ꜱ ᴛɪᴍᴇ ɪ ɢᴇᴛ ᴛᴏ ᴋɴᴏᴡ ʏᴏᴜ ʙᴇᴛᴛᴇʀ , ᴄᴏᴍᴘʟᴇᴛᴇʟʏ</b></blockquote>",
        reply_markup=buttons,
        quote=True,
        parse_mode=ParseMode.HTML, 
        message_effect_id=5046509860389126442
    )

@bot_app.on_callback_query(filters.regex("close"))
async def close_callback(client, callback_query):
    await callback_query.message.delete()
    await callback_query.answer()

# ====================================================
#                   TOTAL APPROVED
# ====================================================

@bot_app.on_message(filters.command("total_approved") & is_sudo())
async def total_approved(client: Client, message: Message):
    try:
        await client.send_chat_action(message.chat.id, ChatAction.TYPING)

        # Step 1: Initial message
        msg = await message.reply_text(
            "<pre>Fᴇᴛᴄʜɪɴɢ ʏᴏᴜʀ ɪɴғᴏʀᴍᴀᴛɪᴏɴ...</pre>",
            parse_mode=ParseMode.HTML
        )

        await asyncio.sleep(0.2)

        # Step 2: Editing message
        await msg.edit_text(
            "<b><i><pre>Dᴏɴᴇ sᴇɴᴅɪɴɢ...</pre></i></b>",
            parse_mode=ParseMode.HTML
        )

        await asyncio.sleep(0.1)

        # Step 3: Delete message
        await msg.delete()

        await client.send_chat_action(message.chat.id, ChatAction.CHOOSE_STICKER)

        # Step 4: Send random sticker
        stickers = [
            "CAACAgUAAxkBAAEOXBhoCoKZ76jevKX-Vc5v5SZhCeQAAXMAAh4KAALJrhlVZygbxFWWTLw2BA",
        ]
        await message.reply_sticker(random.choice(stickers))

        # Step 5: Fetch total approved users
        total = get_total_approvals()  # Should return an integer

        # Step 6: Build buttons
        buttons = InlineKeyboardMarkup([
            [InlineKeyboardButton("Dᴇᴠᴇʟᴏᴘᴇʀ", url="https://t.me/RexySama")],
            [InlineKeyboardButton("Cʟᴏsᴇ ✖", callback_data="close_msg")]
        ])

        # Step 7: Send photo with total
        await message.reply_photo(
            photo="https://i.ibb.co/CK3nKw6r/photo-2025-04-28-21-31-37-7498479901964501008.jpg",
            caption=f"<pre>➥ <b>Tᴏᴛᴀʟ ᴜsᴇʀs ᴀᴘᴘʀᴏᴠᴇᴅ ʙʏ ᴛʜᴇ ʙᴏᴛ :</b> <code>{total}</code></pre>",
            parse_mode=ParseMode.HTML,
            message_effect_id=5046509860389126442,
            reply_markup=buttons
        )

    except Exception as e:
        await message.reply(
            f"⚠️ <b>Error:</b> <code>{str(e)}</code>",
            parse_mode=ParseMode.HTML
        )

# ====================================================
#                   RESTART 
# ====================================================

@bot_app.on_message(filters.command('restart') & is_sudo())
async def restart_bot(client: Client, message: Message):
    print("Restarting bot...")
    
    # Send a message indicating bot restart
    msg = await message.reply(
        text=f"<b><i><blockquote>⚠️ {client.name} ɢᴏɪɴɢ ᴛᴏ Rᴇsᴛᴀʀᴛ...</blockquote></i></b>"
    )
    
    try:
        # Close the database connection before restarting
        close_db_connection()

        # Wait for 6 seconds before restarting
        await asyncio.sleep(6)
        await msg.delete()

        # Restart the bot by executing the same script
        args = [sys.executable, sys.argv[0]]
        os.execl(sys.executable, *args)
        
    except Exception as e:
        print(f"Error occurred while restarting the bot: {e}")
        await msg.edit_text(
            f"<b><i>! Eʀʀᴏʀ, Cᴏɴᴛᴀᴄᴛ ᴅᴇᴠᴇʟᴏᴘᴇʀ ᴛᴏ sᴏʟᴠᴇ ᴛʜᴇ ɪssᴜᴇs @JeffySama</i></b>\n"
            f"<blockquote expandable><b>Rᴇᴀsᴏɴ:</b> {e}</blockquote>"
        )

    # Once restarted, reconnect to the database
    reconnect_db()

# ====================================================
#                   ADD ME
# ====================================================

@bot_app.on_message(filters.command("kidnap_me") & filters.private)
async def addme_command(client: Client, message: Message):
    await client.send_chat_action(message.chat.id, ChatAction.TYPING)
    await asyncio.sleep(0.5)

    # Send "Gen message" text
    gen_msg = await message.reply_text(
        "<b><pre>Gᴇɴ ᴍᴇssᴀɢᴇ... ᴏʜ, ᴅᴏ ʏᴏᴜ ᴋɴᴏᴡ ᴡʜᴀᴛ ɪ'ᴍ ᴛʜɪɴᴋɪɴɢ ?</pre></b>",
        parse_mode=ParseMode.HTML
    )

    await asyncio.sleep(0.5)

    # Edit the message to "Done sending"
    await gen_msg.edit_text(
        "<b><pre>Dᴏɴᴇ sᴇɴᴅɪɴɢ... ᴡᴏʏᴏᴜ ʜɪᴛ ᴍʏ ᴍɪɴᴅ, ɴᴏᴡ ?</pre></b>",
        parse_mode=ParseMode.HTML
    )

    await asyncio.sleep(0.5)

    # Send the sticker
    sticker_id = "CAACAgUAAxkBAAEOXBhoCoKZ76jevKX-Vc5v5SZhCeQAAXMAAh4KAALJrhlVZygbxFWWTLw2BA"
    await message.reply_sticker(sticker=sticker_id)

    await asyncio.sleep(0.5)

    # Send the add-me menu
    await send_addme_menu(message)

async def send_addme_menu(message_or_query):
    photo_url = "https://i.ibb.co/PzQBGF5d/photo-2025-04-29-09-11-07-7498660153151979536.jpg"
    buttons = InlineKeyboardMarkup([
        [
            InlineKeyboardButton("➕ Aᴅᴅ ᴍᴇ ᴛᴏ ᴄʜᴀɴɴᴇʟ", callback_data="add_channel"),
            InlineKeyboardButton("➕ Aᴅᴅ ᴍᴇ ᴛᴏ ɢʀᴏᴜᴘ", callback_data="add_group")
        ],
        [
            InlineKeyboardButton("Cʟᴏsᴇ ✖", callback_data="close")
        ]
    ])
    
    caption = (
        "<b><blockquote>Wʜᴇʀᴇ ᴅᴏ ʏᴏᴜ ᴅʀᴇᴀᴍ ᴏғ ᴘʟᴀᴄɪɴɢ ᴍᴇ... ɪɴ ᴛʜᴇ ᴄᴏʀɴᴇʀs ᴏғ ʏᴏᴜʀ ʜᴇᴀʀᴛ ᴡʜᴇʀᴇ ɴᴏ ᴏɴᴇ ᴇʟsᴇ ᴄᴀɴ ᴛᴏᴜᴄʜ, ᴏʀ ɪɴ ʏᴏᴜʀ ᴀʀᴍꜱ ᴡʜᴇʀᴇ ᴇᴠᴇʀʏ ʙᴇᴀᴛ ᴏғ ʏᴏᴜʀ ʜᴇᴀʀᴛ ᴡʜɪsᴘᴇʀs ᴍʏ ɴᴀᴍᴇ ?</blockquote></b>\n"
        "<pre><b>Cʜᴏᴏsᴇ ᴀɴ ᴏᴘᴛɪᴏɴ ʙᴇʟᴏᴡ :</b></pre>"
    )

    if isinstance(message_or_query, CallbackQuery):
        await message_or_query.message.edit_media(
            media=InputMediaPhoto(
                media=photo_url,
                caption=caption,
                parse_mode=ParseMode.HTML
            ),
            reply_markup=buttons
        )
    else:
        await message_or_query.reply_photo(
            photo=photo_url,
            caption=caption,
            reply_markup=buttons,
            parse_mode=ParseMode.HTML
        )

@bot_app.on_callback_query(filters.regex("add_channel"))
async def add_channel_callback(client: Client, callback_query: CallbackQuery):
    await callback_query.answer()
    photo_url = "https://i.ibb.co/TMpqf7kV/photo-2025-04-28-19-28-49-7498448256645464084.jpg"
    buttons = InlineKeyboardMarkup([
        [
            InlineKeyboardButton("「  Aᴅᴅ ᴛᴏ ᴄʜᴀɴɴᴇʟ  」", url="https://t.me/Private_Auto_Approval_Bot?startchannel=true")
        ],
        [
            InlineKeyboardButton("« Bᴀᴄᴋ", callback_data="addme_back"),
            InlineKeyboardButton("Cʟᴏsᴇ ✖", callback_data="close")
        ]
    ])
    await callback_query.message.edit_media(
        media=InputMediaPhoto(
            media=photo_url,
            caption="<blockquote>Aᴅᴅ ᴍᴇ ᴛᴏ ʏᴏᴜʀ <b>ᴄʜᴀɴɴᴇʟ</b> ᴀɴᴅ ʟᴇᴛ ᴍᴇ ᴘᴀɪɴᴛ ʏᴏᴜʀ ᴅᴀʏs ᴡɪᴛʜ ᴀ ꜱᴘᴀʀᴋ ᴏғ ᴍʏ ᴘʀᴇꜱᴇɴᴄᴇ... ᴊᴜꜱᴛ ᴄʟɪᴄᴋ ᴛʜᴇ ʙᴜᴛᴛᴏɴ ʙᴇʟᴏᴡ.</blockquote>",
            parse_mode=ParseMode.HTML
        ),
        reply_markup=buttons
    )

@bot_app.on_callback_query(filters.regex("add_group"))
async def add_group_callback(client: Client, callback_query: CallbackQuery):
    await callback_query.answer()
    photo_url = "https://i.ibb.co/hRgKXFsq/photo-2025-04-28-19-28-57-7498448286710235152.jpg"
    buttons = InlineKeyboardMarkup([
        [
            InlineKeyboardButton("「  Aᴅᴅ ᴛᴏ ɢʀᴏᴜᴘ  」", url="https://t.me/Private_Auto_Approval_Bot?startgroup=true")
        ],
        [
            InlineKeyboardButton("« Bᴀᴄᴋ", callback_data="addme_back"),
            InlineKeyboardButton("Cʟᴏsᴇ ✖", callback_data="close")
        ]
    ])
    await callback_query.message.edit_media(
        media=InputMediaPhoto(
            media=photo_url,
            caption="<blockquote>Aᴅᴅ ᴍᴇ ᴛᴏ ʏᴏᴜʀ ɢʀᴏᴜᴘ ᴀɴᴅ ᴡᴀᴛᴄʜ ᴍᴇ ᴀᴘᴘʀᴏᴠᴇ ᴛʜᴇ ʙᴇꜱᴛ ᴘᴇᴏᴘʟᴇ ᴛᴏ ꜰɪᴛ ᴏᴜʀ ᴠɪʙᴇ... ʙᴜᴛ ʀᴇᴍᴇᴍʙᴇʀ, ɴᴏ ᴏɴᴇ ꜰɪᴛꜱ ʟɪᴋᴇ ᴍᴇ.</blockquote>",
            parse_mode=ParseMode.HTML
        ),
        reply_markup=buttons
    )

@bot_app.on_callback_query(filters.regex("close"))
async def close_callback(client: Client, callback_query: CallbackQuery):
    await callback_query.answer()
    await callback_query.message.delete()

@bot_app.on_callback_query(filters.regex("addme_back"))
async def back_callback(client: Client, callback_query: CallbackQuery):
    await callback_query.answer()
    await send_addme_menu(callback_query)
        
# ====================================================
#                    BOT START
# ====================================================

print("I'm Alive Now!")
if __name__ == "__main__":
    user_app.start()
    bot_app.run()
