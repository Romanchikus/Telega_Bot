from xmlrpc.client import ServerProxy
import os
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
import logging
import config as cfg

import time
from time import sleep

import re

regex = re.compile(
    r'^(?:http|ftp)s?://'  # http:// or https://
    # domain...
    r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|'
    r'localhost|'  # localhost...
    r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})'  # ...or ip
    r'(?::\d+)?'  # optional port
    r'(?:/?|[/?]\S+)$', re.IGNORECASE)

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)

token = "875809845:AAHxB49VM_TowQhXtaBz80fx07XrIvgcHIc"

client = ServerProxy(f"http://{cfg.host}:{cfg.port}")
updater = Updater(token=token)
dispatcher = updater.dispatcher
cwd = os.getcwd()


def send_img(update, context):

    chat_id = update.effective_chat.id
    img_name = f"img/{chat_id}_{int(time.time()*1000.0)}.png"

    try:
        url = context.args[0]
    except IndexError:
        url = None
    print(url)

    if not url or not re.match(regex, url):
        context.bot.send_message(chat_id=update.message.chat_id,
                                 text='Send valid link')
    else:

        print(client.hello(url, img_name))

        sleep(15)
        context.bot.send_document(
            chat_id, document=open((cwd + '/' + img_name), 'rb'))


photo_handler = CommandHandler('screen', send_img, run_async=True)
dispatcher.add_handler(photo_handler)


def startCommand(update, context):
    context.bot.send_message(
        chat_id=update.effective_chat.id,  text='Please send link')


def textMessage(update, context):
    context.bot.send_message(chat_id=update.message.chat_id,
                             text=update.message.text)


start_command_handler = CommandHandler('start', startCommand)
dispatcher.add_handler(start_command_handler)

text_message_handler = MessageHandler(
    Filters.text & (~Filters.command), textMessage)
dispatcher.add_handler(text_message_handler)


#  start the bot
updater.start_polling()
#  Ctrl + C
updater.idle()
