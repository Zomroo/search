import os
from pyrogram import Client, filters
from pyrogram.types import Message
import requests

# Set up your Yandex API key
YANDEX_API_KEY = os.environ.get("pdct.1.1.20230417T173414Z.11f0fa2998c61794.8f5c7895468d7cb94d573c07710a39ad856eefc2")

# Set up your Pyrogram API ID, API hash, and bot token
API_ID = os.environ.get("16844842")
API_HASH = os.environ.get("f6b0ceec5535804be7a56ac71d08a5d4")
BOT_TOKEN = os.environ.get("5931504207:AAF-jzKC8USclrFYrtcaeAZifQcmEcwFNe4")

# Create the Pyrogram client object
app = Client("my_bot", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

# Define the command handler for the /start command
@app.on_message(filters.command("start"))
def start_command_handler(client: Client, message: Message):
    message.reply_text("Hi! Send me an image and I'll try to find the waifu or character's name for you.")

# Define the message handler for images
@app.on_message(filters.photo)
def image_handler(client: Client, message: Message):
    # Download the image from Telegram
    file_path = client.download_media(message.photo.file_id)

    # Send the image to Yandex for reverse image search
    yandex_result = search_yandex(file_path)

    # Reply with the Yandex result
    message.reply_text(f"Result: {yandex_result}")

def search_yandex(file_path: str) -> str:
    # Set up the request URL and parameters
    url = "https://yandex.com/images/search"
    headers = {"User-Agent": "Mozilla/5.0"}
    params = {"rpt": "imageview", "format": "json", "request": "{\"blocks\":[{\"block\":\"b-page_type_search-by-image__link\"}],\"params\":{\"url\":\"" + file_path + "\",\"rpt\":\"imageview\"}}"}

    # Send the request to Yandex and parse the response
    response = requests.get(url, headers=headers, params=params)
    data = response.json()
    name = data["blocks"][0]["params"]["name"]

    return name

# Start the Pyrogram client
app.run()
