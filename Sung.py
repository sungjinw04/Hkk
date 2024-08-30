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

# Handler for the /randiproof command
@app.on_message(filters.command("randiproof") & filters.reply)
async def randiproof(client, message: Message):
    logging.info("randiproof command received")
    reply = message.reply_to_message
    try:
        if reply:
            if reply.text:
                logging.info(f"Attempting to blacklist text: {reply.text}")
                blacklist_collection.insert_one({"type": "text", "content": reply.text, "chat_id": message.chat.id})
                await message.reply_text(f"Text blacklisted successfully.")
                logging.info("Text blacklisted successfully.")
            elif reply.sticker:
                logging.info(f"Attempting to blacklist sticker: {reply.sticker.file_id}")
                blacklist_collection.insert_one({"type": "sticker", "content": reply.sticker.file_id, "chat_id": message.chat.id})
                await message.reply_text(f"Sticker blacklisted successfully.")
                logging.info("Sticker blacklisted successfully.")
    except Exception as e:
        logging.error(f"Error in randiproof command: {e}")

# Simple echo handler to confirm bot is working
@app.on_message(filters.text & filters.group)
async def echo(client, message: Message):
    logging.info(f"Echoing message: {message.text}")
    await message.reply_text(f"You said: {message.text}")

if __name__ == "__main__":
    logging.info("Starting bot...")
    app.run()
