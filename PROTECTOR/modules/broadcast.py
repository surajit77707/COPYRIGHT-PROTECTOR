import asyncio
from pyrogram import filters
from pyrogram.errors import FloodWait
from config import SUDOERS
from PROTECTOR import PROTECTOR as app
from PROTECTOR.helper.mongo import get_served_chats, get_served_users

IS_BROADCASTING = False

@app.on_message(filters.command(["broadcast", "gcast", "bcast"]) & SUDOERS)
async def broadcast_message(client, message):
    global IS_BROADCASTING

    # Check if the message is a reply and extract the message_id if available
    if message.reply_to_message and message.reply_to_message.message_id:
        x = message.reply_to_message.message_id
        y = message.chat.id
    else:
        if len(message.command) < 2:
            return await message.reply_text("**Usage**:\n/broadcast [MESSAGE] or [Reply to a Message]")
        query = message.text.split(None, 1)[1]
        query = query.replace("-pin", "").replace("-nobot", "").replace("-pinloud", "").replace("-user", "")
        if query == "":
            return await message.reply_text("Please provide some text to broadcast.")

    IS_BROADCASTING = True
    sent, pin, susr = 0, 0, 0  # Tracking counts

    # Fetch chats and users efficiently
    chats = [int(chat["chat_id"]) for chat in await get_served_chats()]
    users = [int(user["user_id"]) for user in await get_served_users()]

    # Bot broadcast inside chats
    if "-nobot" not in message.text:
        for i in chats:
            if i == -1002059718978:  # Exclude specific chat ID
                continue
            try:
                m = await app.forward_messages(i, y, x) if message.reply_to_message else await app.send_message(i, text=query)
                
                if "-pin" in message.text:
                    try:
                        await m.pin(disable_notification=True)
                        pin += 1
                    except Exception:
                        continue
                elif "-pinloud" in message.text:
                    try:
                        await m.pin(disable_notification=False)
                        pin += 1
                    except Exception:
                        continue
                sent += 1
            except FloodWait as e:
                flood_time = int(e.x)
                if flood_time > 200:
                    print(f"Skipping chat {i} due to high FloodWait ({flood_time}s)")
                    continue
                await asyncio.sleep(flood_time)
            except Exception as e:
                print(f"Error sending to chat {i}: {e}")
                continue
        try:
            await message.reply_text(f"**Broadcasted Message In {sent} Chats with {pin} Pins.**")
        except:
            pass

    # Bot broadcasting to users
    if "-user" in message.text:
        for i in users:
            try:
                m = await app.forward_messages(i, y, x) if message.reply_to_message else await app.send_message(i, text=query)
                susr += 1
            except FloodWait as e:
                flood_time = int(e.x)
                if flood_time > 200:
                    print(f"Skipping user {i} due to high FloodWait ({flood_time}s)")
                    continue
                await asyncio.sleep(flood_time)
            except Exception as e:
                print(f"Error sending to user {i}: {e}")
                continue
        try:
            await message.reply_text(f"**Broadcasted Message to {susr} Users.**")
        except:
            pass

    IS_BROADCASTING = False
