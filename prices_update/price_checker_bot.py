from binance import Client
from regex import P
from config import *
import requests
import time, json, os, sys
import logging
logging.basicConfig(format='%(asctime)s %(message)s', datefmt='%m/%d/%Y %H:%M:%S', level=logging.INFO)

def send_message(message, bot_token, chat_ids):

    responses = []
    for chat_id in chat_ids: 
        responses.append(requests.post(f"https://api.telegram.org/bot{bot_token}/sendMessage", data={"chat_id": chat_id, "text":message}))
    return responses

client = Client()

counts_for_24_hours = 86400 / TIME_INTERVAL
if os.path.isfile("data.json"):
    with open("data.json", "r") as f:
        data = json.load(f)
        previous_prices = data["previous_prices"]
        # counts_dict = data["counts_dict"]
else:
    # counts_dict = {}
    previous_prices = client.get_all_tickers()
    # data = {"counts_dict": counts_dict, "previous_prices": previous_prices}
    data = {"previous_prices": previous_prices}
    with open("data.json", "w") as f:
        json.dump(data, f)
    sys.exit(0)
    

logging.info("Checking Prices...")
new_prices = client.get_all_tickers()
for previous_ticker in previous_prices:
    previous_symbol = previous_ticker["symbol"]
    if "BUSD" not in previous_symbol:
        continue 
    # if previous_symbol in counts_dict and counts_dict[previous_symbol] < counts_for_24_hours:
    #     counts_dict[previous_symbol] += 1
    #     continue
    previous_price = float(previous_ticker["price"])
    for new_ticker in new_prices:
        if new_ticker["symbol"] == previous_symbol:
            new_price = float(new_ticker["price"])
            if new_price >= 1.04*previous_price:
                if "e" in str(new_price):
                    new_price_str = f'{new_price:.8f}'
                else:
                    new_price_str = str(new_price)
                message = "Price Update\n\n%s is up %s in the last 30 minutes. Now at %s" % (previous_symbol, str(round(((new_price / previous_price) - 1)*100, 2)) + '%', new_price_str)
                logging.info(message)
                send_message(message, TELEGRAM_BOT_TOKEN, CHAT_IDS)
                # counts_dict[previous_symbol] = 0
            break

# data = {"counts_dict": counts_dict, "previous_prices": new_prices}
data = {"previous_prices": new_prices}
with open("data.json", "w") as f:
    json.dump(data, f)
