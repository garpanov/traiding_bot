from httpx import AsyncClient
import time
import base64
import urllib
from cryptography.hazmat.primitives.serialization import load_pem_private_key
import os

import models_pd
from dotenv import load_dotenv
load_dotenv()

url = "https://api.binance.com"
API_KEY = os.getenv("BINANCE_API_KEY")
API_PRIVATE = os.getenv("BINANCE_PRIVATE_KEY")

timestamp = int(time.time() * 1000)
params = {
    "timestamp": timestamp
}

private_key = load_pem_private_key(API_PRIVATE.encode('utf-8'), password=None)
payload = urllib.parse.urlencode(params, encoding='UTF-8')
signature = base64.b64encode(private_key.sign(payload.encode('ASCII'))).decode("utf-8")
params['signature'] = signature

headers = {
    'X-MBX-APIKEY': API_KEY,
}

async def info_user_query():
    async with AsyncClient() as client:
        response = await client.get(f'{url}/api/v3/account', headers=headers, params=params)
        print(response.json())

