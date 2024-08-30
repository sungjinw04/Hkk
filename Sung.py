from pyrogram import Client, filters
from pyrogram.types import Message
import os

# Replace these with your actual credentials
API_ID = "25064357"
API_HASH = "cda9f1b3f9da4c0c93d1f5c23ccb19e2"
BOT_TOKEN = "7329929698:AAGD5Ccwm0qExCq9_6GVHDp2E7iidLH-McU"

# Initialize the Pyrogram Client
app = Client("sung_bot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

# Sets to store blacklisted words and stickers
blacklisted_words = set()
blacklisted_stickers = set()

# Command to add a word to the blacklist
@app.on_message(filters.command("blacklist") & filters.private)
async def blacklist_word(client, message: Message):
    if len(message.command) < 2:
        await message.reply_text("Please provide a word to blacklist.")
        return

    word = message.command[1].lower()
    blacklisted_words.add(word)
    await message.reply_text(f"Word '{word}' has been blacklisted.")

# Command to add a sticker to the blacklist by replying to a sticker
@app.on_message(filters.command("blackliststicker") & filters.reply & filters.private)
async def blacklist_sticker(client, message: Message):
    if message.reply_to_message.sticker:
        sticker_id = message.reply_to_message.sticker.file_id
        blacklisted_stickers.add(sticker_id)
        await message.reply_text("Sticker has been blacklisted.")
    else:
        await message.reply_text("Please reply to a sticker to blacklist it.")

# Delete messages containing blacklisted words
@app.on_message(filters.text)
async def delete_blacklisted_words(client, message: Message):
    for word in blacklisted_words:
        if word in message.text.lower():
            await message.delete()
            break

# Delete messages containing blacklisted stickers
@app.on_message(filters.sticker)
async def delete_blacklisted_stickers(client, message: Message):
    if message.sticker.file_id in blacklisted_stickers:
        await message.delete()

# Run the bot
if __name__ == "__main__":
    app.run()
