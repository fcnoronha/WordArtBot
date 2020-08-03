from telegram.ext import Updater, CommandHandler
from pythonWordArt import pyWordArt
from random import randint
import logging
import sys
import os


# enabling logging
logging.basicConfig(level=logging.INFO,
                    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")
logger = logging.getLogger()

mode = os.getenv('MODE')
TOKEN = os.getenv('BOT_TOKEN')

if mode == "dev":
    def run(updater):
        updater.start_polling()
elif mode == "prod":
    def run(updater):
        PORT = int(os.environ.get("PORT", "8443"))
        HEROKU_APP_NAME = os.environ.get("HEROKU_APP_NAME")
        # Code from https://github.com/python-telegram-bot/python-telegram-bot/wiki/Webhooks#heroku
        updater.start_webhook(listen="0.0.0.0",
                              port=PORT,
                              url_path=TOKEN)
        updater.bot.set_webhook("https://{}.herokuapp.com/{}".format(HEROKU_APP_NAME, TOKEN))
else:
    logger.error("No MODE specified!")
    sys.exit(1)

def generate_art(text, fila_path):
    
    # There are 30 available WordArt styles
    style = randint(0, 29)

    w = pyWordArt()
    w.transparentBackground = True
    w.WordArt(text, style, 100)
    w.toFile(fila_path)

def wordArt1(bot, update):

    update_id = update['update_id']
    chat_id = update.message.chat_id
    text = update.message.text

    #bot.send_video(chat_id=chat_id, video='https://random.dog/e03b1dce-fe0c-4d47-a208-8f7c2a9ff57f.mp4')
    if (len(text) > 10):
        text = text[10:]
        #print(text)
        file_path = str(update_id) + '.png'
        #os.system('python3 generate_art.py \'' + text + '\' ' + file_path)
        bot.send_photo(chat_id=chat_id, photo=open('not-yet.png', 'rb'))
        #bot.send_photo(chat_id=chat_id, photo=open(file_path, 'rb'))
        #os.remove(file_path)

if __name__ == '__main__':

    logger.info("Starting bot")
    updater = Updater(TOKEN)
    
    dp = updater.dispatcher
    dp.add_handler(CommandHandler('wordart1', wordArt1))

    run(updater)