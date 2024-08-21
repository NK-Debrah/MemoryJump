# Google Calendar Telegram Bot

This Telegram bot integrates with Google Calendar to help users manage their events and set reminders. It allows users to check their upcoming events and set custom reminders through a simple chat interface.

## Features

- View the next upcoming event from your Google Calendar
- Set custom reminders for events
- Receive notifications before events based on your preferences

## Commands

- `/start` or `/hello`: Greet the bot and start the interaction
- `/help`: Display help information and available commands
- `/set_reminder <minutes>`: Set a reminder for a specified number of minutes before events
- `/upnext`: Show your next upcoming event

## Setup

1. Clone this repository
2. Install the required dependencies: `pip install python-dotenv python-telegram-bot google-auth-oauthlib google-auth-httplib2 google-api-python-client`
3. Set up a Telegram bot and obtain the bot token from BotFather
4. Create a Google Cloud project and enable the Google Calendar API
5. Download the `credentials.json` file for your Google Cloud project
6. Create a `.env` file in the project root and add your Telegram bot token: `BOT_TOKEN=your_telegram_bot_token_here`
7. Run the script: `python bot.py`


## Authentication

On first run, you'll need to authenticate with your Google account. The script will open a browser window for you to complete the OAuth2 flow. After successful authentication, a `token.json` file will be created to store your credentials.

## Note

This bot uses the `google-auth-oauthlib` library, which requires a local server for the OAuth2 flow. The server runs on port 8080 by default.

## Contributing

Feel free to fork this repository and submit pull requests with any improvements or bug fixes.

