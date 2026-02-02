from pydantic import BaseModel

class InfoUser(BaseModel):
    user_id: int
    api_key: str
    api_private: str
    nonce_api: str
    nonce_secret: str

class Crypto(InfoUser):
    currency: str

class BuyCrypto(Crypto):
    count_usdt: float

class SellCrypto(Crypto):
    count_curr: float
