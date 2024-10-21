from telegram import Bot
from config import BOT_TOKEN
import logging

logger = logging.getLogger(__name__)

SENT_ADS_FILE = "sent_ads.txt"
USERS_FILE = "users.txt"

def load_sent_ads():
    try:
        with open(SENT_ADS_FILE, "r") as f:
            return set(line.strip() for line in f)
    except FileNotFoundError:
        return set()

def save_sent_ads(sent_ads):
    with open(SENT_ADS_FILE, "w") as f:
        for ad in sent_ads:
            f.write(ad + "\n")

def load_users():
    try:
        with open(USERS_FILE, "r") as f:
            return set(line.strip() for line in f)
    except FileNotFoundError:
        return set()

def handle_start_command(chat_id):
    users = load_users()
    users.add(str(chat_id))
    with open(USERS_FILE, "w") as f:
        for user in users:
            f.write(f"{user}\n")
    logger.info(f"User {chat_id} saved to {USERS_FILE}")

def send_telegram_message(message, specific_users=None):
    bot = Bot(BOT_TOKEN)
    users = specific_users if specific_users else load_users()
    for chat_id in users:
        try:
            bot.send_message(chat_id=int(chat_id), text=message)
        except Exception as e:
            logger.error(f"Message could not be sent to {chat_id}: {e}")