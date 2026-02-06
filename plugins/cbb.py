# Minimal callback handler for banuser.py and request_fsub.py support
from pyrogram import Client, filters
from pyrogram.types import CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton
from bot import Bot
from database.database import db

print("[CBB] Loading minimal callback handler for banuser & request_fsub...")

@Bot.on_callback_query()
async def cb_handler(client: Bot, query: CallbackQuery):
    data = query.data
    user_id = query.from_user.id
    
    print(f"[CBB] Callback received: {data} from user {user_id}")

    # ============================================
    # CLOSE CALLBACK (for banuser.py)
    # ============================================
    if data == "close":
        await query.message.delete()
        try:
            await query.message.reply_to_message.delete()
        except:
            pass
        print(f"[CBB] Closed message for user {user_id}")

    # ============================================
    # FORCE SUB CALLBACKS (for request_fsub.py)
    # ============================================
    
    elif data.startswith("rfs_ch_"):
        """View channel force-sub mode settings"""
        cid = int(data.split("_")[2])
        try:
            chat = await client.get_chat(cid)
            mode = await db.get_channel_mode(cid)
            status = "🟢 ᴏɴ" if mode == "on" else "🔴 ᴏғғ"
            new_mode = "off" if mode == "on" else "on"
            buttons = [
                [InlineKeyboardButton(f"ʀᴇǫ ᴍᴏᴅᴇ {'OFF' if mode == 'on' else 'ON'}", callback_data=f"rfs_toggle_{cid}_{new_mode}")],
                [InlineKeyboardButton("‹ ʙᴀᴄᴋ", callback_data="fsub_back")]
            ]
            await query.message.edit_text(
                f"<b>Channel:</b> {chat.title}\n<b>Current Force-Sub Mode:</b> {status}",
                reply_markup=InlineKeyboardMarkup(buttons)
            )
            print(f"[CBB] Showed force-sub settings for channel {cid}")
        except Exception as e:
            print(f"[CBB] Error fetching channel {cid}: {e}")
            await query.answer("Failed to fetch channel info", show_alert=True)

    elif data.startswith("rfs_toggle_"):
        """Toggle force-sub mode ON/OFF for a channel"""
        cid, action = data.split("_")[2:]
        cid = int(cid)
        mode = "on" if action == "on" else "off"

        await db.set_channel_mode(cid, mode)
        await query.answer(f"✅ Force-Sub set to {'ON' if mode == 'on' else 'OFF'}")
        print(f"[CBB] Toggled force-sub mode to {mode} for channel {cid}")

        # Refresh the channel settings view
        try:
            chat = await client.get_chat(cid)
            status = "🟢 ON" if mode == "on" else "🔴 OFF"
            new_mode = "off" if mode == "on" else "on"
            buttons = [
                [InlineKeyboardButton(f"ʀᴇǫ ᴍᴏᴅᴇ {'OFF' if mode == 'on' else 'ON'}", callback_data=f"rfs_toggle_{cid}_{new_mode}")],
                [InlineKeyboardButton("‹ ʙᴀᴄᴋ", callback_data="fsub_back")]
            ]
            await query.message.edit_text(
                f"<b>Channel:</b> {chat.title}\n<b>Current Force-Sub Mode:</b> {status}",
                reply_markup=InlineKeyboardMarkup(buttons)
            )
        except Exception as e:
            print(f"[CBB] Error refreshing channel {cid}: {e}")

    elif data == "fsub_back":
        """Go back to force-sub channels list"""
        channels = await db.show_channels()
        buttons = []
        for cid in channels:
            try:
                chat = await client.get_chat(cid)
                mode = await db.get_channel_mode(cid)
                status = "🟢" if mode == "on" else "🔴"
                buttons.append([InlineKeyboardButton(f"{status} {chat.title}", callback_data=f"rfs_ch_{cid}")])
            except Exception as e:
                print(f"[CBB] Error loading channel {cid}: {e}")
                continue

        if not buttons:
            buttons.append([InlineKeyboardButton("❌ No channels found", callback_data="close")])

        await query.message.edit_text(
            "<b>⚡ Sᴇʟᴇᴄᴛ ᴀ ᴄʜᴀɴɴᴇʟ ᴛᴏ ᴛᴏɢɢʟᴇ ɪᴛs ғᴏʀᴄᴇ-sᴜʙ ᴍᴏᴅᴇ:</b>",
            reply_markup=InlineKeyboardMarkup(buttons)
        )
        print(f"[CBB] Showed force-sub channels list")

print("[CBB] ✅ Minimal callback handler loaded successfully!")
