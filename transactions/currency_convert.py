from decimal import Decimal

def convert_currency(source, target, amount):
    """Convert between currencies (btc and usd)"""

    if source==target:
        return amount

    btc_to_usd = 17000
    btc_to_usd = Decimal(17000)

    if source=="btc" and target=="usd":
        ret = amount * btc_to_usd
    elif source=="usd" and target=="btc":
        ret = amount / btc_to_usd
    else:
        raise ValueError("Source and target currencies combination is invalid")

    return ret
