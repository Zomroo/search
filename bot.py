import os
from PIL import Image
from pyrogram import Client, filters

app = Client("my_bot")

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
