import logging
from datetime import datetime

import aiohttp
import asyncio

from schemas import Coin

logger = logging.getLogger(__name__)


def format_price_custom(price):
    if isinstance(price, str):
        price = price.replace('$', '').replace(',', '')

    price_float = float(price)
    price_str = f"{price_float:.30f}"

    if price_float < 1:
        parts = price_str.split('.')
        if len(parts) > 1:
            decimal_part = parts[1]

            last_zero_pos = -1

            for i, digit in enumerate(decimal_part):
                if digit == '0':
                    last_zero_pos = i
                else:
                    break

            if last_zero_pos >= 0:
                digits_to_show = last_zero_pos + 1 + 4
                formatted = f"{price_float:.{digits_to_show}f}"
                return f"${formatted}"
            else:
                return f"${price_float:.4f}"

    elif price_float < 1000:
        return f"${price_float:.2f}"
    else:
        return f"${price_float:,.2f}"


async def request_coins_info(start: int, limit: int):
    try:
        api_url = (
            "https://api.coinmarketcap.com/data-api/v3/cryptocurrency/listing"
            f"?start={start}"
            f"&limit={limit}"
            "&sortBy=rank"
            "&sortType=desc"
            "&convert=USD"
            "&cryptoType=all"
            "&tagType=all"
            "&audited=false"
            "&aux=ath,atl,high24h,low24h,num_market_pairs,cmc_rank,date_added,"
            "max_supply,circulating_supply,total_supply,volume_7d,volume_30d,"
            "self_reported_circulating_supply,self_reported_market_cap"
        )
        async with aiohttp.ClientSession() as session:
            async with session.get(api_url) as response:
                if response.status != 200:
                    logger.error(f">>> Error while try to get data from API. Status code: {response.status}")

                coins_info = await response.json()

                return coins_info["data"]["cryptoCurrencyList"]

    except Exception as ex:
        logger.error(f">>> Error while try to get data from API: {ex}")
        return []


async def start_api_parse(pages_to_parse: int):
    parse_task_list = []
    start = 1

    for i in range(pages_to_parse):
        parse_task_list.append(asyncio.ensure_future(request_coins_info(start, 100)))
        start += 100

    tasks_response  = await asyncio.gather(*parse_task_list)
    total_coins_info = [item for sublist in tasks_response for item in sublist]

    formated_coins_info=[]
    for coin in total_coins_info:
        formated_coins_info.append(Coin(
            rank=str(coin["cmcRank"]),
            name=coin["name"],
            symbol=coin["symbol"],
            price=format_price_custom(coin['quotes'][0]['price']),
            day_price_change=f"{coin['quotes'][0]['percentChange24h']:,.2f}%",
            market_cap=f"${coin['quotes'][0]['marketCap']:,.0f}",
            timestamp=datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            parse_type="api"
        ))

    return formated_coins_info
