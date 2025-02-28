import logging
import os
import platform
import psutil
import time

from pyrogram import Client, filters
from pyrogram.types import CallbackQuery, InlineKeyboardButton, InlineKeyboardMarkup, Message

from config import BOT_USERNAME, OWNER_ID
from PROTECTOR import PROTECTOR as app

# Constants
FORBIDDEN_KEYWORDS = ["porn", "xxx", "NCERT", "ncert", "ans", "Pre-Medical", "kinematics", "Experiments", "Experiment", "experiment", "experimens", "XII", "page", "Ans", "meiotic", "divisions", "S[...]"]

START_TEXT = """<b> 🤖 ᴄᴏᴘʏʀɪɢʜᴛ ᴘʀᴏᴛᴇᴄᴛᴏʀ 🛡️ </b>

ʜᴇʏ ᴛʜɪs ɪs ᴄᴏᴘʏʀɪɢʜᴛ ᴘʀᴏᴛᴇᴄᴛᴏʀ ʀᴏʙᴏᴛ🤖!\n ᴡᴇ ᴇɴsᴜʀᴇ ʏᴏᴜʀ ɢʀᴏᴜᴘ sᴇᴄᴜʀɪᴛʏ💻 !\n ᴛʜɪs ʙᴏᴛ ᴄᴀɴ ʀ�[...]"""

# Define the start time
start_time = time.time()

# Functions for formatting time and size
def time_formatter(milliseconds: float) -> str:
    seconds, milliseconds = divmod(milliseconds, 1000)
    minutes, seconds = divmod(seconds, 60)
    hours, minutes = divmod(minutes, 60)
    return f"{int(hours)}h {int(minutes)}m {int(seconds)}s"

def size_formatter(bytes: int) -> str:
    for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
        if bytes < 1024.0:
            break
        bytes /= 1024.0
    return f"{bytes:.2f} {unit}"

# Command Handlers
@app.on_message(filters.command("start"))
async def start_command_handler(_, msg):
    buttons = [
        [InlineKeyboardButton("ᴀᴅᴅ ᴍᴇ", url=f"https://t.me/{BOT_USERNAME}?startgroup=true")],
        [InlineKeyboardButton("• ʜᴀɴᴅʟᴇʀ •", callback_data="vip_back")]
    ]
    reply_markup = InlineKeyboardMarkup(buttons)
    await msg.reply_photo(
        photo="https://telegra.ph/file/fa1489797406a1be5a486.jpg",
        caption=START_TEXT,
        reply_markup=reply_markup
    )

# Callback Query Handlers
gd_buttons = [
    [InlineKeyboardButton("ᴏᴡɴᴇʀ", url=f"https://t.me/BTW_AYU_0"),
     InlineKeyboardButton("• ʙᴀᴄᴋ •", callback_data="back_to_start"),
     InlineKeyboardButton("sᴜᴘᴘᴏʀᴛ", url="https://t.me/NOBITA_PROFESY")]
]

@app.on_callback_query(filters.regex("vip_back"))
async def vip_back_callback_handler(_, query: CallbackQuery):
    await query.message.edit_caption(caption=START_TEXT, reply_markup=InlineKeyboardMarkup(gd_buttons))

@app.on_callback_query(filters.regex("back_to_start"))
async def back_to_start_callback_handler(_, query: CallbackQuery):
    await query.answer()
    await query.message.delete()
    await start_command_handler(_, query.message)

# Bot Functionality
@app.on_message(filters.command("ping"))
async def activevc(_, message: Message):
    uptime = time_formatter((time.time() - start_time) * 1000)
    cpu = psutil.cpu_percent()
    storage = psutil.disk_usage('/')

    python_version = platform.python_version()

    reply_text = (
        f"➪ᴜᴘᴛɪᴍᴇ: {uptime}\n"
        f"➪ᴄᴘᴜ: {cpu}%\n"
        f"➪ꜱᴛᴏʀᴀɢᴇ: {size_formatter(storage.total)} [ᴛᴏᴛᴀʟ]\n"
        f"➪{size_formatter(storage.used)} [ᴜsᴇᴅ]\n"
        f"➪{size_formatter(storage.free)} [ғʀᴇᴇ]\n"
        f"➪ᴊᴀʀᴠɪs ᴠᴇʀsɪᴏɴ: {python_version},"
    )

    await message.reply(reply_text, quote=True)


# Add the broadcast command handler
@app.on_message(filters.command("broad") & filters.user(OWNER_ID))
async def broadcast_command_handler(_, message: Message):
    if len(message.command) < 2:
        await message.reply_text("Please provide a message to broadcast.")
        return

    broadcast_message = message.text.split(None, 1)[1]
    async for dialog in app.iter_dialogs():
        try:
            await app.send_message(dialog.chat.id, broadcast_message)
        except Exception as e:
            logging.error(f"Failed to send message to {dialog.chat.id}: {str(e)}")

    await message.reply_text("Broadcast message sent to all users and chats.")



# Handle Forbidden Keywords
@app.on_message()
async def handle_message(client, message):
    if any(keyword in message.text for keyword in FORBIDDEN_KEYWORDS):
        logging.info(f"Deleting message with ID {message.id}")
        await message.delete()
        await message.reply_text(f"@{message.from_user.username} 𝖣𝗈𝗇'𝗍 𝗌𝖾𝗇𝖽 𝗇𝖾𝗑𝗍 𝗍𝗂𝗆𝖾!")
    elif message.caption and any(keyword in message.caption for keyword in FORBIDDEN_KEYWORDS):
        logging.info(f"Deleting message with ID {message.id}")
        await message.delete()
        await message.reply_text(f"@{message.from_user.username} 𝖣𝗈𝗇'𝗍 𝗌𝖾𝗇𝖽 𝗇𝖾𝗑𝗍 𝗍𝗂𝗆𝖾!")

def is_authorized(user_id: int) -> bool:
    return user_id in OWNER_ID  # Add authorized user IDs in OWNER_ID

# Delete long edited messages but keep short messages and emoji reactions
async def delete_long_edited_messages(client, edited_message: Message):
    if edited_message.text and len(edited_message.text.split()) > 20:
        await edited_message.delete()
    elif edited_message.sticker or edited_message.animation:
        return

@app.on_edited_message(filters.group & ~filters.me)
async def handle_edited_messages(_, edited_message: Message):
    if not is_authorized(edited_message.from_user.id):
        await edited_message.delete()
    else:
        await delete_long_edited_messages(_, edited_message)

# Delete long messages in groups and reply with a warning
MAX_MESSAGE_LENGTH = 25  # Define the maximum allowed length for a message

async def delete_long_messages(client, message: Message):
    if message.text and len(message.text.split()) > MAX_MESSAGE_LENGTH:
        await message.delete()

@app.on_message(filters.group & ~filters.me)
async def handle_messages(_, message: Message):
    await delete_long_messages(_, message)

if __name__ == "__main__":
    app.run()
