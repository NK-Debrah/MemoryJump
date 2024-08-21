Google Calendar Telegram Bot
This is a Python-based Telegram bot that integrates with Google Calendar to help users manage their events and set reminders. The bot can retrieve upcoming events from your Google Calendar and send reminders based on your specified time preferences.

Features
Event Reminders: Set a reminder for a specific number of minutes before an event.
Upcoming Events: Get details of your next upcoming event.
Event Notifications: The bot checks periodically and sends notifications for upcoming events based on your reminders.
Prerequisites
Before you begin, ensure you have the following installed:

Python 3.6+
Pip
A Telegram account and a bot created via BotFather
Google Calendar API enabled and OAuth 2.0 credentials downloaded from the Google Cloud Console
Setup
Clone the repository:

bash
Copy code
git clone https://github.com/yourusername/google-calendar-telegram-bot.git
cd google-calendar-telegram-bot
Install dependencies:

bash
Copy code
pip install -r requirements.txt
Configure environment variables:

Create a .env file in the root directory and add your Telegram bot token:

env
Copy code
BOT_TOKEN=your_telegram_bot_token
Google Calendar API Setup:

Follow the instructions on Google Calendar API Python Quickstart to set up the API.
Download the credentials.json file and place it in the root directory of your project.
Run the bot:

bash
Copy code
python bot.py
The bot will start polling for commands and events.

Available Commands
/start or /hello - Greet the bot and start the interaction.
/help - Get a list of available commands and usage instructions.
/set_reminder <minutes> - Set a reminder for a specified number of minutes before an event.
/upnext - Retrieve and display details of your next upcoming event.
How It Works
The bot uses the Google Calendar API to access your events.
You can set reminders to notify you a certain amount of time before your events.
The bot runs a background thread to check for upcoming events and send notifications if a reminder is set.
Future Enhancements
Create Events: Add functionality to create new events on your Google Calendar directly from the bot.
Event Deletion: Enable event deletion or modification from within the bot.
License
This project is licensed under the MIT License - see the LICENSE file for details.

Contributions & Issues
Feel free to contribute to this project by submitting a pull request or opening an issue for any bugs or feature requests.

