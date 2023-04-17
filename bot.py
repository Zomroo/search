import os
import urllib.request
import requests
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters

TELEGRAM_TOKEN = "YOUR_TELEGRAM_BOT_TOKEN"
TELEGRAPH_TOKEN = "5931504207:AAF-jzKC8USclrFYrtcaeAZifQcmEcwFNe4"

def start(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text="Hi! Send me an image and I'll upload it to telegra.ph for you.")

def handle_image(update, context):
    # Download the image
    photo_file = context.bot.getFile(update.message.photo[-1].file_id)
    photo_file.download('image.jpg')

    # Upload the image to telegra.ph
    response = requests.post('https://telegra.ph/upload', files={'file': open('image.jpg', 'rb')})
    response.raise_for_status()

    # Get the URL of the uploaded image
    image_url = response.json()[0]['src']

    # Create a telegra.ph link for the image
    telegraph_response = requests.post('https://api.telegra.ph/createPage', json={
        'access_token': TELEGRAPH_TOKEN,
        'title': 'Image',
        'author_name': 'Telegram Bot',
        'content': [{'tag': 'img', 'attrs': {'src': image_url}}]
    })
    telegraph_response.raise_for_status()
    telegraph_url = 'https://telegra.ph/{}'.format(telegraph_response.json()['result']['path'])

    # Send the telegra.ph link to the user
    context.bot.send_message(chat_id=update.effective_chat.id, text=telegraph_url)

    # Delete the image
    os.remove('image.jpg')

if __name__ == '__main__':
    updater = Updater(TELEGRAM_TOKEN, use_context=True)
    dp = updater.dispatcher
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(MessageHandler(Filters.photo, handle_image))
    updater.start_polling()
    updater.idle()
