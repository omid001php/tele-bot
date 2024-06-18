import requests
from telegram import Bot, Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import CallbackContext, CommandHandler, CallbackQueryHandler

# Replace 'YOUR_BOT_TOKEN' with your Telegram bot token
bot = Bot(token='YOUR_BOT_TOKEN')

# Replace 'YOUR_GITHUB_USERNAME' with your GitHub username
github_username = 'YOUR_GITHUB_USERNAME'
repository_name = 'YOUR_REPOSITORY_NAME'

def get_raw_file_from_github(file_path):
    url = f'https://raw.githubusercontent.com/{github_username}/{repository_name}/master/{file_path}'
    response = requests.get(url)
    if response.status_code == 200:
        return response.text
    else:
        return None

def send_raw_file_to_telegram(chat_id, lines):
    message = '\n'.join(lines)
    bot.send_message(chat_id=chat_id, text=message)

def start(update: Update, context: CallbackContext):
    keyboard = [
        [InlineKeyboardButton("Set Keyword", callback_data='set_keyword')],
        [InlineKeyboardButton("Set Line Count", callback_data='set_line_count')],
        [InlineKeyboardButton("Get Daily Updates", callback_data='daily_updates')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    update.message.reply_text('Please choose an option:', reply_markup=reply_markup)

def button_callback(update: Update, context: CallbackContext):
    query = update.callback_query
    if query.data == 'set_keyword':
        query.message.reply_text('Please enter the keyword:')
        return 'wait_for_keyword'
    elif query.data == 'set_line_count':
        query.message.reply_text('Please enter the number of lines to be sent:')
        return 'wait_for_line_count'
    elif query.data == 'daily_updates':
        query.message.reply_text('You will receive daily updates of the specified number of lines.')
        return 'daily_updates'

def handle_keyword(update: Update, context: CallbackContext):
    keyword = update.message.text
    context.user_data['keyword'] = keyword
    update.message.reply_text(f'Keyword set to: {keyword}')
    return 'daily_updates'

def handle_line_count(update: Update, context: CallbackContext):
    line_count = int(update.message.text)
    context.user_data['line_count'] = line_count
    update.message.reply_text(f'Line count set to: {line_count}')
    return 'daily_updates'

def daily_update_job(context: CallbackContext):
    chat_id = context.job.context
    keyword = context.user_data.get('keyword')
    line_count = context.user_data.get('line_count')
    file_path = 'path/to/raw/file.txt'  # Replace with the path to your raw file

    raw_file = get_raw_file_from_github(file_path)
    if raw_file:
        lines = raw_file.split('\n')
        filtered_lines = [line for line in lines if line.startswith(keyword)]
        if filtered_lines:
            lines_to_send = filtered_lines[:line_count]
            send_raw_file_to_telegram(chat_id, lines_to_send)
        else:
            bot.send_message(chat_id=chat_id, text=f"No lines found starting with '{keyword}' today.")

def main():
    # Replace 'YOUR_BOT_TOKEN' with your Telegram bot token
    updater = Updater(token='YOUR_BOT_TOKEN', use_context=True)
    dispatcher = updater.dispatcher

    # Add command handlers
    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(CallbackQueryHandler(button_callback))

    # Add conversation handlers
    conversation_handler = ConversationHandler(
        entry_points=[CallbackQueryHandler(button_callback)],
        states={
            'wait_for_keyword': [MessageHandler(Filters.text & ~Filters.command, handle_keyword)],
            'wait_for_line_count': [MessageHandler(Filters.text & ~Filters.command, handle_line_count)]
        },
        fallbacks=[CommandHandler('cancel', cancel)]
    )
    dispatcher.add_handler(conversation_handler)

    # Schedule the daily update job
    job_queue = updater.job_queue
    chat_id = 'YOUR_CHAT_ID'  # Replace with your Telegram chat ID
    job_queue.run_daily(daily_update_job, time=datetime.time(hour=12), context=chat_id)

    # Start the bot
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()
