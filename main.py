import os
import requests
from pyrogram import Client, filters
from pyrogram.types import Message

# Set up your Yandex API key
YANDEX_API_KEY = "pdct.1.1.20230417T173414Z.11f0fa2998c61794.8f5c7895468d7cb94d573c07710a39ad856eefc2"

# Set up your Pyrogram API ID, API hash, and bot token
API_ID = 16844842
API_HASH = "f6b0ceec5535804be7a56ac71d08a5d4"
BOT_TOKEN = "5931504207:AAF-jzKC8USclrFYrtcaeAZifQcmEcwFNe4"

# Set up the Telegraph access token
TELEGRAPH_ACCESS_TOKEN = "8bbe8974d80380a9bc560ce2c91443ab78bc182a8d04a6be0c6c7bcb6038
"

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

    # Upload the image to Telegraph
    telegraph_url = upload_to_telegraph(file_path)

    # Search Yandex for the image using the Telegraph link
    yandex_result = search_yandex(telegraph_url)

    # Reply with the Yandex result
    message.reply_text(f"Result: {yandex_result}")

def upload_to_telegraph(file_path: str) -> str:
    # Set up the request URL and parameters
    url = "https://telegra.ph/upload"
    files = {"file": ("image.jpg", open(file_path, "rb"))}
    headers = {"Authorization": f"Bearer {TELEGRAPH_ACCESS_TOKEN}"}

    # Send the request to Telegraph and parse the response
    response = requests.post(url, files=files, headers=headers)
    data = response.json()

    # Check if the "src" key is present
    if "src" in data:
        return data["src"]

    # Return an error message if no src was found
    return "Sorry, I couldn't upload the image to Telegraph."

def search_yandex(telegraph_url: str) -> str:
    # Set up the request URL and parameters
    url = "https://yandex.com/images/search"
    headers = {"User-Agent": "Mozilla/5.0"}
    params = {"rpt": "imageview", "format": "json", "request": "{\"blocks\":[{\"block\":\"b-page_type_search-by-image__link\"}],\"params\":{\"url\":\"" + telegraph_url + "\",\"rpt\":\"imageview\"}}"}
    headers["Authorization"] = "Api-Key " + YANDEX_API_KEY

    # Send the request to Yandex and parse the response
    response = requests.get(url, headers=headers, params=params)
    data = response.json()

    # Check if the "blocks" key is present
    if "blocks" in data:
        # Get the name from the first block

        name = data["blocks"][0]["params"].get("name")
        if name:
            return name

    # Return an error message if no name was found
    return "Sorry, I couldn't find the name of the character in this image."


# Start the Pyrogram client
app.run()
