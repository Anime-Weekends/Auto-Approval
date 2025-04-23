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

from database import add_user, add_group, all_users, all_groups, users, remove_user
from database import add_admin_db, remove_admin_db, list_admins_db, is_admin
from configs import cfg
from database import datetime
from database import is_sudo

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
        
        # Create the buttons with the three desired actions
        keyboard = InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton("⚡", callback_data="popup_action")  # Popup Button
                ],
                [
                    InlineKeyboardButton("Mᴀɪɴ Cʜᴀɴɴᴇʟ", url="https://t.me/EmitingStars_Botz"),  # URL Button 1
                    InlineKeyboardButton("Sᴜᴘᴘᴏʀᴛ", url="https://t.me/Private_Auto_Approval_Bot")  # URL Button 2
                ]
            ]
        )
        
        # Send a welcome message with a photo and the buttons
        await app.send_photo(
            user.id,
            "https://i.ibb.co/F9JM2pq/photo-2025-03-13-19-25-04-7481377376551567376.jpg",
            caption=f"**🍁 Hᴇʏ {user.mention}!\n\nʏᴏᴜʀ ʀᴇǫᴜᴇsᴛ ʜᴀs ʙᴇᴇɴ ᴀᴘᴘʀᴏᴠᴇᴅ!.. ᴡᴇʟᴄᴏᴍᴇ ᴛᴏ  {chat.title}\n\n__<blockquote>ʙʏ: <a href=https://t.me/EmitingStars_Botz>Eᴍɪᴛɪɴɢ Sᴛᴀʀs</blockquote></a>__**",
            reply_markup=keyboard, 
            message_effect_id=5104841245755180586 #🔥
        )
        add_user(user.id)

    except errors.PeerIdInvalid:
        print("User isn't a proper peer (possibly a group)")
    except Exception as err:
        print(str(err))

# Handle the popup button press
@app.on_callback_query(filters.regex("popup_action"))
async def popup_action(_, cb: CallbackQuery):
    await cb.answer("This is a popup message!", show_alert=True)
    
# ====================================================
#                      START
# ====================================================

from pyrogram.types import InputMediaPhoto

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

        return await m.reply_photo(
            photo="https://example.com/image.jpg",  # Replace with your image URL or file path
            caption="**<blockquote>⚠️ Aᴄᴄᴇss ᴅᴇɴɪᴇᴅ! ⚠️\n\nYou must join the required channel first. Please do so and try again.</blockquote>**",
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
        reply_markup=keyboard, 
        message_effect_id=5104841245755180586 #🔥
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

@app.on_message(filters.command("users") & is_sudo())
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
    
@app.on_callback_query(filters.regex("close_stats"))
async def close_stats(_, cb: CallbackQuery):
    await cb.message.delete()
    await cb.answer("Closed!", show_alert=True)
    
# ====================================================
#                 BROADCAST (COPY)
# ====================================================

@app.on_message(filters.command("bcast") & is_sudo())
async def bcast(_, m: Message):
    global canceled
    canceled = False

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

    total_users = users.count_documents({})
    stats = {"success": 0, "failed": 0, "deactivated": 0, "blocked": 0}

    for idx, u in enumerate(users.find(), 1):
        if canceled:
            await lel.edit(
                "❌ Broadcast process has been canceled.",
                reply_markup=InlineKeyboardMarkup(
                    [[InlineKeyboardButton("Close", callback_data="close_bcast")]]
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
                    InlineKeyboardButton("Cancel", callback_data="cancel_bcast"),
                    InlineKeyboardButton("Close", callback_data="close_bcast")
                ]]
            )
        )

        try:
            await m.reply_to_message.copy(int(u["user_id"]))
            stats["success"] += 1
        except UserDeactivated:
            stats["deactivated"] += 1
        except UserBlocked:
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
                [[InlineKeyboardButton("Close", callback_data="close_bcast")]]
            )
        )

# ====================================================
#               BROADCAST (FORWARD)
# ====================================================

@app.on_message(filters.command("fcast") & is_sudo())
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
#                    HELP CENTER
# ====================================================

@app.on_message(filters.private & filters.command("help"))
async def help_command(_, m: Message):
    keyboard = InlineKeyboardMarkup([
        [
            InlineKeyboardButton("👨‍💻 Support", url="https://t.me/YourSupportChannel"),
            InlineKeyboardButton("📢 Main Channel", url="https://t.me/YourMainChannel")
        ],
        [
            InlineKeyboardButton("💬 FAQ", url="https://t.me/YourFAQChannel"),
            InlineKeyboardButton("❓ Ask a Question", url="https://t.me/YourSupportBot")
        ]
    ])

    # Send the help message with buttons and an image
    await m.reply_photo(
        "https://i.ibb.co/F9JM2pq/photo-2025-03-13-19-25-04-7481377376551567376.jpg",  # Replace with your image link
        caption="**<b>Here is how you can use the bot:</b>\n\n"
                "1. Click on the buttons to access different features.\n"
                "2. Reach out to support if you have any questions.\n"
                "3. Subscribe to the main channel for updates.\n"
                "4. Check the FAQ if you're having trouble.\n\n"
                "Feel free to ask if you need more help!**",
        reply_markup=keyboard
    )

# ====================================================
#                    ADMIMS
# ====================================================

@app.on_message(filters.command("addadmin") & is_sudo())
async def addadmin(_, m: Message):
    if len(m.command) < 2 or not all(x.isdigit() for x in m.command[1:]):
        return await m.reply(
            "Yᴏᴜ ɴᴇᴇᴅ ᴛᴏ ᴀᴅᴅ Aᴅᴍɪɴ ɪᴅs<br><br>"
            "<b>EXAMPLE:</b><br>"
            "<blockquote>/addadmin 123456789 — ᴀᴅᴅ ᴏɴᴇ ᴜsᴇʀ<br>"
            "/addadmin 123456789 987654321 — ᴀᴅᴅ ᴍᴜʟᴛɪᴘʟᴇ ᴜsᴇʀs</blockquote>",
            parse_mode=ParseMode.HTML
        )

    added = []
    for user_id in m.command[1:]:
        uid = int(user_id)
        if not is_admin(uid):
            add_admin_db(uid)
            added.append(uid)

    if not added:
        return await m.reply("All provided users are already admins.", parse_mode=ParseMode.HTML)

    added_text = "\n".join([f"• <a href='tg://user?id={uid}'>{uid}</a>" for uid in added])
    await m.reply(
        f"✅ The following user(s) were added as admins:\n{added_text}",
        parse_mode=ParseMode.HTML
    )


@app.on_message(filters.command("removeadmin") & filters.user(cfg.SUDO))
async def removeadmin(_, m: Message):
    if len(m.command) < 2 or not m.command[1].isdigit():
        return await m.reply(
            "Usage: `/removeadmin <user_id>`",
            parse_mode=ParseMode.MARKDOWN
        )

    user_id = int(m.command[1])
    if not is_admin(user_id):
        return await m.reply(
            "User is not an admin.",
            parse_mode=ParseMode.MARKDOWN
        )

    remove_admin_db(user_id)
    await m.reply(
        f"❌ User [{user_id}](tg://user?id={user_id}) has been removed from admins.",
        parse_mode=ParseMode.MARKDOWN
    )


@app.on_message(filters.command("listadmin") & is_sudo())
async def listadmin(_, m: Message):
    admin_ids = list_admins_db()
    if not admin_ids:
        return await m.reply("No admins found.", parse_mode=ParseMode.MARKDOWN)
    
    lines = ["**Current Admins:**"]
    for uid in admin_ids:
        lines.append(f"• [{uid}](tg://user?id={uid}) (`{uid}`)")
    
    await m.reply("\n".join(lines), parse_mode=ParseMode.MARKDOWN)

def is_sudo():
    return filters.create(lambda _, __, m: m.from_user and (m.from_user.id in cfg.SUDO or is_admin(m.from_user.id)))

# ====================================================
#                    BOT START
# ====================================================

print("I'm Alive Now!")
app.run()
