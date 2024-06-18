# tele-bot
that can be used to sync a raw file from GitHub and send updates to the bot. This bot will send a new message every day with the updated raw file.


To run this bot, you'll need to follow these steps:
**Step 1: Install the Required Libraries
**

  Install the python-telegram-bot library using pip:
pip install python-telegram-bot
  


Step 2: Set Up Your Bot
  1. Create a new bot on the Telegram BotFather.
  2. Note the API token provided by the BotFather.

Step 3: Set Up Your GitHub Repository
  1. Create a new GitHub repository.
  2. Add your raw file to the repository.

Step 4: Run the Bot
  1.Create a new Python file (e.g., bot.py) and add the bot code.
  2.Replace 'YOUR_BOT_TOKEN', 'YOUR_GITHUB_REPO', and 'YOUR_GITHUB_RAW_FILE' with your actual bot token and GitHub repository and file information.
  3.Run the bot using the following command:
  python bot.py

Step 5: Use the Bot
  1. Start the bot by sending /start to the bot.
  2. Use the /sync command to sync the raw file from GitHub.


