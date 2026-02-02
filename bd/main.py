from fastapi import FastAPI, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from config import generate_session
from request_profile import create_user_query, config_sub_query, change_status_sub_query, check_created_user_query, user_statistic_query
from request_price import search_user_with_currency_query
import models_pd

app = FastAPI()

@app.post("/check_user")
async def check_user(data: models_pd.CheckUserPD, session: AsyncSession = Depends(generate_session)):
    return await check_created_user_query(data, session)

@app.post("/create_user")
async def create_user(data: models_pd.CreateUserPD, session: AsyncSession = Depends(generate_session)):
    return await create_user_query(data, session)

@app.post("/config_sub")
async def config_sub(data: models_pd.ConfigSubPD, session: AsyncSession = Depends(generate_session)):
    return await config_sub_query(data, session)

@app.post("/change_status")
async def change_status(data: models_pd.ChangeStatusUserPD, session: AsyncSession = Depends(generate_session)):
    return await change_status_sub_query(data, session)

@app.post("/actual_price")
async def actual_price(data: models_pd.ListCheckPricePD, session: AsyncSession = Depends(generate_session)):
    return await search_user_with_currency_query(data, session)

@app.post("/profile_statistics")
async def profile_statistics(data: models_pd.CheckUserPD, session: AsyncSession = Depends(generate_session)):
    return await user_statistic_query(data, session)