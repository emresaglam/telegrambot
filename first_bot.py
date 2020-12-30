from telegram.ext import Updater
from telegram.ext import CommandHandler
from telegram.ext import MessageHandler, Filters
import logging
import os
import requests


def start(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text="I'm a bot, please talk to me!"
                                                                    "\n"
                                                                    "Some commands you can use:\n"
                                                                    "/kitty\n"
                                                                    "/start\n"
                                                                    "Secret command: /oktay")


def echo(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text=update.message.text)


def shut_up(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text="Shut up Oktay")


def grab_a_kitten(update, context):
    catapi_token = "CATAPITOKEN"
    CATAPITOKEN = os.getenv(catapi_token)
    if CATAPITOKEN is None:
        print("EEK! Define CATAPITOKEN first. 😹")
    fn = "/tmp/kitty.jpg"
    kittyurl = "https://api.thecatapi.com/v1/images/search?limit=1&page=10&order=random"
    r = requests.get(kittyurl)
    kittypicurl=r.json()[0]["url"]
    headers = {"x-api-key": CATAPITOKEN}
    r = requests.get(kittypicurl, headers=headers)
    f = open(fn, "wb")
    r.raw.decode_content = True
    for chunk in r:
        f.write(chunk)
    f.close()
    context.bot.send_photo(chat_id=update.effective_chat.id, photo=open(fn, 'rb'))
    os.remove(fn)


if __name__ == "__main__":
    api_token = "APITOKEN"
    APITOKEN = os.getenv(api_token)
    if APITOKEN is None:
        exit("EEK! Define APITOKEN first.")
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
    # TODO: Add a function to iterate through added handlers. 

    updater.start_polling()
