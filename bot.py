import os
import requests
import logging
import re
from datetime import datetime, timedelta
from telegram.ext import Updater, CommandHandler, MessageHandler

# Set up logging
logging.basicConfig(level=logging.INFO)

# Set up the bot
TOKEN = 'YOUR_BOT_TOKEN'

# Set up the GitHub repository
GITHUB_REPO = 'YOUR_GITHUB_REPO'
GITHUB_RAW_FILE = 'YOUR_GITHUB_RAW_FILE'

# Set up the bot updater
def main():
    updater = Updater(TOKEN, use_context=True)

    # Define the bot's commands
    updater.dispatcher.add_handler(CommandHandler('start', start))
    updater.dispatcher.add_handler(CommandHandler('help', help))
    updater.dispatcher.add_handler(CommandHandler('sync', sync))

    # Start the bot
    updater.start_polling()
    updater.idle()

def start(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text='Hello, I am a Telegram bot. I can help you sync a raw file from GitHub.')

def help(update, context):
    context.bot.send_message(chat_id=update.effective_chat.id, text='I can help you sync a raw file from GitHub. Use the /sync command to sync the file.')

def sync(update, context):
    # Get the raw file from GitHub
    raw_file = requests.get(f'https://raw.githubusercontent.com/{GITHUB_REPO}/{GITHUB_RAW_FILE}').text

    # Check if the first line starts with "vless"
    lines = raw_file.splitlines()
    if lines and lines[0].startswith('vless'):
        # Send the entire raw file to the chat
        context.bot.send_message(chat_id=update.effective_chat.id, text=raw_file)
    else:
        context.bot.send_message(chat_id=update.effective_chat.id, text='The raw file does not start with "vless".')

    # Schedule the bot to send the raw file every day
    schedule.every(1).days.do(sync)  # Send the raw file every day

    # Run the bot
    while True:
        schedule.run_pending()
        time.sleep(1)

if __name__ == '__main__':
    main()
