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

@app.on_message(filters.command("users") & filters.user(cfg.SUDO))
async def dbtool(_, m: Message):
    total_users = all_users()
    total_groups = all_groups()
    total = total_users + total_groups
    
    keyboard = InlineKeyboardMarkup(
        [
            [InlineKeyboardButton("Cʟᴏsᴇ ᴄᴜᴛɪᴇ", callback_data="close_stats")]
        ]
    )

    await m.reply_photo(
        "https://i.ibb.co/F9JM2pq/photo-2025-03-13-19-25-04-7481377376551567376.jpg",
        caption=(
            f"🍀 **Chats Stats** 🍀\n"
            f"❏ Users : `{total_users}`\n"
            f"❏ Groups : `{total_groups}`\n"
            f"❏ Total : `{total}`"
        ),
        reply_markup=keyboard
    )

@app.on_callback_query(filters.regex("close_stats"))
async def close_stats(_, cb: CallbackQuery):
    await cb.message.delete()
    await cb.answer("Stats message closed.", show_alert=True)

# ====================================================
#                 BROADCAST (COPY)
# ====================================================

@app.on_message(filters.command("bcast") & filters.user(cfg.SUDO))
async def bcast(_, m: Message):
    global canceled  # Declare 'canceled' as global to ensure we can modify it in other handlers
    canceled = False  # Reset the flag

    lel = await m.reply_photo(
        "https://i.ibb.co/F9JM2pq/photo-2025-03-13-19-25-04-7481377376551567376.jpg",  # Replace with your image URL
        caption="`⚡️ Processing...`",
        reply_markup=InlineKeyboardMarkup(
            [
                [InlineKeyboardButton("Cancel", callback_data="cancel_bcast")],  # Cancel button
                [InlineKeyboardButton("Close", callback_data="close_bcast")]  # Close button
            ]
        )
    )

    total_users = users.count_documents({})
    stats = {"success": 0, "failed": 0, "deactivated": 0, "blocked": 0}
    
    # Loop through each user in the database
    for idx, u in enumerate(users.find(), 1):
        # Check if the process was canceled
        if canceled:
            await lel.edit("The broadcast process has been canceled.")
            break

        progress = int((idx / total_users) * 100)  # Calculate percentage of progress
        progress_bar = f"[{'█' * (progress // 5)}{' ' * (20 - (progress // 5))}] {progress}%"

        # Update the progress bar
        await lel.edit(
            f"Processing...\n\n"
            f"Progress: {progress_bar}\n"
            f"Success: `{stats['success']}` | Failed: `{stats['failed']}` | Deactivated: `{stats['deactivated']}` | Blocked: `{stats['blocked']}`"
        )

        try:
            # Attempt to send the message
            await m.reply_to_message.copy(int(u["user_id"]))
            stats["success"] += 1
        except Exception as e:
            # Handle specific exceptions
            if isinstance(e, UserDeactivated):
                stats["deactivated"] += 1
            elif isinstance(e, UserBlocked):
                stats["blocked"] += 1
            else:
                stats["failed"] += 1

        # Optional: Add a small delay to avoid hitting rate limits
        await asyncio.sleep(0.1)

    # Once the loop finishes, update the message with the stats
    if not canceled:
        await lel.edit(
            f"✅ Successful: `{stats['success']}`\n"
            f"❌ Failed: `{stats['failed']}`\n"
            f"👾 Blocked: `{stats['blocked']}`\n"
            f"👻 Deactivated: `{stats['deactivated']}`"
        )


@app.on_callback_query(filters.regex("cancel_bcast"))
async def cancel_bcast(_, cb: CallbackQuery):
    global canceled
    canceled = True  # Set the flag to True when cancel is pressed
    # Acknowledge the callback and inform the user
    await cb.answer("Broadcast process has been canceled.", show_alert=True)


@app.on_callback_query(filters.regex("close_bcast"))
async def close_bcast(_, cb: CallbackQuery):
    # Delete the message or edit it to indicate that the process has been closed
    await cb.message.delete()
    # Acknowledge the callback
    await cb.answer("Broadcast process has been closed.", show_alert=True)

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
