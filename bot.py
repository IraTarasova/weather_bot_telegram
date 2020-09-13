import json
from datetime import datetime, timezone, timedelta
import uuid

from utils import read_secrets
from telegram.ext import Updater, CommandHandler, MessageHandler
from telegram import Bot
import requests

from owm import WeatherForecast
from utils import token_owm, token_telegram, lat, lon, images_dir


def get_current_forecast(update, context):
    forecast = WeatherForecast(lat, lon, token_owm)
    current_forecast = forecast.get_current_forecast()[0]
    forecast_str = [f'{k}: {v}' for k, v in current_forecast.items()]
    forecast_str = '\n'.join(forecast_str)
    update.message.reply_text(forecast_str)


def get_hourly_forecast(update, context):
    chat_id = update.message.chat_id
    forecast = WeatherForecast(lat, lon, token_owm, '%H:%M %d-%m')
    image_filename = images_dir / f'{str(uuid.uuid4())}.png'
    forecast.get_fig_hourly_temp(image_filename)
    with open(image_filename, 'rb') as fin:
        photo = fin.read()

    requests.get(
        f'https://api.telegram.org/bot{token_telegram}/sendDocument?chat_id={chat_id}',
        files={'document': ('pic.jpg', photo)})
    image_filename.unlink()


def get_image(update, context):
    with open('/home/daloro/dog.jpg', 'rb') as fin:
        photo = fin.read()

    chat_id = update.message.chat_id
    resp = requests.get(
        f'https://api.telegram.org/bot{token_telegram}/sendPhoto?chat_id={chat_id}', files={'photo': ('pic.jpg', photo)})



    # print(resp)
    # print(update.message.parse_entities())
    # update.send_photo(chat_id=update.message.chat_id, photo='https://sun9-51.userapi.com/c848536/v848536355/5aeca/dNCMhPJhNNA.jpg')

    # update.message.reply_photo(photo=photo)
    # context.bot.sendPhoto(chat_id=update.message.chat_id, photo=photo)
    # updates = updater.bot.get_updates()
    # print([u.message.text for u in updates])
    # print(updater.bot.get_updates()[-1].message.chat_id)


updater = Updater(token_telegram, use_context=True)

updater.dispatcher.add_handler(CommandHandler('current_forecast', get_current_forecast))
updater.dispatcher.add_handler(CommandHandler('get_image', get_image))
updater.dispatcher.add_handler(CommandHandler('hourly_forecast', get_hourly_forecast))

updater.start_polling()
updater.idle()






# def url_with_token():
#     return f'https://api.telegram.org/bot{token}'
#
#
# def url_send_message(chat_id, text):
#     return f'{url_with_token()}/sendMessage?chat_id={chat_id}&text={text}'
#
#
# def url_get_updates():
#     return f'{url_with_token()}/getUpdates'
#
#
# # response = requests.get(url_get_updates())
# #
# # print(response.text)
#
#
# response = requests.get(f'{url_with_token()}/sendPhoto?chat_id=472778932&photo=AgACAgIAAxkBAAM2X1iQLspg1Zk1Kqe3eBYAAQsIMgAB0gACZa0xG5cTyUpJRRyu4chH2W5zGZguAAMBAAMCAANtAANsbAACGwQ')


# with open('/home/daloro/Desktop/telegram.json', 'w') as fin:
#     json.dump(response.json(), fin)

# with open('/home/daloro/Desktop/telegram.json', 'r') as fin:
#     response = json.load(fin)
#
#
# print(response)
# print()
#
# chat_ids = []
# for elem in response['result']:
#     chat_id = elem['message']['chat']['id']
#     chat_ids.append(chat_id)
#
# chat_ids = list(set(chat_ids))
#
# print(chat_ids)
#
# text_for_everyone = 'HUI SUKA'
#
# for chat_id in chat_ids:
#     response = requests.get(url_send_message(chat_id, text_for_everyone))



