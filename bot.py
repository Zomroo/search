import os
from PIL import Image
from pyrogram import Client, filters

API_ID = 16844842
API_HASH = "f6b0ceec5535804be7a56ac71d08a5d4"
BOT_TOKEN = "5931504207:AAF-jzKC8USclrFYrtcaeAZifQcmEcwFNe

# Create the Pyrogram client object
app = Client("my_bot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

TMP_DOWNLOAD_DIRECTORY = "./"

@app.on_message(filters.photo)
async def telegraph(client, message):
    # Download image
    image_path = await client.download_media(
        message=message,
        file_name=TMP_DOWNLOAD_DIRECTORY
    )
    
    # Upload to telegra.ph
    with open(image_path, "rb") as f:
        img_url = await client.create_media("Photo", media=f)
    
    # Send URL back to user
    await message.reply(f"Uploaded to telegra.ph: {img_url}")

app.run()
