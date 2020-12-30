from telegram.ext import Updater
from telegram.ext import CommandHandler
from telegram.ext import MessageHandler, Filters
import logging
import os
import requests


def start(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text="I'm a bot, please talk to me!")


def echo(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text=update.message.text)


def shut_up(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text="Shut up Oktay")


def grab_a_kitten(update, context):
    fn="/tmp/kitty.jpg"
    kittyurl = "http://placekitten.com/200/300"
    r = requests.get(kittyurl)
    f = open(fn, "wb")
    r.raw.decode_content = True
    for chunk in r:
        f.write(chunk)
    f.close()
    context.bot.send_photo(chat_id=update.effective_chat.id, photo=open(fn, 'rb'))
    os.remove(fn)

api_token = "APITOKEN"
APITOKEN = os.getenv(api_token)
updater = Updater(token=APITOKEN, use_context=True)
dispatcher = updater.dispatcher
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)


start_handler = CommandHandler('start', start)
dispatcher.add_handler(start_handler)
oktay_handler = CommandHandler('oktay', shut_up)
dispatcher.add_handler(oktay_handler)
kitty_handler = CommandHandler('kitty', grab_a_kitten)
dispatcher.add_handler(kitty_handler)

echo_handler = MessageHandler(Filters.text & (~Filters.command), echo)
dispatcher.add_handler(echo_handler)


updater.start_polling()
