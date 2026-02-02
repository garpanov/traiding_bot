from fastapi import FastAPI

from query import info_user_query, buy_crypto_query, sell_crypto_query
import models_pd
app = FastAPI()

@app.post("/info_user")
async def info_user(data: models_pd.InfoUser):
    result = await info_user_query(data)
    return result

@app.post("/buy_crypto")
async def buy_crypto(data: models_pd.BuyCrypto):
    result = await buy_crypto_query(data)
    return result

@app.post("/sell_crypto")
async def sell_crypto(data: models_pd.SellCrypto):
    result = await sell_crypto_query(data)
    return result