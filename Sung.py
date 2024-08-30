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

# Handler to track and delete blacklisted messages
@app.on_message()
async def track_messages(client, message: Message):
    logging.debug(f"Received message: {message.text}, Sticker ID: {message.sticker.file_id if message.sticker else 'None'}")
    
    try:
        if message.text:
            logging.debug(f"Checking text: {message.text}")
            blacklisted_text = blacklist_collection.find_one({"type": "text", "content": message.text, "chat_id": message.chat.id})
            if blacklisted_text:
                logging.debug(f"Attempting to delete blacklisted text: {message.text}")
                try:
                    await message.delete()
                    logging.debug("Message deleted successfully.")
                except Exception as e:
                    logging.error(f"Error deleting message: {e}")
        elif message.sticker:
            logging.debug(f"Checking sticker: {message.sticker.file_id}")
            blacklisted_sticker = blacklist_collection.find_one({"type": "sticker", "content": message.sticker.file_id, "chat_id": message.chat.id})
            if blacklisted_sticker:
                logging.debug(f"Attempting to delete blacklisted sticker: {message.sticker.file_id}")
                try:
                    await message.delete()
                    logging.debug("Sticker deleted successfully.")
                except Exception as e:
                    logging.error(f"Error deleting sticker: {e}")
    except Exception as e:
        logging.error(f"Error processing message: {e}")

# Handler for the /randiproof command
@app.on_message()
async def handle_command(client, message: Message):
    if message.text and message.text.startswith("/randiproof"):
        logging.debug("randiproof command received")
        reply = message.reply_to_message
        if reply:
            try:
                if reply.text:
                    logging.debug(f"Attempting to blacklist text: {reply.text}")
                    blacklist_collection.insert_one({"type": "text", "content": reply.text, "chat_id": message.chat.id})
                    await message.reply_text(f"Text blacklisted successfully.")
                    logging.debug("Text blacklisted successfully.")
                elif reply.sticker:
                    logging.debug(f"Attempting to blacklist sticker: {reply.sticker.file_id}")
                    blacklist_collection.insert_one({"type": "sticker", "content": reply.sticker.file_id, "chat_id": message.chat.id})
                    await message.reply_text(f"Sticker blacklisted successfully.")
                    logging.debug("Sticker blacklisted successfully.")
            except Exception as e:
                logging.error(f"Error blacklisting content: {e}")

if __name__ == "__main__":
    logging.info("Starting bot...")
    app.run()
