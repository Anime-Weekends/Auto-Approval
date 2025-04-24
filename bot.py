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
from pyrogram.errors import UserDeactivated, UserBlocked
from pyrogram.errors import PeerIdInvalid
from pyrogram.errors import RPCError
from database import get_total_approvals

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
        await bot_app.approve_chat_join_request(chat.id, user.id)
        
        # Inline buttons layout
        keyboard = InlineKeyboardMarkup(
            [
                [InlineKeyboardButton("Mᴀɪɴ Cʜᴀɴɴᴇʟ", url="https://t.me/EmitingStars_Botz")],  # Button with callback
                [
                    InlineKeyboardButton("Sᴜᴘᴘᴏʀᴛ", url="https://t.me/+HZuPVe0l-F1mM2Jl"), 
                    InlineKeyboardButton("Cʟɪᴄᴋ ʜᴇʀᴇ", callback_data="popup_action")
                ]
            ]
        )

        # Caption with user and chat links
        caption = (
            f"<b><blockquote>Hᴇʏ sᴡᴇᴇᴛɪᴇ</b> <a href='tg://user?id={user.id}'>{user.first_name}</a>  ⭐✨</blockquote>\n\n"
            f"<blockquote>Aᴄᴄᴇss ʜᴀs ʙᴇᴇɴ <b>Gʀᴀɴᴛᴇᴅ</b> sᴛᴇᴘ ɪɴᴛᴏ ᴛʜᴇ ᴘʀᴇsᴛɪɢɪᴏᴜs ʜᴀʟʟs ᴏғ "
            f"<a href='https://t.me/c/{str(chat.id)[4:]}'>{chat.title}</a></blockquote>\n"
            f"<i><blockquote>Pʀᴇsᴇɴᴛᴇᴅ ᴡɪᴛʜ ʜᴏɴᴏʀ ʙʏ <a href='https://t.me/EmitingStars_Botz'>Eᴍɪᴛɪɴɢ sᴛᴀʀs</a></blockquote></i>"
        )
        
        # Sending a photo with the message and buttons
        await bot_app.send_photo(
            user.id,
            "https://i.ibb.co/vxMhkZQD/photo-2025-04-23-20-40-27-7496611286248062984.jpg",
            caption=caption,
            reply_markup=keyboard,
            parse_mode=ParseMode.HTML,
            message_effect_id=5046509860389126442 #🎉
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
    await cb.answer("Iғ ɪ ᴄʀᴏssᴇᴅ ɢᴀʟᴀxɪᴇs ᴀɴᴅ ʙᴇɴᴛ ᴛɪᴍᴇ ᴊᴜsᴛ ᴛᴏ ғɪɴᴅ ʏᴏᴜ, ɪᴛ’ᴅ sᴛɪʟʟ ʙᴇ ᴡᴏʀᴛʜ ᴇᴠᴇʀʏ sᴜᴘᴇʀɴᴏᴠᴀ—ʙᴇᴄᴀᴜsᴇ ɪɴ ᴀʟʟ ᴛʜᴇ ᴍᴜʟᴛɪᴠᴇʀsᴇs, ʏᴏᴜ'ʀᴇ ᴛʜᴇ ᴏɴʟʏ ᴄᴏɴsᴛᴀɴᴛ ᴍʏ ʜᴇᴀʀᴛ ᴏʀʙɪᴛs.", show_alert=True)
    
# ====================================================
#                      START
# ====================================================

from pyrogram.types import InputMediaPhoto

@bot_app.on_message(filters.private & filters.command("start"))
async def start_command(_, m: Message):
    welcome_text = "<i>ᴡᴇʟᴄᴏᴍᴇ ᴛᴏ <b>ʟᴜᴄʏ</b>.\nʜᴏᴘᴇ ʏᴏᴜ'ʀᴇ ᴅᴏɪɴɢ ᴡᴇʟʟ...</i>"

    stickers = [
        "CAACAgUAAxkBAAEOW3hoCf_Za5Dh_qsmeH4OKtJpOEDhggACNwoAApLnMFfso_6k-QJv-zYE",
        "CAACAgUAAxkBAAEOW3poCf_m_FMYs55gjI312AJxgvItxAACzQsAAhjwMVePhvS36tzPHzYE"
    ]

    start_pics = [
        "https://i.ibb.co/v6J0JM80/photo-2025-03-13-18-50-40-7481368571868610580.jpg",
        "https://i.ibb.co/C5N2Xhk9/photo-2025-04-19-18-11-35-7496424313436766224.jpg",
        "https://i.ibb.co/vxMhkZQD/photo-2025-04-23-20-40-27-7496611286248062984.jpg"
    ]

    msg = await m.reply_text(welcome_text)
    await asyncio.sleep(0.2)
    await msg.edit_text("<b><i>ꜱᴛᴀʀᴛɪɴɢ...</i></b>")
    await asyncio.sleep(0.2)
    await msg.delete()

    await m.reply_sticker(random.choice(stickers))

    try:
        await bot_app.get_chat_member(cfg.CHID, m.from_user.id)
    except:
        try:
            invite_link = await app.create_chat_invite_link(cfg.CHID)
        except:
            return await m.reply("**<blockquote>Mᴀᴋᴇ sᴜʀᴇ ɪ ᴀᴍ ᴀɴ ᴀᴅᴍɪɴ ɪɴ ʏᴏᴜʀ ᴄʜᴀɴɴᴇʟ</blockquote>**")

        button = InlineKeyboardMarkup([
            [InlineKeyboardButton("Jᴏɪɴ ʜᴇʀᴇ", url=invite_link.invite_link)],
            [InlineKeyboardButton("Rᴇғʀᴇsʜ", url="https://t.me/Private_Auto_Approval_Bot?start=start")]
        ])

        return await m.reply_photo(
            photo=random.choice(start_pics),
            caption="<b><blockquote>Esᴛᴇᴇᴍᴇᴅ ɢᴜᴇsᴛ,</blockquote></b>\n<blockquote expandable>ᴀᴄᴄᴇss ᴛᴏ ᴍʏ sᴇʀᴠɪᴄᴇs...</blockquote>",
            reply_markup=button,
            parse_mode=ParseMode.HTML,
            message_effect_id=5104841245755180586
        )

    add_user(m.from_user.id)

    keyboard = InlineKeyboardMarkup([
        [
            InlineKeyboardButton("Mᴀɪɴ ᴄʜᴀɴɴᴇʟ", url="https://t.me/EmitingStars_Botz"),
            InlineKeyboardButton("Sᴜᴘᴘᴏʀᴛ", url="https://t.me/+HZuPVe0l-F1mM2Jl")
        ],
        [
            InlineKeyboardButton("⤬ Kɪᴅɴᴀᴘᴘ ᴍᴇ ʙᴀʙʏ ⤬", url="http://t.me/Private_Auto_Approval_Bot?startchannel=true")
        ],
        [
            InlineKeyboardButton("⧉ Aʙᴏᴜᴛ", callback_data="about")
        ]
    ])

    await m.reply_photo(
        random.choice(start_pics),
        caption=(
            f"🍁 <b>Hello</b> <a href='tg://user?id={m.from_user.id}'>{m.from_user.first_name}</a>!\n\n"
            "I'm an auto-approve bot. Add me to your chat and promote me to admin "
            "with <b>Add Members</b> permission."
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
            InlineKeyboardButton("⨉ Cʟᴏsᴇ", callback_data="close_msg")
        ]
    ])
    await cq.message.edit_media(
        media=InputMediaPhoto(
            media="https://i.ibb.co/vxMhkZQD/photo-2025-04-23-20-40-27-7496611286248062984.jpg",  # Your about image
            caption=(
                "<b>About ʟᴜᴄʏ</b>\n\n"
                "A sleek auto-approval bot for Telegram.\n"
                "Created to simplify managing join requests.\n"
                "Fast, aesthetic, and private.\n\n"
                "<i>Made with love by the team.</i>"
            ),
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
            InlineKeyboardButton("⤬ Kɪᴅɴᴀᴘᴘ ᴍᴇ ʙᴀʙʏ ⤬", url="http://t.me/Private_Auto_Approval_Bot?startchannel=true")
        ],
        [
            InlineKeyboardButton("⧉ Aʙᴏᴜᴛ", callback_data="about")
        ]
    ])
    await cq.message.edit_media(
        media=InputMediaPhoto(
            media="https://i.ibb.co/v6J0JM80/photo-2025-03-13-18-50-40-7481368571868610580.jpg",  # Your start image
            caption=(
                f"🍁 <b>Hello</b> <a href='tg://user?id={cq.from_user.id}'>{cq.from_user.first_name}</a>!\n\n"
                "I'm an auto-approve bot. Add me to your chat and promote me to admin "
                "with <b>Add Members</b> permission."
            ),
            parse_mode=ParseMode.HTML
        ),
        reply_markup=keyboard
    )


@bot_app.on_callback_query(filters.regex("close_msg"))
async def close_message(_, cq: CallbackQuery):
    await cq.answer()
    await cq.message.delete()


# ====================================================
#                   CALLBACK CHECK
# ====================================================

@bot_app.on_callback_query(filters.regex("chk"))
async def chk_callback(_, cb: CallbackQuery):
    try:
        await bot_app.get_chat_member(cfg.CHID, cb.from_user.id)
    except:
        return await cb.answer(
            "Yᴏᴜ ʜᴀᴠᴇɴ'ᴛ ᴊᴏɪɴᴇᴅ ᴏᴜʀ ᴄʜᴀɴɴᴇʟ ʏᴇᴛ. ᴘʟᴇᴀsᴇ ᴊᴏɪɴ ᴀɴᴅ ᴛʀʏ ᴀɢᴀɪɴ!",
            show_alert=True
        )

    keyboard = InlineKeyboardMarkup([
        [
            InlineKeyboardButton("Mᴀɪɴ ᴄʜᴀɴɴᴇʟ", url="https://t.me/EmitingStars_Botz"),
            InlineKeyboardButton("Sᴜᴘᴘᴏʀᴛ", url="https://t.me/+HZuPVe0l-F1mM2Jl")
        ],
        [
            InlineKeyboardButton("⤬ Kɪᴅɴᴀᴘᴘ ᴍᴇ ʙᴀʙʏ ⤬", url="http://t.me/Private_Auto_Approval_Bot?startchannel=true")
        ]
    ])

    add_user(cb.from_user.id)

    await cb.edit_message_text(
        f"🍁 <b>Hello</b> {cb.from_user.mention()}!\n\n"
        "I'm an <b>auto-approve bot</b>. Add me to your chat and promote me to admin "
        "with <b>Add Members</b> permission.",
        reply_markup=keyboard,
        parse_mode=ParseMode.HTML, 
        message_effect_id=5104841245755180586 #🔥
    )

# ====================================================
#                      INFO CMD
# ====================================================

@bot_app.on_message(filters.command("status") & is_sudo())
async def dbtool(_, m: Message):
    # Animation sequence
    welcome_text = "<pre>Pʀᴇᴘᴀʀɪɴɢ sᴛᴀᴛᴜs ʀᴇᴘᴏʀᴛ...</pre>"
    msg = await m.reply_text(welcome_text)
    await asyncio.sleep(0.2)
    await msg.edit_text("<b><i><pre>Dᴏɴᴇ sᴇɴᴅɪɴɢ...</pre></i></b>")
    await asyncio.sleep(0.1)
    await msg.delete()

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
        photo="https://i.ibb.co/gbbYfsXt/photo-2025-04-24-11-50-49-7496845877361770512.jpg",
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
        "CAACAgUAAxkBAAEOW3hoCf_Za5Dh_qsmeH4OKtJpOEDhggACNwoAApLnMFfso_6k-QJv-zYE",
        "CAACAgUAAxkBAAEOW3poCf_m_FMYs55gjI312AJxgvItxAACzQsAAhjwMVePhvS36tzPHzYE"
    ]
    
# ====================================================
#                 BROADCAST (COPY)
# ====================================================

@bot_app.on_message(filters.command("broadcast") & is_sudo())
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

@bot_app.on_message(filters.command("fbroadcast") & is_sudo())
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
    welcome_text = "<pre>Cʀᴇᴀᴛɪɴɢ ᴍᴇssᴀɢᴇ... </pre>"
    msg = await m.reply_text(welcome_text)
    await asyncio.sleep(0.2)
    await msg.edit_text("<b><i><pre>Dᴏɴᴇ sᴇɴᴅɪɴɢ...</pre></i></b>")
    await asyncio.sleep(0.1)
    await msg.delete()

    # Random sticker from a predefined list
    stickers = [
        "CAACAgUAAxkBAAIBgWYqY3yMZMJYkuf5tLxjBrXnK1e3AAIbAwAC2MNpVjXpWxuDqZkPMwQ",
        "CAACAgUAAxkBAAIBg2YqY4OQ8QABFzM9UcwDf90m_JA2dgACYAQAAulVZRrB8ykNP5xj9jME",
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
        "https://i.ibb.co/n88kgW8r/photo-2025-04-24-10-49-04-7496829977392840720.jpg",
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


@bot_app.on_message(filters.command("listofadmins") & is_sudo())
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
        chat_id = m.chat.id
        requests = [req async for req in user_app.get_chat_join_requests(chat_id)]

        batch_size = 50
        delay_seconds = 5
        approved = 0

        for i in range(0, len(requests), batch_size):
            batch = requests[i:i + batch_size]
            for req in batch:
                await user_app.approve_chat_join_request(chat_id, req.user.id)
                approved += 1
            await asyncio.sleep(delay_seconds)

        await m.reply(
            f"✅ Successfully approved  <b>{approved}</b> join request (s).",
            parse_mode=ParseMode.HTML,
            reply_markup=InlineKeyboardMarkup(
                [[InlineKeyboardButton("❌ Close", callback_data="close_msg")]]
            )
        )

    except PeerIdInvalid:
        await m.reply("❌ <b>Invalid group/channel ID.</b>", parse_mode=ParseMode.HTML)
    except RPCError as err:
        await m.reply(f"⚠️ <b>Telegram Error:</b> <code>{err}</code>", parse_mode=ParseMode.HTML)
    except Exception as err:
        await m.reply(f"⚠️ <b>Unexpected Error:</b> <code>{err}</code>", parse_mode=ParseMode.HTML)

@user_app.on_callback_query(filters.regex("close_msg"))
async def close_message(_, cb):
    try:
        await cb.message.delete()
    except Exception:
        await cb.answer("Couldn't delete the message.", show_alert=True)


# ====================================================
#                   USER ID
# ====================================================

@bot_app.on_message(filters.private & filters.command("approveall"))
async def help_command(_, m: Message):
    help_text = (
        "<blockquote>𝗙𝗢𝗟𝗟𝗢𝗪 𝗧𝗛𝗘𝗦𝗘 𝗦𝗧𝗘𝗣𝗦</blockquote>\n"
        "<b><blockquote>➥ Sᴛᴇᴘ 1 :</b> Aᴅᴅ ᴛʜɪs ᴛᴇʟᴇɢʀᴀᴍ ɪᴅ ᴛᴏ ʏᴏᴜʀ ᴄʜᴀɴɴᴇʟ.</blockquote>\n"
        "<b><blockquote>➥ Sᴛᴇᴘ 2 :</b> Mᴀᴋᴇ ᴛʜɪs ɪᴅ ᴀs ᴀᴅᴍɪɴ</blockquote>\n"
        "<b><blockquote>➥ Sᴛᴇᴘ 3 :</b> Sᴇɴᴅ ᴛʜᴇ /acceptall ᴄᴏᴍᴍᴀɴᴅ ɪɴ ʏᴏᴜʀ ᴄʜᴀɴɴᴇʟ ᴛᴏ ᴀᴘᴘʀᴏᴠᴇ ᴀʟʟ ᴘᴇɴᴅɪɴɢ ʀᴇǫᴜᴇsᴛs. ᴏɴᴄᴇ ᴅᴏɴᴇ, ʀᴇᴍᴏᴠᴇ ᴛʜɪs ɪᴅ ғʀᴏᴍ ʏᴏᴜʀ ᴄʜᴀɴɴᴇʟ.</blockquote>"
    )

    # Image URL or file path (you can use a URL to the image)
    image_url = "https://i.ibb.co/xSG8wZJD/photo-2025-04-24-11-20-18-7496838026161553424.jpg"  # Replace with your image URL or file path

    buttons = InlineKeyboardMarkup([
        [
            InlineKeyboardButton("Sᴜᴘᴘᴏʀᴛ", url="https://t.me/+HZuPVe0l-F1mM2Jl")
        ],
        [
            InlineKeyboardButton("Dᴇᴠᴇʟᴏᴘᴇʀ", url="https://t.me/RexySama"),
            InlineKeyboardButton("Cʟᴏsᴇ ✖", callback_data="close_msg")
        ]
    ])

    # Send the help message with an image
    await m.reply_photo(
        photo=image_url,
        caption=help_text,
        reply_markup=buttons,
        parse_mode=ParseMode.HTML, 
        message_effect_id=5046509860389126442 #🎉
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
    user_id = message.chat.id
    photo_url = "https://i.ibb.co/YzFqHky/photo-2025-04-15-09-14-30-7493465832589099024.jpg"

    buttons = InlineKeyboardMarkup([
        [
            InlineKeyboardButton("Dᴇᴠᴇʟᴏᴘᴇʀ", url="https://t.me/RexySama"),
            InlineKeyboardButton("❌ Close", callback_data="close")
        ]
    ])

    await message.reply_photo(
        photo=photo_url,
        caption=f"<b>Your user ID is:</b> <code>{user_id}</code>",
        reply_markup=buttons,
        quote=True,
        parse_mode=ParseMode.HTML
    )

@bot_app.on_callback_query(filters.regex("close"))
async def close_callback(client, callback_query):
    await callback_query.message.delete()
    await callback_query.answer()


# ====================================================
#                   TOTAL APPROVED
# ====================================================

@user_app.on_message(filters.command("totalapproved") & is_sudo())
async def total_approved(_, m: Message):
    try:
        total = get_total_approvals()
        await m.reply(
            f"✅ <b>Total users approved by the bot:</b> <code>{total}</code>",
            parse_mode=ParseMode.HTML
        )
    except Exception as e:
        await m.reply(
            f"⚠️ <b>Error:</b> <code>{e}</code>",
            parse_mode=ParseMode.HTML
        )
        
# ====================================================
#                    BOT START
# ====================================================

print("I'm Alive Now!")
if __name__ == "__main__":
    user_app.start()
    bot_app.run()
