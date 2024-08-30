from pyrogram import Client, filters
from pyrogram.types import Message
from pymongo import MongoClient

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
        "message_id": message.id,  # Corrected from message.message_id to message.id
        "chat_id": message.chat.id,
        "user_id": message.from_user.id if message.from_user else None,
        "username": message.from_user.username if message.from_user else None,
        "text": message.text,
        "sticker_id": message.sticker.file_id if message.sticker else None,
        "date": message.date
    }
    messages_collection.insert_one(message_data)

# Handler to track and save all messages
@app.on_message(filters.group)
async def track_messages(client, message: Message):
    save_message_to_db(message)
    
    # Check for blacklisted content
    if message.text:
        blacklisted_text = blacklist_collection.find_one({"type": "text", "content": message.text, "chat_id": message.chat.id})
        if blacklisted_text:
            await message.delete()
    elif message.sticker:
        blacklisted_sticker = blacklist_collection.find_one({"type": "sticker", "content": message.sticker.file_id, "chat_id": message.chat.id})
        if blacklisted_sticker:
            await message.delete()

# Handler for the /randiproof command
@app.on_message(filters.command("randiproof") & filters.reply & filters.user("admin"))
async def randiproof(client, message: Message):
    reply = message.reply_to_message
    if reply:
        if reply.text:
            # Blacklist the text
            blacklist_collection.insert_one({"type": "text", "content": reply.text, "chat_id": message.chat.id})
            await message.reply_text(f"Text blacklisted successfully.")
        elif reply.sticker:
            # Blacklist the sticker ID
            blacklist_collection.insert_one({"type": "sticker", "content": reply.sticker.file_id, "chat_id": message.chat.id})
            await message.reply_text(f"Sticker blacklisted successfully.")

if __name__ == "__main__":
    app.run()
