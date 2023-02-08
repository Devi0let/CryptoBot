from pycoingecko import CoinGeckoAPI

api = CoinGeckoAPI()


async def crypto_price(coin):
    try:
        price = api.get_price(ids=coin.lower(), vs_currencies='rub')[coin.lower()]['rub']
        return price
    except Exception:
        return None
