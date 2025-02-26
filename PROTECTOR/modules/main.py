import logging
import os
import platform
import psutil
import time
import json
import motor.motor_asyncio
from pyrogram import Client, filters
from pyrogram.types import CallbackQuery, InlineKeyboardButton, InlineKeyboardMarkup, Message
from config import BOT_USERNAME, OWNER_ID, MONGO_URI
from PROTECTOR import PROTECTOR as app

# MongoDB Setup
client = motor.motor_asyncio.AsyncIOMotorClient(MONGO_URI)
db = client["copyright_protector"]
users_collection = db["authorized_users"]

# Constants
START_TEXT = """<b>🤖 ᴄᴏᴘʏʀɪɢʜᴛ ᴘʀᴏᴛᴇᴄᴛᴏʀ 🛡️</b>

ʜᴇʏ ᴛʜɪs ɪs ᴄᴏᴘʏʀɪɢʜᴛ ᴘʀᴏᴛᴇᴄᴛᴏʀ ʀᴏʙᴏᴛ 🤖\n
ᴡᴇ ᴇɴsᴜʀᴇ ʏᴏᴜʀ ɢʀᴏᴜᴘ's sᴇᴄᴜʀɪᴛʏ 📌\n
ᴛʜɪs ʙᴏᴛ ᴄᴀɴ ʀᴇᴍᴏᴠᴇ ʟᴏɴɢ ᴇᴅɪᴛᴇᴅ ᴛᴇxᴛs ᴀɴᴅ ᴄᴏᴘʏʀɪɢʜᴛᴇᴅ ᴍᴀᴛᴇʀɪᴀʟ 📁\n
ᴊᴜsᴛ ᴀᴅᴅ ᴛʜɪs ʙᴏᴛ ᴛᴏ ʏᴏᴜʀ ɢʀᴏᴜᴘ ᴀɴᴅ ᴍᴀᴋᴇ ɪᴛ ᴀɴ ᴀᴅᴍɪɴ\n
ғᴇᴇʟ ғʀᴇᴇ ғʀᴏᴍ ᴀɴʏ ᴛʏᴘᴇ ᴏғ **ᴄᴏᴘʏʀɪɢʜᴛ** 🛡️
"""
MAX_MESSAGE_LENGTH = 40
Devs = ["7044783841", "7019293589", "6757745933"]

start_time = time.time()

# Buttons
gd_buttons = [
    [InlineKeyboardButton("ᴏᴡɴᴇʀ", url="https://t.me/JARVIS_V2"),
     InlineKeyboardButton("• ʙᴀᴄᴋ •", callback_data="back_to_start"),
     InlineKeyboardButton("sᴜᴘᴘᴏʀᴛ", url="https://t.me/JARVIS_V_SUPPORT")]
]

# Utility Functions
async def is_admin(client, message):
    chat_member = await client.get_chat_member(message.chat.id, client.me.id)
    return chat_member.status in ("administrator", "creator")

async def is_authorized(user_id):
    return await users_collection.find_one({"user_id": user_id}) is not None

async def authorize_user(user_id):
    await users_collection.insert_one({"user_id": user_id})

async def unauthorize_user(user_id):
    await users_collection.delete_one({"user_id": user_id})

async def list_authorized_users():
    users = await users_collection.find().to_list(None)
    return [str(user["user_id"]) for user in users]

# Command Handlers
@app.on_message(filters.command("start"))
async def start_command_handler(_, msg):
    buttons = [[InlineKeyboardButton("ᴀᴅᴅ ᴍᴇ", url=f"https://t.me/{BOT_USERNAME}?startgroup=true")]]
    await msg.reply_photo(
        photo="https://telegra.ph/file/8f6b2cc26b522a252b16a.jpg",
        caption=START_TEXT,
        reply_markup=InlineKeyboardMarkup(buttons)
    )

@app.on_message(filters.command("ping"))
async def ping(_, message):
    uptime = time.time() - start_time
    cpu = psutil.cpu_percent()
    storage = psutil.disk_usage('/')
    python_version = platform.python_version()

    await message.reply(
        f"➪ Uptime: {uptime:.2f}s\n"
        f"➪ CPU: {cpu}%\n"
        f"➪ Storage: {storage.total // (1024 ** 3)}GB [Total]\n"
        f"➪ {storage.used // (1024 ** 3)}GB [Used]\n"
        f"➪ {storage.free // (1024 ** 3)}GB [Free]\n"
        f"➪ Python Version: {python_version}"
    )

@app.on_message(filters.command("auth") & filters.user(OWNER_ID))
async def auth_user(_, message):
    if len(message.command) != 2:
        await message.reply_text("Usage: /auth <user_id>")
        return

    user_id = int(message.command[1])
    if not await is_authorized(user_id):
        await authorize_user(user_id)
        await message.reply_text(f"User {user_id} has been authorized.")
    else:
        await message.reply_text(f"User {user_id} is already authorized.")

@app.on_message(filters.command("unauth") & filters.user(OWNER_ID))
async def unauth_user(_, message):
    if len(message.command) != 2:
        await message.reply_text("Usage: /unauth <user_id>")
        return

    user_id = int(message.command[1])
    if await is_authorized(user_id):
        await unauthorize_user(user_id)
        await message.reply_text(f"User {user_id} has been unauthorized.")
    else:
        await message.reply_text(f"User {user_id} is not authorized.")

@app.on_message(filters.command("listauth") & filters.user(OWNER_ID))
async def list_auth_users(_, message):
    users = await list_authorized_users()
    if not users:
        await message.reply_text("No users are currently authorized.")
    else:
        await message.reply_text("Authorized Users:\n" + "\n".join(users))

@app.on_message(filters.group & ~filters.me)
async def handle_messages(client, message):
    if not await is_admin(client, message):
        return
    if not (await is_authorized(message.from_user.id) or message.from_user.id in Devs):
        if message.text and len(message.text.split()) > MAX_MESSAGE_LENGTH:
            await message.reply_text(f"{message.from_user.mention}, ᴘʟᴇᴀsᴇ ᴋᴇᴇᴘ ʏᴏᴜʀ ᴍᴇssᴀɢᴇ sʜᴏʀᴛ.")
            await message.delete()

if __name__ == "__main__":
    app.run()
