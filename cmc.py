import aiohttp, os
from dotenv import load_dotenv

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
                try:
                    prices[ticker] = _data_list[0]['quote']['USD']['price']
                except Exception as e:
                    print(f"{ticker} Got an error {str(e)}")
                    prices[ticker] = 0

            return prices



