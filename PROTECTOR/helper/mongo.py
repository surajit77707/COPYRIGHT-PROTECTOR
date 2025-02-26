import sys
from config import MONGO_URI  # Correct import usage  # Correct import usage
from motor.motor_asyncio import AsyncIOMotorClient
import logging

# Set up logging
logging.basicConfig(level=logging.INFO)

# Mongo Database
try:
    mongodb = AsyncIOMotorClient(MONGO_URL).ULTRON
except Exception as e:
    logging.error("Failed to connect to MongoDB: %s", e)
    print("Please change your MongoDB settings.")
    sys.exit()

chatsdb = mongodb.tgchatsdb
usersdb = mongodb.tgusersdb


# All Served Users
async def is_served_user(user_id: int) -> bool:
    user = await usersdb.find_one({"user_id": user_id})
    if not user:
        return False
    return True


async def get_served_users() -> list:
    users_list = []
    async for user in usersdb.find({"user_id": {"$gt": 0}}):
        users_list.append(user)
    return users_list


async def add_served_user(user_id: int):
    is_served = await is_served_user(user_id)
    if is_served:
        return
    return await usersdb.insert_one({"user_id": user_id})


# All Served Chats
async def get_served_chats() -> list:
    chats_list = []
    async for chat in chatsdb.find({"chat_id": {"$lt": 0}}):
        chats_list.append(chat)
    return chats_list


async def is_served_chat(chat_id: int) -> bool:
    chat = await chatsdb.find_one({"chat_id": chat_id})
    if not chat:
        return False
    return True


async def add_served_chat(chat_id: int):
    is_served = await is_served_chat(chat_id)
    if is_served:
        return
    return await chatsdb.insert_one({"chat_id": chat_id})
