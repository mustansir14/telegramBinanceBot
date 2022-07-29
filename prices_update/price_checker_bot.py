from binance import Client
from regex import P
from config import *
import requests
import time
import logging
logging.basicConfig(format='%(asctime)s %(message)s', datefmt='%m/%d/%Y %H:%M:%S', level=logging.INFO)

def send_message(message, bot_token, chat_ids):

    responses = []
    for chat_id in chat_ids: 
        responses.append(requests.post(f"https://api.telegram.org/bot{bot_token}/sendMessage", data={"chat_id": chat_id, "text":message}))
    return responses

client = Client()
previous_prices = client.get_all_tickers()

counts_for_24_hours = 86400 / TIME_INTERVAL
counts_dict = {}
while True:
    time.sleep(TIME_INTERVAL)
    logging.info("Checking Prices...")
    new_prices = client.get_all_tickers()
    for previous_ticker in previous_prices:
        previous_symbol = previous_ticker["symbol"]
        if previous_symbol in counts_dict and counts_dict[previous_symbol] < counts_for_24_hours:
            counts_dict[previous_symbol] += 1
            continue
        previous_price = float(previous_ticker["price"])
        for new_ticker in new_prices:
            if new_ticker["symbol"] == previous_symbol:
                new_price = float(new_ticker["price"])
                if new_price >= 1.04*previous_price:
                    message = "Price Update\n\n%s is up %s in the last 30 minutes. Now at %s" % (previous_symbol, str(round(((new_price / previous_price) - 1)*100, 2)) + '%', new_price)
                    send_message(message, TELEGRAM_BOT_TOKEN, CHAT_IDS)
                    counts_dict[previous_symbol] = 0
                break

    previous_prices = new_prices
