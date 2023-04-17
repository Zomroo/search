from pyrogram import Client, filters
import requests
import json
import os

# Set up your Pyrogram API ID, API hash, and bot token
API_ID = 16844842
API_HASH = "f6b0ceec5535804be7a56ac71d08a5d4"
BOT_TOKEN = "5931504207:AAF-jzKC8USclrFYrtcaeAZifQcmEcwFNe4"

@app.on_message(filters.command("start"))
async def start_command(client, message):
    await message.reply_text("Hi! Send me an image and I'll find the topmost similar result.")

@app.on_message(filters.photo)
async def download_and_upload_image(client, message):
    photo = message.photo[-1] # Get the largest photo size
    file_path = await client.download_media(photo, file_name="image.jpg") # Download the image to a temporary file
    with open(file_path, "rb") as f:
        files = {"file": f}
        response = requests.post("https://telegra.ph/upload", files=files) # Upload the image to telegra.ph
        result = response.json()[0]
        telegraph_url = "https://telegra.ph" + result["src"]
    os.remove(file_path) # Delete the temporary file
    yandex_url = "https://www.yandex.com/images/search?rpt=imageview&url=" + telegraph_url # Generate the Yandex search URL
    response = requests.get(yandex_url) # Search for the image on Yandex
    html = response.text
    start_index = html.find('img_url=')
    if start_index == -1:
        await message.reply_text("Sorry, I couldn't find any results.")
        return
    start_index += len('img_url=') + 1
    end_index = html.find('&amp;', start_index)
    if end_index == -1:
        end_index = len(html)
    result_url = html[start_index:end_index]
    result_url = result_url.encode().decode('unicode-escape')
    await message.reply_text(result_url) # Reply with the topmost result URL

app.run() # Run the bot
