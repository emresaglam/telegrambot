from telegram.ext import Updater
from telegram.ext import CommandHandler
from telegram.ext import MessageHandler, Filters
import logging
import os
api_token="APITOKEN"
APITOKEN=os.getenv(api_token)
updater = Updater(token=APITOKEN, use_context=True)
dispatcher = updater.dispatcher
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)

def start(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text="I'm a bot, please talk to me!")

def echo(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text=update.message.text)

def shut_up(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text="Shut up Oktay")

start_handler = CommandHandler('start', start)
dispatcher.add_handler(start_handler)
updater.start_polling()
echo_handler = MessageHandler(Filters.text & (~Filters.command), echo)
dispatcher.add_handler(echo_handler)

oktay_handler = CommandHandler('oktay', shut_up)
dispatcher.add_handler(oktay_handler)
