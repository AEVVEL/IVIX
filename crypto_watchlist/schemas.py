from datetime import datetime

from pydantic import BaseModel


class Coin(BaseModel):
    rank: str
    name: str
    symbol: str
    price: str
    day_price_change: str
    market_cap: str
    parse_type: str
    timestamp: str