import os
import urllib.request
import requests
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters

TELEGRAPH_TOKEN = "8bbe8974d80380a9bc560ce2c91443ab78bc182a8d04a6be0c6c7bcb6038"
TELEGRAM_TOKEN = "5931504207:AAF-jzKC8USclrFYrtcaeAZifQcmEcwFNe4"
YANDEX_API_KEY = "pdct.1.1.20230417T173414Z.11f0fa2998c61794.8f5c7895468d7cb94d573c07710a39ad856eefc2"

def start(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text="Hi! Send me an image and I'll upload it to telegra.ph for you.")

def handle_image(update, context):
    # Download the image
    photo_file = context.bot.getFile(update.message.photo[-1].file_id)
    photo_file.download('image.jpg')

    # Upload the image to telegra.ph
    response = requests.post('https://telegra.ph/upload', files={'file': open('image.jpg', 'rb')})
    if response.status_code != 200:
        context.bot.send_message(chat_id=update.effective_chat.id, text="Failed to upload image to telegra.ph.")
        return

    # Get the URL of the uploaded image
    if isinstance(response.json(), list):
        image_url = response.json()[0].get('src')
    elif isinstance(response.json(), dict):
        image_url = response.json().get('src')
    else:
        context.bot.send_message(chat_id=update.effective_chat.id, text="Failed to get URL of uploaded image.")
        return

    if not image_url:
        context.bot.send_message(chat_id=update.effective_chat.id, text="Failed to get URL of uploaded image.")
        return

    # Use the Yandex API to find visually similar images
    params = {
        "apikey": YANDEX_API_KEY,
        "lang": "en",
        "image_url": image_url,
        "filter": "images",
        "per_page": 1
    }
    response = requests.get("https://api.webmaster.yandex.net/v4/management/hosts/qa.yandex.net/verification?callback=jsonp1&"+ urllib.parse.urlencode(params))
    if response.status_code != 200:
        context.bot.send_message(chat_id=update.effective_chat.id, text="Failed to find visually similar images.")
        return

    # Get the URL of the best match image
    best_match_url = response.json()['items'][0]['url'] if len(response.json().get('items', [])) > 0 else 'No results found.'
    context.bot.send_message(chat_id=update.effective_chat.id, text=best_match_url)


updater = Updater(token=TELEGRAM_TOKEN, use_context=True)
dispatcher = updater.dispatcher
dispatcher.add_handler(CommandHandler("start", start))
dispatcher.add_handler(MessageHandler(Filters.photo, handle_image))

updater.start_polling()
updater.idle()
