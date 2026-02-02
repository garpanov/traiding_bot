from pydantic import BaseModel

class CreateUserPD(BaseModel):
    id: int

class CheckUserPD(CreateUserPD):
    pass

class ConfigSubPD(BaseModel):
    id: int
    currency: str
    step_order: float
    step_price: float
    max_order: int
    code_exchange: int
    api_key: str
    secret_key: str

class ChangeStatusUserPD(CreateUserPD):
    pass

class CheckPricePD(BaseModel):
    currency: str
    price: float
    code_exchange: int

class ListCheckPricePD(BaseModel):
    data: list[CheckPricePD]


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
