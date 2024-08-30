from pyrogram import Client, filters
from pyrogram.types import Message, InlineKeyboardButton, InlineKeyboardMarkup, InputMediaPhoto
import os

# Replace these with your actual credentials
API_ID = "25064357"
API_HASH = "cda9f1b3f9da4c0c93d1f5c23ccb19e2"
BOT_TOKEN = "7329929698:AAGD5Ccwm0qExCq9_6GVHDp2E7iidLH-McU"

# Initialize the Pyrogram Client
app = Client("sung_bot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

# Command handler for /start
@app.on_message(filters.command("start") & filters.private)
async def start(client: Client, message: Message):
    # Send an image first
    await message.reply_photo(
        "https://telegra.ph//file/919714d04904fae43ffd0.jpg"
    )
    
    # Welcome message
    welcome_text = "Welcome to the bot! Please choose an option below:"
    
    # Inline keyboard with buttons arranged vertically
    keyboard = InlineKeyboardMarkup(
        [
            [InlineKeyboardButton("My Master", url="http://t.me/sung_jinwo4")],
            [InlineKeyboardButton("Support", url="http://t.me/beyondlimit7")],
            [InlineKeyboardButton("Destroyer", url="http://t.me/souls_borns")],
            [InlineKeyboardButton("Network", url="http://t.me/soul_networks")],
        ]
    )
    
    # Sending the message with the inline keyboard
    await message.reply(welcome_text, reply_markup=keyboard)

# Create a set to store blacklisted words and stickers
blacklisted_words = set()
blacklisted_stickers = set()

# Command to blacklist a word
@app.on_message(filters.command("blacklist") & filters.private)
async def blacklist_word(client, message: Message):
    if len(message.command) < 2:
        await message.reply_text("Please provide a word to blacklist.")
        return

    word = message.command[1].lower()
    blacklisted_words.add(word)
    await message.reply_text(f"Word '{word}' has been blacklisted.")

# Command to blacklist a sticker
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

if __name__ == "__main__":
    app.run()
