from telegram.ext import Updater, CommandHandler
from random import randint
import logging
import sys
import os

# enabling logging
logging.basicConfig(level=logging.INFO,
                    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")
logger = logging.getLogger()

MODE = os.getenv('MODE')
TOKEN = os.getenv('BOT_TOKEN')

def wordArt1(bot, update):

    update_id = update['update_id']
    chat_id = update['message']['chat_id']
    
    if update['message']['text'] is not None:
        text = update['message']['text']
        if (len(text) <= 10):
            update.message.reply_text('Escreva uma mensagem ou responda a outra')
            return
        text = text[10:]

    elif update['message']['reply_to_message']['text'] is not None:
        text = update['message']['reply_to_message']['text']
    
    file_path = str(update_id) + '.png'
    os.system('python3 generate_art.py \'' + text + '\' ' + file_path)
    bot.send_photo(chat_id=chat_id, photo=open(file_path, 'rb'))
    os.remove(file_path)

if __name__ == '__main__':

    logger.info("Starting bot")
    updater = Updater(TOKEN)
    
    dp = updater.dispatcher
    dp.add_handler(CommandHandler('wordart1', wordArt1))

    # Code from https://github.com/python-telegram-bot/python-telegram-bot/wiki/Webhooks#heroku
    if MODE == "dev":
        updater.start_polling()
    elif MODE == "prod":
        PORT = int(os.environ.get("PORT", "8443"))
        HEROKU_APP_NAME = os.environ.get("HEROKU_APP_NAME")
        updater.start_webhook(listen="0.0.0.0",
                              port=PORT,
                              url_path=TOKEN)
        updater.bot.set_webhook("https://{}.herokuapp.com/{}".format(HEROKU_APP_NAME, TOKEN))
    else:
        logger.error("ERROR: No MODE specified!")
        sys.exit(1)