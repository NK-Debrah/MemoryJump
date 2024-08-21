import os
from dotenv import load_dotenv
import datetime
import os.path
import time
import threading

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

import telebot
load_dotenv()

# If modifying these scopes, delete the file token.json.
SCOPES = ["https://www.googleapis.com/auth/calendar.readonly"]

BOT_TOKEN = os.getenv('BOT_TOKEN')
bot = telebot.TeleBot(BOT_TOKEN)

reminders = {}  # Dictionary to store user reminder preferences

print(BOT_TOKEN)

@bot.message_handler(commands=['start', 'hello'])
def send_welcome(message):
    bot.reply_to(message, "Howdy, how are you doing? type /help for more info")

@bot.message_handler(commands=['help'])
def send_help(message):
    help_text = (
        "I can help you manage your Google Calendar events and set reminders. Here are the available commands:\n\n"
        "/start, /hello - Greet the bot and start the interaction.\n"
        "/help - Display this help message.\n"
        "/set_reminder <minutes> - Set a reminder for a certain number of minutes before an event.\n"
        "/upnext - Show your next upcoming event.\n\n"
        "Example usage:\n"
        "`/set_reminder 30` - Set a reminder for 30 minutes before your events."
    )
    bot.reply_to(message, help_text)

@bot.message_handler(commands=['set_reminder'])
def set_reminder(message):
    try:
        time_before_event = int(message.text.split()[1])
        reminders[message.chat.id] = time_before_event
        bot.reply_to(message, f"Reminder set for {time_before_event} minutes before events.")
    except (IndexError, ValueError):
        bot.reply_to(message, "Please use the command in the format: /set_reminder <minutes>")

@bot.message_handler(commands=['upnext'])
def upnext(message):
    creds = None
    if os.path.exists("token.json"):
        creds = Credentials.from_authorized_user_file("token.json", SCOPES)
    
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                "credentials.json", SCOPES
            )
            creds = flow.run_local_server(port=8080)  # Fixed port 8080
        with open("token.json", "w") as token:
            token.write(creds.to_json())

    try:
        service = build("calendar", "v3", credentials=creds)
        now = datetime.datetime.utcnow().isoformat() + "Z"
        events_result = (
            service.events()
            .list(
                calendarId="primary",
                timeMin=now,
                maxResults=1,  # Only get the next upcoming event
                singleEvents=True,
                orderBy="startTime",
            )
            .execute()
        )
        events = events_result.get("items", [])

        if not events:
            bot.reply_to(message, "No upcoming events found.")
            return

        event = events[0]
        start = event["start"].get("dateTime", event["start"].get("date"))
        event_time = datetime.datetime.fromisoformat(start)
        bot.reply_to(
            message, 
            f"Your next event is '{event['summary']}' at {event_time.strftime('%Y-%m-%d %H:%M:%S')}"
        )

    except HttpError as error:
        print(f"An error occurred: {error}")
        bot.reply_to(message, "Sorry, I couldn't retrieve your next event.")

def check_events():
    while True:
        for chat_id, reminder_time in reminders.items():
            notify_upcoming_events(chat_id, reminder_time)
        time.sleep(60)  # Check every minute

def notify_upcoming_events(chat_id, reminder_time):
    creds = None
    if os.path.exists("token.json"):
        creds = Credentials.from_authorized_user_file("token.json", SCOPES)
    
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                "credentials.json", SCOPES
            )
            creds = flow.run_local_server(port=8080)  # Fixed port 8080
        with open("token.json", "w") as token:
            token.write(creds.to_json())

    try:
        service = build("calendar", "v3", credentials=creds)
        now = datetime.datetime.utcnow().isoformat() + "Z"
        events_result = (
            service.events()
            .list(
                calendarId="primary",
                timeMin=now,
                maxResults=10,
                singleEvents=True,
                orderBy="startTime",
            )
            .execute()
        )
        events = events_result.get("items", [])

        if not events:
            return

        for event in events:
            start = event["start"].get("dateTime", event["start"].get("date"))
            event_time = datetime.datetime.fromisoformat(start)
            time_until_event = (event_time - datetime.datetime.utcnow()).total_seconds() / 60

            if 0 < time_until_event <= reminder_time:
                bot.send_message(chat_id, f"Reminder: Upcoming event '{event['summary']}' at {event_time.strftime('%Y-%m-%d %H:%M:%S')}")

    except HttpError as error:
        print(f"An error occurred: {error}")

# Start the thread that checks events
threading.Thread(target=check_events).start()

bot.infinity_polling()
