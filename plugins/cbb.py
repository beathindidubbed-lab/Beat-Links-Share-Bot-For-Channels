# Don't Remove Credit @BeatAnime, @mebeet1
# Ask Doubt on telegram @Beat_Anime_Discussion
#
# Copyright (C) 2025 by Beat Anime-Bots@Github, < https://github.com/beathindidubbed-lab >.
#
# This file is part of < https://github.com/beathindidubbed-lab/Advance-File-Share-bot-V4 > project,
# and is released under the MIT License.
# Please see < https://github.com/beathindidubbed-lab/Advance-File-Share-bot-V4/blob/master/LICENSE >
#
# All rights reserved.

import random
import os
import psutil
import asyncio
from datetime import datetime, timezone
from pyrogram import Client 
from bot import Bot
from config import *
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
from database.database import *
from helper_func import get_readable_time, get_exp_time

print("[CBB] Loading COMPLETE callback handler module...")

# ============================================
# IMAGE HANDLING WITH LOGGING
# ============================================

def get_random_pic_with_logging(pic_list, pic_name="Picture"):
    """Get random picture with error logging"""
    try:
        if not pic_list or pic_list == [""]:
            print(f"[CBB] ⚠️ {pic_name} list is empty, using fallback")
            return "https://telegra.ph/file/6ceef6a98b82b0e0e2f03.jpg"
        
        # Filter out empty strings
        valid_pics = [pic.strip() for pic in pic_list if pic.strip()]
        
        if not valid_pics:
            print(f"[CBB] ⚠️ No valid {pic_name} URLs found, using fallback")
            return "https://telegra.ph/file/6ceef6a98b82b0e0e2f03.jpg"
        
        selected = random.choice(valid_pics)
        print(f"[CBB] ✅ Selected {pic_name}: {selected[:50]}...")
        return selected
    except Exception as e:
        print(f"[CBB] ❌ Error selecting {pic_name}: {e}")
        return "https://telegra.ph/file/6ceef6a98b82b0e0e2f03.jpg"


# Get help pictures
HELP_PICS_LIST = os.environ.get("HELP_PICS", "").split(",")
if not HELP_PICS_LIST or HELP_PICS_LIST == [""]:
    HELP_PICS_LIST = [
        "https://telegra.ph/file/ec17880d61180d3312d6a.jpg",
        "https://telegra.ph/file/e292b12890b8b4b9dcbd1.jpg"
    ]

# Get start pictures
START_PICS_LIST = os.environ.get("START_PICS", "").split(",")
if not START_PICS_LIST or START_PICS_LIST == [""]:
    START_PICS_LIST = [START_PIC] if START_PIC else ["https://telegra.ph/file/ec17880d61180d3312d6a.jpg"]

# Get auto delete pictures
AUTO_DEL_PICS_LIST = os.environ.get("AUTO_DELETE_PICS", "").split(",")
if not AUTO_DEL_PICS_LIST or AUTO_DEL_PICS_LIST == [""]:
    AUTO_DEL_PICS_LIST = ["https://telegra.ph/file/6ceef6a98b82b0e0e2f03.jpg"]

# Get files pictures
FILES_PICS_LIST = os.environ.get("FILES_PICS", "").split(",")
if not FILES_PICS_LIST or FILES_PICS_LIST == [""]:
    FILES_PICS_LIST = ["https://telegra.ph/file/6ceef6a98b82b0e0e2f03.jpg"]


def get_random_help_pic():
    return get_random_pic_with_logging(HELP_PICS_LIST, "Help Picture")

def get_random_start_pic():
    return get_random_pic_with_logging(START_PICS_LIST, "Start Picture")

def get_auto_delete_pic():
    return get_random_pic_with_logging(AUTO_DEL_PICS_LIST, "Auto Delete Picture")

def get_files_pic():
    return get_random_pic_with_logging(FILES_PICS_LIST, "Files Picture")


# ============================================
# STATS HELPER FUNCTIONS
# ============================================

def get_system_stats():
    """Get detailed system statistics"""
    cpu_percent = psutil.cpu_percent(interval=1)
    cpu_freq = psutil.cpu_freq()
    cpu_count_physical = psutil.cpu_count(logical=False)
    cpu_count_logical = psutil.cpu_count(logical=True)
    memory = psutil.virtual_memory()
    swap = psutil.swap_memory()
    disk = psutil.disk_usage('/')
    disk_io = psutil.disk_io_counters()
    net_io = psutil.net_io_counters()
    os_uptime = datetime.now(timezone.utc) - datetime.fromtimestamp(psutil.boot_time(), tz=timezone.utc)
    
    return {
        'cpu_percent': cpu_percent,
        'cpu_freq': cpu_freq.current if cpu_freq else 0,
        'cpu_physical': cpu_count_physical,
        'cpu_logical': cpu_count_logical,
        'memory': memory,
        'swap': swap,
        'disk': disk,
        'disk_io': disk_io,
        'net_io': net_io,
        'os_uptime': os_uptime,
        'os_version': os.popen('uname -v').read().strip() if os.name != 'nt' else 'Windows',
        'os_arch': os.popen('uname -m').read().strip() if os.name != 'nt' else 'x86_64'
    }

def format_bytes(bytes_value):
    """Format bytes to human readable format"""
    for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
        if bytes_value < 1024.0:
            return f"{bytes_value:.2f}{unit}"
        bytes_value /= 1024.0
    return f"{bytes_value:.2f}PB"

def get_progress_bar(percentage, length=10):
    """Create a visual progress bar"""
    filled = int(length * percentage / 100)
    bar = '▓' * filled + '░' * (length - filled)
    return f"[{bar}] {percentage:.1f}%"


# ============================================
# MAIN CALLBACK HANDLER
# ============================================

@Bot.on_callback_query()
async def cb_handler(client: Bot, query: CallbackQuery):
    data = query.data
    user_id = query.from_user.id
    
    print(f"[CBB] 📥 Callback received: {data} from user {user_id}")

    # ============================================
    # FONT CALLBACKS - PASS TO font_system.py
    # ============================================
    if data.startswith("font_"):
        print(f"[CBB] 📥 Font callback passed to font_system.py: {data}")
        # Don't return, let it be handled by font_system.py
        pass 

    # ============================================
    # BASIC NAVIGATION CALLBACKS
    # ============================================
    
    elif data == "help":
        user_name = query.from_user.first_name
        
        help_content = (
            "<b>➪ I ᴀᴍ ᴀ ᴘʀɪᴠᴀᴛᴇ ғɪʟᴇ sʜᴀʀɪɴɢ ʙᴏᴛ, ᴍᴇᴀɴᴛ ᴛᴏ ᴘʀᴏᴠɪᴅᴇ ғɪʟᴇs ᴀɴᴅ ɴᴇᴄᴇssᴀʀʏ sᴛᴜғғ ᴛʜʀᴏᴜɢʜ sᴘᴇᴄɪᴀʟ ʟɪɴᴋ ғᴏʀ sᴘᴇᴄɪғɪᴄ ᴄʜᴀɴɴᴇʟs.\n\n"
            "➪ Iɴ ᴏʀᴅᴇʀ ᴛᴏ ɢᴇᴛ ᴛʜᴇ ғɪʟᴇs ʏᴏᴜ ʜᴀᴠᴇ ᴛᴏ ᴊᴏɪɴ ᴛʜᴇ ᴀʟʟ ᴍᴇɴᴛɪᴏɴᴇᴅ ᴄʜᴀɴɴᴇʟ ᴛʜᴀᴛ I ᴘʀᴏᴠɪᴅᴇ ʏᴏᴜ ᴛᴏ ᴊᴏɪɴ. "
            "Yᴏᴜ ᴄᴀɴ ɴᴏᴛ ᴀᴄᴄᴇss ᴏʀ ɢᴇᴛ ᴛʜᴇ ғɪʟᴇs ᴜɴʟᴇss ʏᴏᴜ ᴊᴏɪɴᴇᴅ ᴀʟʟ ᴄʜᴀɴɴᴇʟs.\n\n"
            "➪ Sᴏ ᴊᴏɪɴ Mᴇɴᴛɪᴏɴᴇᴅ Cʜᴀɴɴᴇʟs ᴛᴏ ɢᴇᴛ Fɪʟᴇs ᴏʀ ɪɴɪᴛɪᴀᴛᴇ ᴍᴇssᴀɢᴇs...\n\n"
            "━ /help - Oᴘᴇɴ ᴛʜɪs ʜᴇʟᴘ ᴍᴇssᴀɢᴇ !</b>"
        )
        
        help_text = (
            f"<b>‼️ Hᴇʟʟᴏ {user_name} ~</b>\n\n"
            f"<blockquote expandable>{help_content}</blockquote>\n"
            "<b>◈ Sᴛɪʟʟ ʜᴀᴠᴇ ᴅᴏᴜʙᴛs, ᴄᴏɴᴛᴀᴄᴛ ʙᴇʟᴏᴡ ᴘᴇʀsᴏɴs/ɢʀᴏᴜᴘ ᴀs ᴘᴇʀ ʏᴏᴜʀ ɴᴇᴇᴅ !</b>"
        )
        
        await query.message.delete()
        help_pic = get_random_help_pic()
        
        try:
            await query.message.reply_photo(
                photo=help_pic,
                caption=help_text,
                reply_markup=InlineKeyboardMarkup([
                    [ InlineKeyboardButton("ᴀɴɪᴍᴇ ᴄʜᴀɴɴᴇʟ", url="https://t.me/Beat_Hindi_Dubbed"),
                      InlineKeyboardButton("ᴄᴏɴᴛᴀᴄᴛ ᴀᴅᴍɪɴ", url="https://t.me/Beat_Anime_Ocean")
                    ],
                    [InlineKeyboardButton('ʜᴏᴍᴇ', callback_data='start'),
                     InlineKeyboardButton("ᴄʟᴏꜱᴇ", callback_data='close')]
                ])
            )
            print(f"[CBB] ✅ Sent help with photo to {user_id}")
        except Exception as e:
            print(f"[CBB] ⚠️ Help photo failed for {user_id}: {e}")
            print(f"[CBB] 🔗 Failed URL: {help_pic}")
            await query.message.reply_text(
                text=help_text,
                disable_web_page_preview=True,
                reply_markup=InlineKeyboardMarkup([
                    [ InlineKeyboardButton("ᴀɴɪᴍᴇ ᴄʜᴀɴɴᴇʟ", url="https://t.me/Beat_Hindi_Dubbed"),
                      InlineKeyboardButton("ᴄᴏɴᴛᴀᴄᴛ ᴀᴅᴍɪɴ", url="https://t.me/Beat_Anime_Ocean")
                    ],
                    [InlineKeyboardButton('ʜᴏᴍᴇ', callback_data='start'),
                     InlineKeyboardButton("ᴄʟᴏꜱᴇ", callback_data='close')]
                ])
            )
    elif data == "about":
        await query.message.delete()
        start_pic = get_random_start_pic()
        
        try:
            await query.message.reply_photo(
                photo=start_pic,
                caption=ABOUT_TXT.format(first=query.from_user.first_name),
                reply_markup=InlineKeyboardMarkup([
                    [InlineKeyboardButton('ʜᴏᴍᴇ', callback_data='start'),
                     InlineKeyboardButton('ᴄʟᴏꜱᴇ', callback_data='close')]
                ])
            )
            print(f"[CBB] ✅ Sent about with photo to {user_id}")
        except Exception as e:
            print(f"[CBB] ⚠️ About photo failed for {user_id}: {e}")
            print(f"[CBB] 🔗 Failed URL: {start_pic}")
            await query.message.reply_text(
                text=ABOUT_TXT.format(first=query.from_user.first_name),
                reply_markup=InlineKeyboardMarkup([
                    [InlineKeyboardButton('ʜᴏᴍᴇ', callback_data='start'),
                     InlineKeyboardButton('ᴄʟᴏꜱᴇ', callback_data='close')]
                ])
            )

    elif data == "start":
        await query.message.delete()
        start_pic = get_random_start_pic()
        
        try:
            await query.message.reply_photo(
                photo=start_pic,
                caption=START_MSG.format(
                    first=query.from_user.first_name,
                    last=query.from_user.last_name,
                    username=None if not query.from_user.username else '@' + query.from_user.username,
                    mention=query.from_user.mention,
                    id=query.from_user.id
                ),
                reply_markup=InlineKeyboardMarkup([
                    [InlineKeyboardButton("ʜᴇʟᴘ", callback_data='help'),
                     InlineKeyboardButton("ᴀʙᴏᴜᴛ", callback_data='about')]
                ])
            )
            print(f"[CBB] ✅ Sent start with photo to {user_id}")
        except Exception as e:
            print(f"[CBB] ⚠️ Start photo failed for {user_id}: {e}")
            print(f"[CBB] 🔗 Failed URL: {start_pic}")
            await query.message.reply_text(
                text=START_MSG.format(
                    first=query.from_user.first_name,
                    last=query.from_user.last_name,
                    username=None if not query.from_user.username else '@' + query.from_user.username,
                    mention=query.from_user.mention,
                    id=query.from_user.id
                ),
                reply_markup=InlineKeyboardMarkup([
                    [InlineKeyboardButton("ʜᴇʟᴘ", callback_data='help'),
                     InlineKeyboardButton("ᴀʙᴏᴜᴛ", callback_data='about')]
                ])
            )

    elif data == "close":
        await query.message.delete()
        try:
            await query.message.reply_to_message.delete()
        except:
            pass

    # ============================================
    # FORCE SUB CALLBACKS
    # ============================================
    
    elif data.startswith("rfs_ch_"):
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
                f"Channel: {chat.title}\nCurrent Force-Sub Mode: {status}",
                reply_markup=InlineKeyboardMarkup(buttons)
            )
        except Exception as e:
            print(f"[CBB] ❌ Error in rfs_ch: {e}")
            await query.answer("Failed to fetch channel info", show_alert=True)

    elif data.startswith("rfs_toggle_"):
        cid, action = data.split("_")[2:]
        cid = int(cid)
        mode = "on" if action == "on" else "off"

        await db.set_channel_mode(cid, mode)
        await query.answer(f"Force-Sub set to {'ON' if mode == 'on' else 'OFF'}")

        chat = await client.get_chat(cid)
        status = "🟢 ON" if mode == "on" else "🔴 OFF"
        new_mode = "off" if mode == "on" else "on"
        buttons = [
            [InlineKeyboardButton(f"ʀᴇǫ ᴍᴏᴅᴇ {'OFF' if mode == 'on' else 'ON'}", callback_data=f"rfs_toggle_{cid}_{new_mode}")],
            [InlineKeyboardButton("‹ ʙᴀᴄᴋ", callback_data="fsub_back")]
        ]
        await query.message.edit_text(
            f"Channel: {chat.title}\nCurrent Force-Sub Mode: {status}",
            reply_markup=InlineKeyboardMarkup(buttons)
        )

    elif data == "fsub_back":
        channels = await db.show_channels()
        buttons = []
        for cid in channels:
            try:
                chat = await client.get_chat(cid)
                mode = await db.get_channel_mode(cid)
                status = "🟢" if mode == "on" else "🔴"
                buttons.append([InlineKeyboardButton(f"{status} {chat.title}", callback_data=f"rfs_ch_{cid}")])
            except:
                continue

        await query.message.edit_text(
            "sᴇʟᴇᴄᴛ ᴀ ᴄʜᴀɴɴᴇʟ ᴛᴏ ᴛᴏɢɢʟᴇ ɪᴛs ғᴏʀᴄᴇ-sᴜʙ ᴍᴏᴅᴇ:",
            reply_markup=InlineKeyboardMarkup(buttons)
        )

    # ============================================
    # AUTO DELETE CALLBACKS
    # ============================================

    elif data == "auto_del_toggle_mode":
        """Info about auto-delete mode"""
        if user_id != OWNER_ID:
            return await query.answer("⚠️ ᴏɴʟʏ ᴏᴡɴᴇʀ ᴄᴀɴ ᴄʜᴀɴɢᴇ sᴇᴛᴛɪɴɢs!", show_alert=True)
        
        await query.answer(
            "ℹ️ ᴀᴜᴛᴏ-ᴅᴇʟᴇᴛᴇ ɪs ᴀʟᴡᴀʏs ᴇɴᴀʙʟᴇᴅ.\n"
            "ʏᴏᴜ ᴄᴀɴ ᴀᴅᴊᴜsᴛ ᴛʜᴇ ᴛɪᴍᴇʀ ᴜsɪɴɢ sᴇᴛ ᴛɪᴍᴇʀ ʙᴜᴛᴛᴏɴ.",
            show_alert=True
        )
    
    elif data == "auto_del_set_timer":
        """Show timer selection menu"""
        if user_id != OWNER_ID:
            return await query.answer("⚠️ ᴏɴʟʏ ᴏᴡɴᴇʀ ᴄᴀɴ ᴄʜᴀɴɢᴇ sᴇᴛᴛɪɴɢs!", show_alert=True)
        
        current_timer = await db.get_del_timer()
        minutes = current_timer // 60
        
        keyboard = InlineKeyboardMarkup([
            [InlineKeyboardButton("⏱ 1 ᴍɪɴᴜᴛᴇ", callback_data="auto_del_set_60")],
            [InlineKeyboardButton("⏱ 5 ᴍɪɴᴜᴛᴇs", callback_data="auto_del_set_300")],
            [InlineKeyboardButton("⏱ 10 ᴍɪɴᴜᴛᴇs", callback_data="auto_del_set_600")],
            [InlineKeyboardButton("⏱ 30 ᴍɪɴᴜᴛᴇs", callback_data="auto_del_set_1800")],
            [InlineKeyboardButton("⏱ 1 ʜᴏᴜʀ", callback_data="auto_del_set_3600")],
            [InlineKeyboardButton("« ʙᴀᴄᴋ", callback_data="auto_del_back")]
        ])
        
        caption = f"""<b>⏱ sᴇᴛ ᴅᴇʟᴇᴛᴇ ᴛɪᴍᴇʀ</b>

<b>ᴄᴜʀʀᴇɴᴛ ᴛɪᴍᴇʀ:</b> <code>{minutes} ᴍɪɴᴜᴛᴇs</code>

<b>sᴇʟᴇᴄᴛ ᴀ ᴘʀᴇsᴇᴛ ᴛɪᴍᴇ:</b>"""
        
        try:
            await query.message.edit_caption(caption=caption, reply_markup=keyboard)
        except:
            await query.message.edit_text(text=caption, reply_markup=keyboard)
    
    elif data.startswith("auto_del_set_"):
        """Set specific timer value"""
        if user_id != OWNER_ID:
            return await query.answer("⚠️ ᴏɴʟʏ ᴏᴡɴᴇʀ ᴄᴀɴ ᴄʜᴀɴɢᴇ sᴇᴛᴛɪɴɢs!", show_alert=True)
        
        timer_seconds = int(data.split("_")[3])
        await db.set_del_timer(timer_seconds)
        
        minutes = timer_seconds // 60
        await query.answer(f"✅ ᴛɪᴍᴇʀ sᴇᴛ ᴛᴏ {minutes} ᴍɪɴᴜᴛᴇs!", show_alert=False)
        
        await asyncio.sleep(0.5)
        
        # Get fresh timer value
        current_timer = await db.get_del_timer()
        
        caption = f"""<b>🤖 𝗔𝗨𝗧𝗢 𝗗𝗘𝗟𝗘𝗧𝗘 𝗦𝗘𝗧𝗧𝗜𝗡𝗚𝗦</b>

<blockquote><b>🗑 ᴀᴜᴛᴏ ᴅᴇʟᴇᴛᴇ ᴍᴏᴅᴇ: ᴇɴᴀʙʟᴇᴅ ✅</b></blockquote>
<blockquote><b>⏱ ᴅᴇʟᴇᴛᴇ ᴛɪᴍᴇʀ: {get_exp_time(current_timer)}</b></blockquote>

<b>CLICK BELOW BUTTONS TO CHANGE SETTINGS</b>"""
        
        keyboard = InlineKeyboardMarkup([
            [InlineKeyboardButton(f"❌ ᴅᴇʟᴇᴛᴇ ᴍᴏᴅᴇ ❌", callback_data="auto_del_toggle_mode"),
             InlineKeyboardButton("◆ sᴇᴛ ᴛɪᴍᴇʀ ⏱", callback_data="auto_del_set_timer")],
            [
                InlineKeyboardButton(" ʀᴇғʀᴇsʜ", callback_data="auto_del_refresh"),
                InlineKeyboardButton("ᴄʟᴏsᴇ ✖️", callback_data="close")
            ]
        ])
        
        try:
            await query.message.edit_caption(caption=caption, reply_markup=keyboard)
        except:
            await query.message.edit_text(text=caption, reply_markup=keyboard)
    
    elif data == "auto_del_back":
        """Go back to auto_del main screen"""
        # Get fresh timer value
        delete_timer = await db.get_del_timer()
        
        caption = f"""<b>🤖 𝗔𝗨𝗧𝗢 𝗗𝗘𝗟𝗘𝗧𝗘 𝗦𝗘𝗧𝗧𝗜𝗡𝗚𝗦</b>

<blockquote><b>🗑 ᴀᴜᴛᴏ ᴅᴇʟᴇᴛᴇ ᴍᴏᴅᴇ: ᴇɴᴀʙʟᴇᴅ ✅</b></blockquote>
<blockquote><b>⏱ ᴅᴇʟᴇᴛᴇ ᴛɪᴍᴇʀ: {get_exp_time(delete_timer)}</b></blockquote>

<b>CLICK BELOW BUTTONS TO CHANGE SETTINGS</b>"""
        
        keyboard = InlineKeyboardMarkup([
            [InlineKeyboardButton(f"❌ ᴅᴇʟᴇᴛᴇ ᴍᴏᴅᴇ ❌", callback_data="auto_del_toggle_mode"),
             InlineKeyboardButton("◆ sᴇᴛ ᴛɪᴍᴇʀ ⏱", callback_data="auto_del_set_timer")],
            [
                InlineKeyboardButton(" ʀᴇғʀᴇsʜ", callback_data="auto_del_refresh"),
                InlineKeyboardButton("ᴄʟᴏsᴇ ✖️", callback_data="close")
            ]
        ])
        
        try:
            await query.message.edit_caption(caption=caption, reply_markup=keyboard)
        except:
            await query.message.edit_text(text=caption, reply_markup=keyboard)
        
        await query.answer("« Back", show_alert=False)
    
    elif data == "auto_del_refresh":
        """Refresh auto_del settings display"""
        # Get fresh timer value
        delete_timer = await db.get_del_timer()
        
        caption = f"""<b>🤖 𝗔𝗨𝗧𝗢 𝗗𝗘𝗟𝗘𝗧𝗘 𝗦𝗘𝗧𝗧𝗜𝗡𝗚𝗦</b>

<blockquote><b>🗑 ᴀᴜᴛᴏ ᴅᴇʟᴇᴛᴇ ᴍᴏᴅᴇ: ᴇɴᴀʙʟᴇᴅ ✅</b></blockquote>
<blockquote><b>⏱ ᴅᴇʟᴇᴛᴇ ᴛɪᴍᴇʀ: {get_exp_time(delete_timer)}</b></blockquote>

<b>CLICK BELOW BUTTONS TO CHANGE SETTINGS</b>"""
        
        keyboard = InlineKeyboardMarkup([
            [InlineKeyboardButton(f"❌ ᴅᴇʟᴇᴛᴇ ᴍᴏᴅᴇ ❌", callback_data="auto_del_toggle_mode"),
             InlineKeyboardButton("◆ sᴇᴛ ᴛɪᴍᴇʀ ⏱", callback_data="auto_del_set_timer")],
            [
                InlineKeyboardButton(" ʀᴇғʀᴇsʜ", callback_data="auto_del_refresh"),
                InlineKeyboardButton("ᴄʟᴏsᴇ ✖️", callback_data="close")
            ]
        ])
        
        try:
            await query.message.edit_caption(caption=caption, reply_markup=keyboard)
        except:
            await query.message.edit_text(text=caption, reply_markup=keyboard)
        
        await query.answer("✅ Refreshed!", show_alert=False)

    # ============================================
    # FILES CALLBACKS
    # ============================================

    elif data == "files_toggle_protect":
        """Toggle protect content"""
        if user_id != OWNER_ID:
            return await query.answer("⚠️ Only owner can change settings!", show_alert=True)
        
        current = await db.get_protect_content()
        new_value = not current
        await db.set_protect_content(new_value)
        
        status = "Enabled ✅" if new_value else "Disabled ❌"
        await query.answer(f"🔒 Protect Content: {status}", show_alert=False)
        
        await asyncio.sleep(0.3)
        
        # Get fresh settings
        protect_content = await db.get_protect_content()
        hide_caption = await db.get_hide_caption()
        channel_button = await db.get_channel_button()
        button_settings = await db.get_button_settings()
        
        button_name = button_settings.get('name', 'ᴍᴀɪɴ ᴄʜᴀɴɴᴇʟ ᴊᴏɪɴ')
        button_link = button_settings.get('link', f'https://t.me/{client.username}')
        
        protect_status_symbol = "✅" if protect_content else "❌"
        caption_status_symbol = "✅" if hide_caption else "❌"
        channel_btn_status_symbol = "✅" if channel_button else "❌"
        protect_status = "Eɴᴀʙʟᴇᴅ ✅" if protect_content else "Dɪsᴀʙʟᴇᴅ ❌"
        caption_status = "Eɴᴀʙʟᴇᴅ ✅" if hide_caption else "Dɪsᴀʙʟᴇᴅ ❌"
        btn_status = "Eɴᴀʙʟᴇᴅ ✅" if channel_button else "Dɪsᴀʙʟᴇᴅ ❌"
        
        files_caption = f'''<b>🤖 𝗙𝗜𝗟𝗘𝗦 𝗥𝗘𝗟𝗔𝗧𝗘𝗗 𝗦𝗘𝗧𝗧𝗜𝗡𝗚𝗦 ⚙️</b>

<blockquote expandable><b>🔒 ᴘʀᴏᴛᴇᴄᴛ ᴄᴏɴᴛᴇɴᴛ: {protect_status}</b>
<b>🫥 ʜɪᴅᴇ ᴄᴀᴘᴛɪᴏɴ: {caption_status}</b>
<b>🔘 ᴄʜᴀɴɴᴇʟ ʙᴜᴛᴛᴏɴ: {btn_status}</b>

<b>💎 ʙᴜᴛᴛᴏɴ Nᴀᴍᴇ:</b> <code>{button_name}</code>
<b>💎 ʙᴜᴛᴛᴏɴ Lɪɴᴋ:</b>
<code>{button_link}</code></blockquote>

<b>ᴄʟɪᴄᴋ ʙᴇʟᴏᴡ ʙᴜᴛᴛᴏɴs ᴛᴏ ᴄʜᴀɴɢᴇ sᴇᴛᴛɪɴɢs</b>'''
        
        keyboard = InlineKeyboardMarkup([
            [InlineKeyboardButton(f" ᴘʀᴏᴛᴇᴄᴛ ᴄᴏɴᴛᴇɴᴛ...{protect_status_symbol}", callback_data="files_toggle_protect"),
             InlineKeyboardButton(f" ʜɪᴅᴇ ᴄᴀᴘᴛɪᴏɴ:{caption_status_symbol} ", callback_data="files_toggle_caption")],
            [
                InlineKeyboardButton(f" ᴄʜᴀɴɴᴇʟ ʙᴜᴛᴛᴏɴ:{channel_btn_status_symbol} ", callback_data="files_toggle_channel_btn"),
                InlineKeyboardButton("◆ sᴇᴛ ʙᴜᴛᴛᴏɴ ⇨", callback_data="files_set_button")
            ],
            [
                InlineKeyboardButton(" ʀᴇғʀᴇsʜ", callback_data="files_refresh"),
                InlineKeyboardButton("ᴄʟᴏsᴇ ✖️", callback_data="close")
            ]
        ])
        
        try:
            await query.message.edit_caption(caption=files_caption, reply_markup=keyboard)
        except:
            await query.message.edit_text(text=files_caption, reply_markup=keyboard)
    
    elif data == "files_toggle_caption":
        """Toggle hide caption"""
        if user_id != OWNER_ID:
            return await query.answer("⚠️ Only owner can change settings!", show_alert=True)
        
        current = await db.get_hide_caption()
        new_value = not current
        await db.set_hide_caption(new_value)
        
        status = "Enabled ✅" if new_value else "Disabled ❌"
        await query.answer(f"📝 Hide Caption: {status}", show_alert=False)
        
        await asyncio.sleep(0.3)
        
        # Get fresh settings
        protect_content = await db.get_protect_content()
        hide_caption = await db.get_hide_caption()
        channel_button = await db.get_channel_button()
        button_settings = await db.get_button_settings()
        
        button_name = button_settings.get('name', 'ᴍᴀɪɴ ᴄʜᴀɴɴᴇʟ ᴊᴏɪɴ')
        button_link = button_settings.get('link', f'https://t.me/{client.username}')
        
        protect_status_symbol = "✅" if protect_content else "❌"
        caption_status_symbol = "✅" if hide_caption else "❌"
        channel_btn_status_symbol = "✅" if channel_button else "❌"
        protect_status = "Eɴᴀʙʟᴇᴅ ✅" if protect_content else "Dɪsᴀʙʟᴇᴅ ❌"
        caption_status = "Eɴᴀʙʟᴇᴅ ✅" if hide_caption else "Dɪsᴀʙʟᴇᴅ ❌"
        btn_status = "Eɴᴀʙʟᴇᴅ ✅" if channel_button else "Dɪsᴀʙʟᴇᴅ ❌"
        
        files_caption = f'''<b>🤖 𝗙𝗜𝗟𝗘𝗦 𝗥𝗘𝗟𝗔𝗧𝗘𝗗 𝗦𝗘𝗧𝗧𝗜𝗡𝗚𝗦 ⚙️</b>

<blockquote expandable><b>🔒 ᴘʀᴏᴛᴇᴄᴛ ᴄᴏɴᴛᴇɴᴛ: {protect_status}</b>
<b>🫥 ʜɪᴅᴇ ᴄᴀᴘᴛɪᴏɴ: {caption_status}</b>
<b>🔘 ᴄʜᴀɴɴᴇʟ ʙᴜᴛᴛᴏɴ: {btn_status}</b>

<b>💎 ʙᴜᴛᴛᴏɴ Nᴀᴍᴇ:</b> <code>{button_name}</code>
<b>💎 ʙᴜᴛᴛᴏɴ Lɪɴᴋ:</b>
<code>{button_link}</code></blockquote>

<b>ᴄʟɪᴄᴋ ʙᴇʟᴏᴡ ʙᴜᴛᴛᴏɴs ᴛᴏ ᴄʜᴀɴɢᴇ sᴇᴛᴛɪɴɢs</b>'''
        
        keyboard = InlineKeyboardMarkup([
            [InlineKeyboardButton(f" ᴘʀᴏᴛᴇᴄᴛ ᴄᴏɴᴛᴇɴᴛ...{protect_status_symbol}", callback_data="files_toggle_protect"),
             InlineKeyboardButton(f" ʜɪᴅᴇ ᴄᴀᴘᴛɪᴏɴ:{caption_status_symbol} ", callback_data="files_toggle_caption")],
            [
                InlineKeyboardButton(f" ᴄʜᴀɴɴᴇʟ ʙᴜᴛᴛᴏɴ:{channel_btn_status_symbol} ", callback_data="files_toggle_channel_btn"),
                InlineKeyboardButton("◆ sᴇᴛ ʙᴜᴛᴛᴏɴ ⇨", callback_data="files_set_button")
            ],
            [
                InlineKeyboardButton(" ʀᴇғʀᴇsʜ", callback_data="files_refresh"),
                InlineKeyboardButton("ᴄʟᴏsᴇ ✖️", callback_data="close")
            ]
        ])
        
        try:
            await query.message.edit_caption(caption=files_caption, reply_markup=keyboard)
        except:
            await query.message.edit_text(text=files_caption, reply_markup=keyboard)
    
    elif data == "files_toggle_channel_btn":
        """Toggle channel button"""
        if user_id != OWNER_ID:
            return await query.answer("⚠️ Only owner can change settings!", show_alert=True)
        
        current = await db.get_channel_button()
        new_value = not current
        await db.set_channel_button(new_value)
        
        status = "Enabled ✅" if new_value else "Disabled ❌"
        await query.answer(f"⚪ Channel Button: {status}", show_alert=False)
        
        await asyncio.sleep(0.3)
        
        # Get fresh settings
        protect_content = await db.get_protect_content()
        hide_caption = await db.get_hide_caption()
        channel_button = await db.get_channel_button()
        button_settings = await db.get_button_settings()
        
        button_name = button_settings.get('name', 'ᴍᴀɪɴ ᴄʜᴀɴɴᴇʟ ᴊᴏɪɴ')
        button_link = button_settings.get('link', f'https://t.me/{client.username}')
        
        protect_status_symbol = "✅" if protect_content else "❌"
        caption_status_symbol = "✅" if hide_caption else "❌"
        channel_btn_status_symbol = "✅" if channel_button else "❌"
        protect_status = "Eɴᴀʙʟᴇᴅ ✅" if protect_content else "Dɪsᴀʙʟᴇᴅ ❌"
        caption_status = "Eɴᴀʙʟᴇᴅ ✅" if hide_caption else "Dɪsᴀʙʟᴇᴅ ❌"
        btn_status = "Eɴᴀʙʟᴇᴅ ✅" if channel_button else "Dɪsᴀʙʟᴇᴅ ❌"
        
        files_caption = f'''<b>🤖 𝗙𝗜𝗟𝗘𝗦 𝗥𝗘𝗟𝗔𝗧𝗘𝗗 𝗦𝗘𝗧𝗧𝗜𝗡𝗚𝗦 ⚙️</b>

<blockquote expandable><b>🔒 ᴘʀᴏᴛᴇᴄᴛ ᴄᴏɴᴛᴇɴᴛ: {protect_status}</b>
<b>🫥 ʜɪᴅᴇ ᴄᴀᴘᴛɪᴏɴ: {caption_status}</b>
<b>🔘 ᴄʜᴀɴɴᴇʟ ʙᴜᴛᴛᴏɴ: {btn_status}</b>

<b>💎 ʙᴜᴛᴛᴏɴ Nᴀᴍᴇ:</b> <code>{button_name}</code>
<b>💎 ʙᴜᴛᴛᴏɴ Lɪɴᴋ:</b>
<code>{button_link}</code></blockquote>

<b>ᴄʟɪᴄᴋ ʙᴇʟᴏᴡ ʙᴜᴛᴛᴏɴs ᴛᴏ ᴄʜᴀɴɢᴇ sᴇᴛᴛɪɴɢs</b>'''
        
        keyboard = InlineKeyboardMarkup([
            [InlineKeyboardButton(f" ᴘʀᴏᴛᴇᴄᴛ ᴄᴏɴᴛᴇɴᴛ...{protect_status_symbol}", callback_data="files_toggle_protect"),
             InlineKeyboardButton(f" ʜɪᴅᴇ ᴄᴀᴘᴛɪᴏɴ:{caption_status_symbol} ", callback_data="files_toggle_caption")],
            [
                InlineKeyboardButton(f" ᴄʜᴀɴɴᴇʟ ʙᴜᴛᴛᴏɴ:{channel_btn_status_symbol} ", callback_data="files_toggle_channel_btn"),
                InlineKeyboardButton("◆ sᴇᴛ ʙᴜᴛᴛᴏɴ ⇨", callback_data="files_set_button")
            ],
            [
                InlineKeyboardButton(" ʀᴇғʀᴇsʜ", callback_data="files_refresh"),
                InlineKeyboardButton("ᴄʟᴏsᴇ ✖️", callback_data="close")
            ]
        ])
        
        try:
            await query.message.edit_caption(caption=files_caption, reply_markup=keyboard)
        except:
            await query.message.edit_text(text=files_caption, reply_markup=keyboard)
    
    elif data == "files_set_button":
        """Show button editor menu"""
        if user_id != OWNER_ID:
            return await query.answer("⚠️ Only owner can change settings!", show_alert=True)
        
        button_settings = await db.get_button_settings()
        button_name = button_settings.get('name', 'Main Channel Join')
        button_link = button_settings.get('link', f'https://t.me/{client.username}')
        
        keyboard = InlineKeyboardMarkup([
            [InlineKeyboardButton("✏️ Edit Button Name", callback_data="files_edit_name"),
             InlineKeyboardButton("🔗 Edit Button Link", callback_data="files_edit_link")],
            [InlineKeyboardButton("🔄 Reset to Default", callback_data="files_reset_btn"),
             InlineKeyboardButton("« Back", callback_data="files_back")]
        ])
        
        caption = f"""<b>⚙️ BUTTON EDITOR</b>

<b>Current Button Settings:</b>
<b>├ Name:</b> <code>{button_name}</code>
<b>└ Link:</b> <code>{button_link}</code>

<b>Select an option below:</b>"""
        
        try:
            await query.message.edit_caption(caption=caption, reply_markup=keyboard)
        except:
            await query.message.edit_text(text=caption, reply_markup=keyboard)
    
    elif data == "files_edit_name":
        """Info on how to edit button name"""
        await query.answer(
            "ℹ️ To edit button name:\n"
            "Use: /set_button_name <text>\n"
            "Example: /set_button_name Join Our Channel",
            show_alert=True
        )
    
    elif data == "files_edit_link":
        """Info on how to edit button link"""
        await query.answer(
            "ℹ️ To edit button link:\n"
            "Use: /set_button_link <url>\n"
            "Example: /set_button_link https://t.me/YourChannel",
            show_alert=True
        )
    
    elif data == "files_reset_btn":
        """Reset button to default"""
        if user_id != OWNER_ID:
            return await query.answer("⚠️ Only owner can change settings!", show_alert=True)
        
        await db.set_button_settings(
            name="Main Channel Join",
            link=f"https://t.me/{client.username}"
        )
        
        await query.answer("✅ Button reset to default!", show_alert=False)
        
        await asyncio.sleep(0.5)
        
        # Get fresh settings and refresh display
        protect_content = await db.get_protect_content()
        hide_caption = await db.get_hide_caption()
        channel_button = await db.get_channel_button()
        button_settings = await db.get_button_settings()
        
        button_name = button_settings.get('name', 'ᴍᴀɪɴ ᴄʜᴀɴɴᴇʟ ᴊᴏɪɴ')
        button_link = button_settings.get('link', f'https://t.me/{client.username}')
        
        protect_status_symbol = "✅" if protect_content else "❌"
        caption_status_symbol = "✅" if hide_caption else "❌"
        channel_btn_status_symbol = "✅" if channel_button else "❌"
        protect_status = "Eɴᴀʙʟᴇᴅ ✅" if protect_content else "Dɪsᴀʙʟᴇᴅ ❌"
        caption_status = "Eɴᴀʙʟᴇᴅ ✅" if hide_caption else "Dɪsᴀʙʟᴇᴅ ❌"
        btn_status = "Eɴᴀʙʟᴇᴅ ✅" if channel_button else "Dɪsᴀʙʟᴇᴅ ❌"
        
        files_caption = f'''<b>🤖 𝗙𝗜𝗟𝗘𝗦 𝗥𝗘𝗟𝗔𝗧𝗘𝗗 𝗦𝗘𝗧𝗧𝗜𝗡𝗚𝗦 ⚙️</b>

<blockquote expandable><b>🔒 ᴘʀᴏᴛᴇᴄᴛ ᴄᴏɴᴛᴇɴᴛ: {protect_status}</b>
<b>🫥 ʜɪᴅᴇ ᴄᴀᴘᴛɪᴏɴ: {caption_status}</b>
<b>🔘 ᴄʜᴀɴɴᴇʟ ʙᴜᴛᴛᴏɴ: {btn_status}</b>

<b>💎 ʙᴜᴛᴛᴏɴ Nᴀᴍᴇ:</b> <code>{button_name}</code>
<b>💎 ʙᴜᴛᴛᴏɴ Lɪɴᴋ:</b>
<code>{button_link}</code></blockquote>

<b>ᴄʟɪᴄᴋ ʙᴇʟᴏᴡ ʙᴜᴛᴛᴏɴs ᴛᴏ ᴄʜᴀɴɢᴇ sᴇᴛᴛɪɴɢs</b>'''
        
        keyboard = InlineKeyboardMarkup([
            [InlineKeyboardButton(f" ᴘʀᴏᴛᴇᴄᴛ ᴄᴏɴᴛᴇɴᴛ...{protect_status_symbol}", callback_data="files_toggle_protect"),
             InlineKeyboardButton(f" ʜɪᴅᴇ ᴄᴀᴘᴛɪᴏɴ:{caption_status_symbol} ", callback_data="files_toggle_caption")],
            [
                InlineKeyboardButton(f" ᴄʜᴀɴɴᴇʟ ʙᴜᴛᴛᴏɴ:{channel_btn_status_symbol} ", callback_data="files_toggle_channel_btn"),
                InlineKeyboardButton("◆ sᴇᴛ ʙᴜᴛᴛᴏɴ ⇨", callback_data="files_set_button")
            ],
            [
                InlineKeyboardButton(" ʀᴇғʀᴇsʜ", callback_data="files_refresh"),
                InlineKeyboardButton("ᴄʟᴏsᴇ ✖️", callback_data="close")
            ]
        ])
        
        try:
            await query.message.edit_caption(caption=files_caption, reply_markup=keyboard)
        except:
            await query.message.edit_text(text=files_caption, reply_markup=keyboard)
    
    elif data == "files_back":
        """Go back to files main screen"""
        # Get fresh settings
        protect_content = await db.get_protect_content()
        hide_caption = await db.get_hide_caption()
        channel_button = await db.get_channel_button()
        button_settings = await db.get_button_settings()
        
        button_name = button_settings.get('name', 'ᴍᴀɪɴ ᴄʜᴀɴɴᴇʟ ᴊᴏɪɴ')
        button_link = button_settings.get('link', f'https://t.me/{client.username}')
        
        protect_status_symbol = "✅" if protect_content else "❌"
        caption_status_symbol = "✅" if hide_caption else "❌"
        channel_btn_status_symbol = "✅" if channel_button else "❌"
        protect_status = "Eɴᴀʙʟᴇᴅ ✅" if protect_content else "Dɪsᴀʙʟᴇᴅ ❌"
        caption_status = "Eɴᴀʙʟᴇᴅ ✅" if hide_caption else "Dɪsᴀʙʟᴇᴅ ❌"
        btn_status = "Eɴᴀʙʟᴇᴅ ✅" if channel_button else "Dɪsᴀʙʟᴇᴅ ❌"
        
        files_caption = f'''<b>🤖 𝗙𝗜𝗟𝗘𝗦 𝗥𝗘𝗟𝗔𝗧𝗘𝗗 𝗦𝗘𝗧𝗧𝗜𝗡𝗚𝗦 ⚙️</b>

<blockquote expandable><b>🔒 ᴘʀᴏᴛᴇᴄᴛ ᴄᴏɴᴛᴇɴᴛ: {protect_status}</b>
<b>🫥 ʜɪᴅᴇ ᴄᴀᴘᴛɪᴏɴ: {caption_status}</b>
<b>🔘 ᴄʜᴀɴɴᴇʟ ʙᴜᴛᴛᴏɴ: {btn_status}</b>

<b>💎 ʙᴜᴛᴛᴏɴ Nᴀᴍᴇ:</b> <code>{button_name}</code>
<b>💎 ʙᴜᴛᴛᴏɴ Lɪɴᴋ:</b>
<code>{button_link}</code></blockquote>

<b>ᴄʟɪᴄᴋ ʙᴇʟᴏᴡ ʙᴜᴛᴛᴏɴs ᴛᴏ ᴄʜᴀɴɢᴇ sᴇᴛᴛɪɴɢs</b>'''
        
        keyboard = InlineKeyboardMarkup([
            [InlineKeyboardButton(f" ᴘʀᴏᴛᴇᴄᴛ ᴄᴏɴᴛᴇɴᴛ...{protect_status_symbol}", callback_data="files_toggle_protect"),
             InlineKeyboardButton(f" ʜɪᴅᴇ ᴄᴀᴘᴛɪᴏɴ:{caption_status_symbol} ", callback_data="files_toggle_caption")],
            [
                InlineKeyboardButton(f" ᴄʜᴀɴɴᴇʟ ʙᴜᴛᴛᴏɴ:{channel_btn_status_symbol} ", callback_data="files_toggle_channel_btn"),
                InlineKeyboardButton("◆ sᴇᴛ ʙᴜᴛᴛᴏɴ ⇨", callback_data="files_set_button")
            ],
            [
                InlineKeyboardButton(" ʀᴇғʀᴇsʜ", callback_data="files_refresh"),
                InlineKeyboardButton("ᴄʟᴏsᴇ ✖️", callback_data="close")
            ]
        ])
        
        try:
            await query.message.edit_caption(caption=files_caption, reply_markup=keyboard)
        except:
            await query.message.edit_text(text=files_caption, reply_markup=keyboard)
        
        await query.answer("« Back", show_alert=False)
    
    elif data == "files_refresh":
        """Refresh files settings display"""
        # Get fresh settings
        protect_content = await db.get_protect_content()
        hide_caption = await db.get_hide_caption()
        channel_button = await db.get_channel_button()
        button_settings = await db.get_button_settings()
        
        button_name = button_settings.get('name', 'ᴍᴀɪɴ ᴄʜᴀɴɴᴇʟ ᴊᴏɪɴ')
        button_link = button_settings.get('link', f'https://t.me/{client.username}')
        
        protect_status_symbol = "✅" if protect_content else "❌"
        caption_status_symbol = "✅" if hide_caption else "❌"
        channel_btn_status_symbol = "✅" if channel_button else "❌"
        protect_status = "Eɴᴀʙʟᴇᴅ ✅" if protect_content else "Dɪsᴀʙʟᴇᴅ ❌"
        caption_status = "Eɴᴀʙʟᴇᴅ ✅" if hide_caption else "Dɪsᴀʙʟᴇᴅ ❌"
        btn_status = "Eɴᴀʙʟᴇᴅ ✅" if channel_button else "Dɪsᴀʙʟᴇᴅ ❌"
        
        files_caption = f'''<b>🤖 𝗙𝗜𝗟𝗘𝗦 𝗥𝗘𝗟𝗔𝗧𝗘𝗗 𝗦𝗘𝗧𝗧𝗜𝗡𝗚𝗦 ⚙️</b>

<blockquote expandable><b>🔒 ᴘʀᴏᴛᴇᴄᴛ ᴄᴏɴᴛᴇɴᴛ: {protect_status}</b>
<b>🫥 ʜɪᴅᴇ ᴄᴀᴘᴛɪᴏɴ: {caption_status}</b>
<b>🔘 ᴄʜᴀɴɴᴇʟ ʙᴜᴛᴛᴏɴ: {btn_status}</b>

<b>💎 ʙᴜᴛᴛᴏɴ Nᴀᴍᴇ:</b> <code>{button_name}</code>
<b>💎 ʙᴜᴛᴛᴏɴ Lɪɴᴋ:</b>
<code>{button_link}</code></blockquote>

<b>ᴄʟɪᴄᴋ ʙᴇʟᴏᴡ ʙᴜᴛᴛᴏɴs ᴛᴏ ᴄʜᴀɴɢᴇ sᴇᴛᴛɪɴɢs</b>'''
        
        keyboard = InlineKeyboardMarkup([
            [InlineKeyboardButton(f" ᴘʀᴏᴛᴇᴄᴛ ᴄᴏɴᴛᴇɴᴛ...{protect_status_symbol}", callback_data="files_toggle_protect"),
             InlineKeyboardButton(f" ʜɪᴅᴇ ᴄᴀᴘᴛɪᴏɴ:{caption_status_symbol} ", callback_data="files_toggle_caption")],
            [
                InlineKeyboardButton(f" ᴄʜᴀɴɴᴇʟ ʙᴜᴛᴛᴏɴ:{channel_btn_status_symbol} ", callback_data="files_toggle_channel_btn"),
                InlineKeyboardButton("◆ sᴇᴛ ʙᴜᴛᴛᴏɴ ⇨", callback_data="files_set_button")
            ],
            [
                InlineKeyboardButton(" ʀᴇғʀᴇsʜ", callback_data="files_refresh"),
                InlineKeyboardButton("ᴄʟᴏsᴇ ✖️", callback_data="close")
            ]
        ])
        
        try:
            await query.message.edit_caption(caption=files_caption, reply_markup=keyboard)
        except:
            await query.message.edit_text(text=files_caption, reply_markup=keyboard)
        
        await query.answer("✅ Refreshed!", show_alert=False)

    # ============================================
    # STATS CALLBACKS
    # ============================================
    
    elif data.startswith("stats_"):
        await handle_stats_callback(client, query)

    # ============================================
    # FEATURES CALLBACKS - PASS TO features_command.py
    # ============================================
    
    elif data.startswith("feat_"):
        print(f"[CBB] 📥 Features callback passed to features_command.py: {data}")
        # Don't return, let it be handled by features_command.py
        return


async def handle_stats_callback(client: Bot, query: CallbackQuery):
    """Handle all stats-related callbacks"""
    data = query.data
    
    if data == "stats_bot":
        now = datetime.now(timezone.utc)
        delta = now - client.uptime
        total_seconds = int(delta.total_seconds())
        uptime_str = get_readable_time(total_seconds)
        
        users = await db.full_userbase()
        total_users = len(users)
        
        stats = get_system_stats()
        
        text = f"""<b>◇ ʙᴏᴛ sᴛᴀᴛɪsᴛɪᴄs :</b>

<b>├ ʙᴏᴛ ᴜᴘᴛɪᴍᴇ :</b> <code>{uptime_str}</code>

<b>┌ ʀᴀᴍ ( ᴍᴇᴍᴏʀʏ ) :</b>
<b>│</b> {get_progress_bar(stats['memory'].percent)}
<b>└ ᴜ :</b> <code>{format_bytes(stats['memory'].used)}</code> <b>| ғ :</b> <code>{format_bytes(stats['memory'].available)}</code> <b>| ᴛ :</b> <code>{format_bytes(stats['memory'].total)}</code>

<b>┌ sᴡᴀᴘ ᴍᴇᴍᴏʀʏ :</b>
<b>│</b> {get_progress_bar(stats['swap'].percent)}
<b>└ ᴜ :</b> <code>{format_bytes(stats['swap'].used)}</code> <b>| ғ :</b> <code>{format_bytes(stats['swap'].free)}</code> <b>| ᴛ :</b> <code>{format_bytes(stats['swap'].total)}</code>

<b>┌ ᴅɪsᴋ :</b>
<b>│</b> {get_progress_bar(stats['disk'].percent)}
<b>│ ᴛᴏᴛᴀʟ ᴅɪsᴋ ʀᴇᴀᴅ :</b> <code>{format_bytes(stats['disk_io'].read_bytes) if stats['disk_io'] else 'N/A'}</code>
<b>│ ᴛᴏᴛᴀʟ ᴅɪsᴋ ᴡʀɪᴛᴇ :</b> <code>{format_bytes(stats['disk_io'].write_bytes) if stats['disk_io'] else 'N/A'}</code>
<b>└ ᴜ :</b> <code>{format_bytes(stats['disk'].used)}</code> <b>| ғ :</b> <code>{format_bytes(stats['disk'].free)}</code> <b>| ᴛ :</b> <code>{format_bytes(stats['disk'].total)}</code>
"""
        
        buttons = InlineKeyboardMarkup([
            [InlineKeyboardButton("ʙᴀᴄᴋ", callback_data="stats_back"),
             InlineKeyboardButton("ᴄʟᴏsᴇ", callback_data="close")]
        ])
        
        await query.message.edit_text(text, reply_markup=buttons)
    
    elif data == "stats_os":
        stats = get_system_stats()
        
        os_uptime_str = get_readable_time(int(stats['os_uptime'].total_seconds()))
        
        try:
            load_avg = os.getloadavg()
            load_str = f"<code>{load_avg[0]:.2f}%, {load_avg[1]:.2f}%, {load_avg[2]:.2f}%</code>"
        except:
            load_str = "<code>N/A</code>"
        
        text = f"""<b>◇ ᴏs sʏsᴛᴇᴍ :</b>

<b>├ ᴏs ᴜᴘᴛɪᴍᴇ :</b> <code>{os_uptime_str}</code>
<b>├ ᴏs ᴠᴇʀsɪᴏɴ :</b> <code>{stats['os_version'][:50]}</code>
<b>└ ᴏs ᴀʀᴄʜ :</b> <code>{stats['os_arch']}</code>

<b>◇ ɴᴇᴛᴡᴏʀᴋ sᴛᴀᴛs :</b>

<b>├ ᴜᴘʟᴏᴀᴅ ᴅᴀᴛᴀ :</b> <code>{format_bytes(stats['net_io'].bytes_sent)}</code>
<b>├ ᴅᴏᴡɴʟᴏᴀᴅ ᴅᴀᴛᴀ :</b> <code>{format_bytes(stats['net_io'].bytes_recv)}</code>
<b>├ ᴘᴋᴛs sᴇɴᴛ :</b> <code>{stats['net_io'].packets_sent}</code>
<b>├ ᴘᴋᴛs ʀᴇᴄᴇɪᴠᴇᴅ :</b> <code>{stats['net_io'].packets_recv}</code>
<b>└ ᴛᴏᴛᴀʟ ɪ/ᴏ ᴅᴀᴛᴀ :</b> <code>{format_bytes(stats['net_io'].bytes_sent + stats['net_io'].bytes_recv)}</code>

<b>┌ ᴄᴘᴜ :</b>
<b>│</b> {get_progress_bar(stats['cpu_percent'])}
<b>├ ᴄᴘᴜ ғʀᴇǫᴜᴇɴᴄʏ :</b> <code>{stats['cpu_freq']:.2f} MHz</code>
<b>├ sʏsᴛᴇᴍ ᴀᴠɢ ʟᴏᴀᴅ :</b> {load_str} (1m, 5m, 15m)
<b>├ ᴘ-ᴄᴏʀᴇ(s) :</b> <code>{stats['cpu_physical']}</code> <b>| ᴠ-ᴄᴏʀᴇ(s) :</b> <code>{stats['cpu_logical']}</code>
<b>├ ᴛᴏᴛᴀʟ ᴄᴏʀᴇ(s) :</b> <code>{stats['cpu_logical']}</code>
<b>└ ᴜsᴀʙʟᴇ ᴄᴘᴜ(s) :</b> <code>{stats['cpu_logical']}</code>
"""
        
        buttons = InlineKeyboardMarkup([
            [InlineKeyboardButton("ʙᴀᴄᴋ", callback_data="stats_back"),
             InlineKeyboardButton("ᴄʟᴏsᴇ", callback_data="close")]
        ])
        
        await query.message.edit_text(text, reply_markup=buttons)
    
    elif data == "stats_db":
        try:
            total_users = len(await db.full_userbase())
            banned_users = len(await db.get_ban_users())
            total_admins = len(await db.get_all_admins())
            force_sub_channels = len(await db.show_channels())
            
            user_storage = total_users * 0.5
            admin_storage = total_admins * 0.5
            channel_storage = force_sub_channels * 1
            
            delete_timer = await db.get_del_timer()
            delete_style = await db.get_delete_style()
            auto_link = await db.get_auto_link_status()
            link_preview = await db.get_link_preview()
            
            total_collections = 9
            estimated_storage = user_storage + admin_storage + channel_storage
            
            free_tier_limit = 512
            storage_mb = estimated_storage / 1024
            storage_percent = (storage_mb / free_tier_limit) * 100
            
            text = f"""<b>◇ DATABASE STATS :</b>

<b>├ Database Type :</b> <code>MongoDB</code>
<b>├ Tier :</b> <code>Free (M0)</code>
<b>├ Storage Limit :</b> <code>{free_tier_limit}MB</code>

<b>┌ STORAGE USAGE :</b>
<b>│</b> {get_progress_bar(min(storage_percent, 100))}
<b>└ Used :</b> <code>{storage_mb:.2f}MB</code> <b>/ Free :</b> <code>{free_tier_limit - storage_mb:.2f}MB</code>

<b>◇ COLLECTIONS DATA :</b>

<b>├ Total Collections :</b> <code>{total_collections}</code>
<b>│</b>
<b>├ 👥 Users Collection :</b>
<b>│  ├ Total Users :</b> <code>{total_users}</code>
<b>│  └ Storage :</b> <code>~{user_storage:.2f}KB</code>
<b>│</b>
<b>├ 👨‍💼 Admins Collection :</b>
<b>│  ├ Total Admins :</b> <code>{total_admins}</code>
<b>│  └ Storage :</b> <code>~{admin_storage:.2f}KB</code>
<b>│</b>
<b>├ 🚫 Banned Users Collection :</b>
<b>│  ├ Banned Users :</b> <code>{banned_users}</code>
<b>│  └ Storage :</b> <code>~{banned_users * 0.5:.2f}KB</code>
<b>│</b>
<b>├ 📺 Channels Collection :</b>
<b>│  ├ Total Channels :</b> <code>{force_sub_channels}</code>
<b>│  └ Storage :</b> <code>~{channel_storage:.2f}KB</code>
<b>│</b>
<b>└ 🔧 Settings Collections :</b>
<b>   ├ Delete Timer :</b> <code>{delete_timer}s</code>
<b>   ├ Delete Style :</b> <code>{delete_style}</code>
<b>   ├ Auto Link :</b> <code>{'ON ✅' if auto_link else 'OFF ❌'}</code>
<b>   └ Link Preview :</b> <code>{'ON ✅' if link_preview else 'OFF ❌'}</code>

<b>◇ FREE TIER LIMITS :</b>

<b>├ Max Storage :</b> <code>512MB</code>
<b>├ Max Connections :</b> <code>500</code>
<b>├ Shared RAM :</b> <code>Shared</code>
<b>└ Bandwidth :</b> <code>Unlimited</code>

<i>💡 Estimated storage based on collection sizes</i>
"""
            
            buttons = InlineKeyboardMarkup([
                [InlineKeyboardButton("Back", callback_data="stats_back"),
                 InlineKeyboardButton("Close", callback_data="close")]
            ])
            
            await query.message.edit_text(text, reply_markup=buttons)
        
        except Exception as e:
            text = f"<b>◇ DATABASE STATS :</b>\n\n<code>Error: {e}</code>"
            buttons = InlineKeyboardMarkup([
                [InlineKeyboardButton("Back", callback_data="stats_back"),
                 InlineKeyboardButton("Close", callback_data="close")]
            ])
            await query.message.edit_text(text, reply_markup=buttons)
    
    elif data == "stats_repo":
        try:
            total_size = 0
            for dirpath, dirnames, filenames in os.walk('.'):
                for filename in filenames:
                    filepath = os.path.join(dirpath, filename)
                    if os.path.exists(filepath):
                        total_size += os.path.getsize(filepath)
            
            file_count = sum([len(files) for r, d, files in os.walk('.')])
            
            import platform
            text = f"""<b>◇ REPO STATS :</b>

<b>├ Repo Size :</b> <code>{format_bytes(total_size)}</code>
<b>├ Total Files :</b> <code>{file_count}</code>
<b>├ Python Version :</b> <code>{platform.python_version()}</code>
<b>└ Pyrogram Version :</b> <code>2.x</code>

<b>◇ PROJECT INFO :</b>

<b>├ Bot Name :</b> <code>File Store Bot</code>
<b>├ Developer :</b> @BeatAnime
<b>├ Support :</b> @Beat_Anime_Discussion
<b>└ Version :</b> <code>5.0</code>
"""
        except Exception as e:
            text = f"<b>◇ REPO STATS :</b>\n\n<code>Error: {e}</code>"
        
        buttons = InlineKeyboardMarkup([
            [InlineKeyboardButton("Back", callback_data="stats_back"),
             InlineKeyboardButton("Close", callback_data="close")]
        ])
        
        await query.message.edit_text(text, reply_markup=buttons)
    
    elif data == "stats_limits":
        text = f"""<b>◇ BOT LIMITS :</b>

<b>├ Max File Size :</b> <code>2GB</code>
<b>├ Max Batch Size :</b> <code>200 files</code>
<b>├ Auto-Delete Timer :</b> <code>{await db.get_del_timer()}s</code>
<b>├ Delete Style :</b> <code>{await db.get_delete_style()}</code>
<b>├ Auto Link :</b> <code>{'ON ✅' if await db.get_auto_link_status() else 'OFF ❌'}</code>
<b>└ Link Preview :</b> <code>{'ON ✅' if await db.get_link_preview() else 'OFF ❌'}</code>

<b>◇ DATABASE INFO :</b>

<b>├ Total Users :</b> <code>{len(await db.full_userbase())}</code>
<b>├ Banned Users :</b> <code>{len(await db.get_ban_users())}</code>
<b>├ Total Admins :</b> <code>{len(await db.get_all_admins())}</code>
<b>├ Force Sub Channels :</b> <code>{len(await db.show_channels())}</code>
<b>└ Database :</b> <code>MongoDB</code>
"""
        
        buttons = InlineKeyboardMarkup([
            [InlineKeyboardButton("Back", callback_data="stats_back"),
             InlineKeyboardButton("Close", callback_data="close")]
        ])
        
        await query.message.edit_text(text, reply_markup=buttons)
    
    elif data == "stats_render":
        """Show Render usage - imported from stats_system.py"""
        try:
            from plugins.stats_system import show_render_usage
            await show_render_usage(client, query)
        except Exception as e:
            await query.answer(f"Error: {e}", show_alert=True)
    
    elif data == "stats_back":
        now = datetime.now(timezone.utc)
        delta = now - client.uptime
        total_seconds = int(delta.total_seconds())
        uptime_str = get_readable_time(total_seconds)
        
        users = await db.full_userbase()
        total_users = len(users)
        
        stats_text = f"""<b>🤖 𝗕𝗢𝗧 𝗦𝗧𝗔𝗧𝗜𝗦𝗧𝗜𝗖𝗦 :</b>

<b>├ ʙᴏᴛ ᴜᴘᴛɪᴍᴇ :</b> <code>{uptime_str}</code>
<b>├ ᴛᴏᴛᴀʟ ᴜsᴇʀs :</b> <code>{total_users}</code>
<b>└ sᴛᴀᴛᴜs :</b> <code>ᴀᴄᴛɪᴠᴇ ✅</code>

<i>💡 Click buttons below for detailed stats</i>
"""
        
        buttons = InlineKeyboardMarkup([
            [
                InlineKeyboardButton("ʙᴏᴛ sᴛᴀᴛs", callback_data="stats_bot"),
                InlineKeyboardButton("ᴏs sᴛᴀᴛs", callback_data="stats_os")
            ],
            [
                InlineKeyboardButton("ʀᴇᴘᴏ sᴛᴀᴛs", callback_data="stats_repo"),
                InlineKeyboardButton("ᴅʙ sᴛᴀᴛs", callback_data="stats_db")
            ],
            [
                InlineKeyboardButton(" ʀᴇɴᴅᴇʀ ᴜsᴀɢᴇ", callback_data="stats_render")
            ],
            [
                InlineKeyboardButton("ʙᴏᴛ ʟɪᴍɪᴛs", callback_data="stats_limits")
            ],
            [InlineKeyboardButton("ᴄʟᴏsᴇ", callback_data="close")]
        ])
        
        await query.message.edit_text(stats_text, reply_markup=buttons)


print("[CBB] ✅ COMPLETE Comprehensive callback handler loaded!")

