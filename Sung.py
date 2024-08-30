import logging
from pyrogram import Client, filters
from pyrogram.types import Message
from pymongo import MongoClient

# Enable logging to help with debugging
logging.basicConfig(level=logging.INFO)

# Initialize the MongoDB client and select the database and collections
mongo_client = MongoClient("mongodb+srv://Sungjinwoo4:sung4224@cluster0.ayaos.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0")
db = mongo_client["telegram_bot_db"]
messages_collection = db["messages"]
blacklist_collection = db["blacklist"]

# Initialize the Pyrogram Client
app = Client("my_bot", api_id="25064357", api_hash="cda9f1b3f9da4c0c93d1f5c23ccb19e2", bot_token="7329929698:AAGD5Ccwm0qExCq9_6GVHDp2E7iidLH-McU")

# Function to save messages to MongoDB
def save_message_to_db(message: Message):
    message_data = {
        "message_id": message.id,
        "chat_id": message.chat.id,
        "user_id": message.from_user.id if message.from_user else None,
        "username": message.from_user.username if message.from_user else None,
        "text": message.text,
        "sticker_id": message.sticker.file_id if message.sticker else None,
        "date": message.date
    }
    try:
        messages_collection.insert_one(message_data)
        logging.info(f"Message saved: {message_data}")
    except Exception as e:
        logging.error(f"Error saving message to MongoDB: {e}")

# Handler to track and save all messages
@app.on_message(filters.group)
async def track_messages(client, message: Message):
    save_message_to_db(message)
    
    # Check for blacklisted content
    try:
        if message.text:
            logging.info(f"Checking text: {message.text}")
            blacklisted_text = blacklist_collection.find_one({"type": "text", "content": message.text, "chat_id": message.chat.id})
            if blacklisted_text:
                await message.delete()
                logging.info(f"Deleted blacklisted text: {message.text}")
        elif message.sticker:
            logging.info(f"Checking sticker: {message.sticker.file_id}")
            blacklisted_sticker = blacklist_collection.find_one({"type": "sticker", "content": message.sticker.file_id, "chat_id": message.chat.id})
            if blacklisted_sticker:
                await message.delete()
                logging.info(f"Deleted blacklisted sticker: {message.sticker.file_id}")
    except Exception as e:
        logging.error(f"Error processing message: {e}")

# Handler for the /randiproof command
@app.on_message(filters.command("randiproof") & filters.reply & filters.user("admin"))
async def randiproof(client, message: Message):
    reply = message.reply_to_message
    try:
        if reply:
            if reply.text:
                logging.info(f"Blacklisting text: {reply.text}")
                blacklist_collection.insert_one({"type": "text", "content": reply.text, "chat_id": message.chat.id})
                await message.reply_text(f"Text blacklisted successfully.")
            elif reply.sticker:
                logging.info(f"Blacklisting sticker: {reply.sticker.file_id}")
                blacklist_collection.insert_one({"type": "sticker", "content": reply.sticker.file_id, "chat_id": message.chat.id})
                await message.reply_text(f"Sticker blacklisted successfully.")
    except Exception as e:
        logging.error(f"Error blacklisting content: {e}")

if __name__ == "__main__":
    app.run()
