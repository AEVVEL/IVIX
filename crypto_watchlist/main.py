import asyncio
import logging
import sys
import time

from api_parser import start_api_parse
from html_parse import start_html_parse
from csv_tools import save_to_csv


logging.basicConfig(
    filename='crypto.log',
    level=logging.ERROR,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)


def main():
    parse_type = "html"
    pages_to_parse = 5
    coins_info = []

    if len(sys.argv) > 1:
        parse_type = sys.argv[1]

    if len(sys.argv) > 2:
        try:
            pages_to_parse = int(sys.argv[2])
        except ValueError:
            print(f"Invalid pages number: {sys.argv[2]}. Using default: 5")
            pages_to_parse = 5

    total_start_time = time.time()
    if parse_type == "html":
        print(f"Starting HTML parsing for {pages_to_parse} pages...")
        coins_info = start_html_parse(pages_to_parse=pages_to_parse)
        formated_coins_info = [coin.model_dump() for coin in coins_info]
        save_to_csv(data=formated_coins_info, filename="crypto_watchlist_html.csv")

    elif parse_type == "api":
        print(f"Starting API parsing for {pages_to_parse} pages...")
        coins_info = asyncio.run(start_api_parse(pages_to_parse=pages_to_parse))
        formated_coins_info = [coin.model_dump() for coin in coins_info]
        save_to_csv(data=formated_coins_info, filename="crypto_watchlist_api.csv")

    else:
        raise ValueError(f"Invalid parse type: {parse_type}. Use 'html' or 'api'")

    total_duration = time.time() - total_start_time
    avg_page_time = total_duration/pages_to_parse

    print("\n" + "=" * 50)
    print(f"Total pages parsed: {pages_to_parse}")
    print(f"Total execution time: {total_duration:.2f} seconds")
    print(f"Average time per page: {avg_page_time:.2f} seconds")
    print(f"Total coins parsed: {len(coins_info)}")
    print("=" * 50)


if __name__ == "__main__":
    main()
