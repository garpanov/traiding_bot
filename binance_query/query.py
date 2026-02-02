from httpx import AsyncClient
import time
import base64
import urllib
from cryptography.hazmat.primitives.serialization import load_pem_private_key

from security import decrypt_data
import models_pd
from dotenv import load_dotenv
load_dotenv()

url = "https://api.binance.com"

def create_params_headers(params: dict, api_key: str, api_private: str):
    timestamp = int(time.time() * 1000)
    params["timestamp"] = timestamp

    private_key = load_pem_private_key(api_private.encode('utf-8'), password=None)
    payload = urllib.parse.urlencode(params, encoding='UTF-8')
    signature = base64.b64encode(private_key.sign(payload.encode('ASCII'))).decode("utf-8")
    params['signature'] = signature

    headers = {
        'X-MBX-APIKEY': api_key,
    }

    return params, headers


async def info_user_query(data: models_pd.InfoUser):
    try:
        keys = decrypt_data(nonce_api=data.nonce_api, cipher_api=data.api_key, nonce_secret=data.nonce_secret, cipher_secret=data.api_private)
        API_KEY = keys["api_key"]
        API_PRIVATE = keys["secret_key"]

        params, headers = create_params_headers(params={}, api_key=API_KEY, api_private=API_PRIVATE)
        async with AsyncClient() as client:
            response = await client.get(f'{url}/api/v3/account', headers=headers, params=params)

        return {"status": True, "data": response.json()}

    except Exception as e:
        return {"status": False, "error": "Sorry, unknown error (please check your keys and try again)"}


async def buy_crypto_query(data: models_pd.BuyCrypto):
    try:
        keys = decrypt_data(nonce_api=data.nonce_api, cipher_api=data.api_key, nonce_secret=data.nonce_secret, cipher_secret=data.api_private)
        API_KEY = keys["api_key"]
        API_PRIVATE = keys["secret_key"]

        params_base = {
            "symbol": data.currency,
            "type": "MARKET",
            "side": "BUY",
            "quoteOrderQty": data.count_usdt
        }

        params, headers = create_params_headers(params=params_base, api_key=API_KEY, api_private=API_PRIVATE)

        async with AsyncClient() as client:
            response = await client.post(f'{url}/api/v3/order', headers=headers, params=params)
            response = response.json()
            commission_usdt = float(response["fills"][0]["price"]) * float(response["fills"][0]["commission"])
            good_data = {"symbol": response["symbol"], "value_usdt": response["cummulativeQuoteQty"],
                         "price_usdt": response["fills"][0]["price"], "quantity_crypto": response["fills"][0]["qty"],
                         "commission_crypto": response["fills"][0]["commission"], "commission_usdt": commission_usdt}


        return {"status": True, "data": good_data}
    except Exception as e:
        return {"status": False, "error": str(e), "code_error": str(e)}

async def sell_crypto_query(data: models_pd.SellCrypto):
    try:
        keys = decrypt_data(nonce_api=data.nonce_api, cipher_api=data.api_key, nonce_secret=data.nonce_secret, cipher_secret=data.api_private)
        API_KEY = keys["api_key"]
        API_PRIVATE = keys["secret_key"]

        params_base = {
            "symbol": data.currency,
            "type": "MARKET",
            "side": "SELL",
            "quantity": data.count_curr
        }

        params, headers = create_params_headers(params=params_base, api_key=API_KEY, api_private=API_PRIVATE)

        async with AsyncClient() as client:
            response = await client.post(f'{url}/api/v3/order', headers=headers, params=params)
            response = response.json()



        return {"status": True, "data": response}
    except Exception as e:
        return {"status": False, "error": str(e), "code_error": str(e)}
