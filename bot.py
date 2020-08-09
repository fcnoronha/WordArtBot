from telegram.ext import Updater, CommandHandler, Filters, MessageHandler
from random import randint
import logging
import sys
import os

TOKEN = os.getenv('BOT_TOKEN')
MODE = os.getenv('MODE')
PORT = int(os.environ.get("PORT", "8443"))
HEROKU_APP_NAME = os.environ.get("HEROKU_APP_NAME")

# enabling logging for error handling
logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s")

def start(update, context):
    context.bot.send_message(
        chat_id=update.effective_chat.id, 
        text='Hello! I am a bot that will generate amazing WordArts for you! '
             'To see available commands type /help.')

def help(update, context):
    context.bot.send_message(
        chat_id=update.effective_chat.id, 
        parse_mode='MarkdownV2',
        disable_web_page_preview=True,
        text='To geneate an WordArt you have the following options:\n\n'
             '\- Forward some text message to @bestWordArtBot\n'
             '\- Answer to a massage with the /wordart command\n'
             '\- Write the desired text right after /wordart\n\n'
             'You can also use the /raibow command instead of the /wordart\. \n'
             'Visit me on [GitHub](https://github.com/mrfelipenoronha/WordArtBot)\.')

def unknown(update, context):
    context.bot.send_message(
        chat_id=update.effective_chat.id, 
        text="Sorry, I didn't understand that command, type /help for help.")

def wordArt(update, context, is_rainbow=''):
    update_id = update['update_id']
    file_path = str(update_id) + '.png'
    chat_id = update['message']['chat_id']
    # get text from reply
    if update['message']['reply_to_message'] is not None:
        text = update['message']['reply_to_message']['text']
    else:
        # get forwarded text
        text = update['message']['text']
        # get command out if it is not forwarded
        if update['message']['forward_from'] is None:
            text = text[8:]
            if len(text) == 0:
                return help(update, context)
        # generate ww only if its not forwarded inside group
        elif update['message']['chat']['type'] == 'group':
            return

    if len(text) > 20:
        context.bot.send_message(
        chat_id=update.effective_chat.id, 
        text='Hello! This message is too big maximum length is 20.')
        return

    logging.getLogger().log(
        level=logging.INFO, 
        msg='Message received, generating wordart')

    os.system('python3 generate_art.py \'' + text + '\' ' + file_path + is_rainbow)
    context.bot.send_photo(chat_id=chat_id, photo=open(file_path, 'rb'))
    os.remove(file_path)

def rainbow(update, context):
    return wordArt(update, context, ' 1')

if __name__ == '__main__':
    logging.getLogger().info("Starting bot")

    # responsible for receiving messages from Telegram
    updater = Updater(TOKEN, use_context=True)
    
    # defining available bot commands
    dp = updater.dispatcher
    dp.add_handler(CommandHandler('start', start))
    dp.add_handler(CommandHandler('help', help))
    dp.add_handler(CommandHandler('wordart', wordArt))
    dp.add_handler(CommandHandler('rainbow', rainbow))
    dp.add_handler(MessageHandler(Filters.forwarded & Filters.text, wordArt))
    dp.add_handler(MessageHandler(Filters.command, unknown))

    # differrent deploy modes for develepment and heroku
    if MODE == "dev":
        updater.start_polling()
    elif MODE == "prod":
        updater.start_webhook(listen="0.0.0.0",
                              port=PORT,
                              url_path=TOKEN)
        updater.bot.set_webhook(
            "https://{}.herokuapp.com/{}".format(HEROKU_APP_NAME, TOKEN))
    else:
        logger.error("ERROR: No MODE specified!")
        sys.exit(1)