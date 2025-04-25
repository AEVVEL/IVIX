import threading
import signal
from time import sleep
from datetime import datetime
import logging

import requests

from config import INITIAL_BACKOFF


class GracefulShutdown:
    def __init__(self):
        self.shutdown_flag = threading.Event()
        signal.signal(signal.SIGINT, self.request_shutdown)
        signal.signal(signal.SIGTERM, self.request_shutdown)

    def request_shutdown(self, *args):
        print('\nShutting down…')
        self.shutdown_flag.set()

    def should_continue(self):
        return not self.shutdown_flag.is_set()


shutdown = GracefulShutdown()
logging.basicConfig(
    filename='price_pulse.log',
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


def send_request(url):
    try:
        return requests.get(url)

    except requests.exceptions.RequestException as ex:
        return ex


def polling(backoff: int, target_url: str, is_success: bool, history: list):
    if not shutdown.should_continue():
        return True

    if not is_success:
        if backoff >= pow(2, 4):
            logger.warning(f"Polling failed. Backoff {backoff} applied")

        sleep(backoff)
        backoff *= 2

    response = send_request(target_url)
    if type(response) != requests.Response:
        return polling(backoff, target_url, False, history)

    if response.status_code != 200:
        return polling(backoff, target_url, False, history)

    btc_info = response.json()["bitcoin"]
    btc_datetime = datetime.fromtimestamp(btc_info['last_updated_at'])
    formated_btc_datetime = btc_datetime.strftime("%Y-%m-%dT%H:%M:%S")
    btc_price: float = btc_info['usd']

    if len(history) == 10:
        history.pop(0)
    history.append(btc_price)
    sma = sum(history)/len(history)

    print(f"[{formated_btc_datetime}] BTC → USD: ${btc_price:,.2f} | SMA({len(history)}): ${sma:,.2f}")
    sleep(INITIAL_BACKOFF)

    return polling(INITIAL_BACKOFF, target_url, True, history)


def main():
    target_url = "https://api.coingecko.com/api/v3/simple/price?ids=bitcoin&vs_currencies=usd&include_last_updated_at=true"

    polling(INITIAL_BACKOFF, target_url, True, [])


if __name__ == "__main__":
    main()
