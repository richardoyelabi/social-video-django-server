from django.conf import settings

import redis
from decimal import Decimal

key = "transactions_btc_to_usd_rate"


def convert_currency(source, target, amount):
    """Convert between currencies (btc and usd)"""

    if source == target:
        return amount

    r = redis.Redis(
        host=settings.REDIS_HOST, port=settings.REDIS_PORT, db=settings.REDIS_DB
    )

    btc_to_usd = r.get(key)

    from .tasks import update_currency_exchange_rate

    while btc_to_usd == None:
        update_currency_exchange_rate()
        btc_to_usd = r.get(key)

    btc_to_usd = Decimal(float(btc_to_usd))

    if source == "btc" and target == "usd":
        ret = amount * btc_to_usd
    elif source == "usd" and target == "btc":
        ret = amount / btc_to_usd
    else:
        raise ValueError("Source and target currencies combination is invalid")

    return ret
