import asyncio, aiohttp, os
from dotenv import load_dotenv
from pprint import pprint

load_dotenv()

API = os.getenv('cmc_api')
cmc_base_url = "https://pro-api.coinmarketcap.com"
latest_data = "/v2/cryptocurrency/quotes/latest"
headers = { "X-CMC_PRO_API_KEY" : API, "Accept": "application/json"}

async def get_data(ticker_list : list) :

    async with aiohttp.ClientSession() as session:
        async with session.get(f'{cmc_base_url}{latest_data}?symbol={",".join(ticker_list)}' , headers = headers) as response:
            res = await response.json()
            data = res['data'] 
            prices = {}
            for ticker,_data_list in data.items():
                prices[ticker] = _data_list[0]['quote']['USD']['price']

            return prices


asyncio.run(get_data(['BTC','ETH']))

