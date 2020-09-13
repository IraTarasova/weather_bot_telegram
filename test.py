import json
from datetime import datetime, timezone, timedelta

from utils import read_secrets
from telegram.ext import Updater, CommandHandler, MessageHandler
import requests


tokens = read_secrets()
token_telegram = tokens['token_telegram']
token_owm = tokens['token_owm']


# def hello(update, context):
#     update.message.reply_text(
#         'Hello {}'.format(update.message.from_user.first_name))
#
#
# def get_current_time(update, context):
#     timezone_mocsow = timezone(timedelta(hours=3))
#     current_time = datetime.now(timezone_mocsow)
#     update.message.reply_text(str(current_time))
#
#
# updater = Updater(token_telegram, use_context=True)
#
# updater.dispatcher.add_handler(CommandHandler('hello', hello))
# updater.dispatcher.add_handler(CommandHandler('current_time', get_current_time))
#
# updater.start_polling()
# updater.idle()



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



