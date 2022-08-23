import time
from config import *
import requests
from telethon.sync import TelegramClient
import time
import logging
logging.basicConfig(format='%(asctime)s %(message)s', datefmt='%m/%d/%Y %H:%M:%S', level=logging.INFO)

def send_message(message, bot_token, chat_ids):

    responses = []
    for chat_id in chat_ids: 
        responses.append(requests.post(f"https://api.telegram.org/bot{bot_token}/sendMessage", data={"chat_id": chat_id, "text":message}))
    return responses

KEYWORDS = ["list","listing", "rebrand","rebranding","Launchpool","trading will open","will open trading","will list","open trading"]

def contains_keyword(text):
    text = text.lower()
    for keyword in KEYWORDS:
        if keyword.lower() in text:
            return True
    return False

if __name__ == "__main__":

    client = TelegramClient("Binance Updates Fetcher", API_ID, API_HASH)

    min_id = MIN_MESSAGE_ID
    while True:
        logging.info("Connecting with API...")
        client.start("+923333487952")
        logging.info("Connected.")
        channel = client.get_entity("binance_announcements")
        messages = client.get_messages(channel, min_id=min_id, limit=100)
        messages.reverse()
        logging.info("Got messages!")
        for message in messages:
            if contains_keyword(message.text):
                logging.info("Found new message matching keyword.")
                logging.info(message.text)
                responses = send_message(message.text, TELEGRAM_BOT_TOKEN, CHAT_IDS)
            min_id = message.id
        logging.info("Disconnecting with API...")
        client.disconnect()
        logging.info(f"Sleeping for {TIME_INTERVAL} seconds...")
        time.sleep(TIME_INTERVAL)




    