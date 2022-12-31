from celery import shared_task
import redis
import requests
import json

from django.conf import settings
from .currency_convert import key

def get_rate():
    """Get exchange rate from exchange rate API"""

    url = "http://api.coincap.io/v2/assets/bitcoin"

    try:
        btc_to_usd = json.loads(requests.request("GET", url).text)["data"]["priceUsd"]
        return btc_to_usd
    except:
        return None

@shared_task
def update_currency_exchange_rate():
    """Task to update currency conversion rate used in app"""

    r = redis.Redis(
        host=settings.REDIS_HOST,
        port=settings.REDIS_PORT,
        db=settings.REDIS_DB
    )

    btc_to_usd = get_rate()

    if btc_to_usd:
        r.set(key, float(btc_to_usd))