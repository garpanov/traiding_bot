from pydantic import BaseModel

class CheckPricePD(BaseModel):
    currency: str
    price: float
    code_exchange: int

class ListCheckPricePD(BaseModel):
    data: list[CheckPricePD]