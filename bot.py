import os
import urllib.request
import requests
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters

TELEGRAPH_TOKEN = "8bbe8974d80380a9bc560ce2c91443ab78bc182a8d04a6be0c6c7bcb6038"
TELEGRAM_TOKEN = "5931504207:AAF-jzKC8USclrFYrtcaeAZifQcmEcwFNe4"
YANDEX_API_KEY = "pdct.1.1.20230417T203954Z.89329fe738fb735b.df3cfd241dbca08dede3ec358ba389728758852f"

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

    # Search for the image on Yandex
    search_url = 'https://yandex.com/images/search'
    headers = {'Authorization': 'Api-Key ' + YANDEX_API_KEY}
    params = {'url': telegraph_url, 'rpt': 'imageview'}
    try:
        response = requests.get(search_url, headers=headers, params=params)
        response.raise_for_status()
        data = response.json()
    except requests.exceptions.HTTPError as e:
        context.bot.send_message(chat_id=update.effective_chat.id, text="Error: {}".format(str(e)))
        return
    except requests.exceptions.JSONDecodeError as e:
        context.bot.send_message(chat_id=update.effective_chat.id, text="Error decoding JSON response from Yandex: {}".format(str(e)))
        return

    if 'items' not in data or not data['items']:
        context.bot.send_message(chat_id=update.effective_chat.id, text="No results found for image search.")
        return

    best_match_url = data['items'][0]['url']

    # Send the best match URL to the user
    context.bot.send_message(chat_id=update.effective_chat.id, text=best_match_url)

    # Delete the image
    os.remove('image.jpg')

def main():
    updater = Updater(TELEGRAM_TOKEN, use_context=True)
    dp = updater.dispatcher
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(MessageHandler(Filters.photo, handle_image))
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
