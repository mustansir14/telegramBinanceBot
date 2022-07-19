from binance.client import Client
import time
from config import *
import requests
import logging
logging.basicConfig(format='%(asctime)s %(message)s', datefmt='%m/%d/%Y %H:%M:%S', level=logging.INFO)

def send_message(message, bot_token, chat_ids):

    responses = []
    for chat_id in chat_ids: 
        responses.append(requests.post(f"https://api.telegram.org/bot{bot_token}/sendMessage", data={"chat_id": chat_id, "text":message}))
    return responses

client = Client()

exchange_info = client.get_exchange_info()
previous_trading_pairs = [s["symbol"] for s in exchange_info['symbols']]

while True:
    time.sleep(TIME_INTERVAL)
    exchange_info = client.get_exchange_info()
    trading_pairs = [s["symbol"] for s in exchange_info['symbols']]
    new_pairs = list(set(trading_pairs) - set(previous_trading_pairs))
    if new_pairs:
        for pair in new_pairs:
            send_message(pair + " - new pair listing", TELEGRAM_BOT_TOKEN, CHAT_IDS)
    else:
        logging.info("No new pairs")
    previous_trading_pairs = trading_pairs