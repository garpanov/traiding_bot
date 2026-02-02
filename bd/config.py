from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from sqlalchemy import text
import asyncio
import os

import models
from security import encrypt_data, decrypt_data
from dotenv import load_dotenv
load_dotenv()

url = os.getenv("DB_URL")
engine = create_async_engine(url, echo=True)
TG_ID = os.getenv("TELEGRAM_USER_ID")

AsyncSessionType = async_sessionmaker(bind=engine,
                                autoflush=False,
                                expire_on_commit=False)

async def generate_session():
    async with AsyncSessionType() as session:
        yield session

async def check_db():
    while True:
        try:
            async with AsyncSessionType() as session:
                await session.execute(text("SELECT 1"))
                break
        except:
            await asyncio.sleep(1)

async def create_table():
    async with engine.begin() as conn:
        await conn.run_sync(models.Base.metadata.create_all)


async def create_user():
    async with AsyncSessionType() as session:
        user = await session.get(models.User, TG_ID)
        if not user:
            keys = encrypt_data(os.getenv("BINANCE_API_KEY"), os.getenv("BINANCE_PRIVATE_KEY"))
            exchange = models.Exchanges(api_key=keys["cipher_api"], secret_key=keys["cipher_secret"],
                                        nonce_api=keys["nonce_api"], nonce_secret=keys["nonce_secret"])
            statistic = models.Statistics()
            subscription = models.Subscription(exchange=exchange)
            user = models.User(id=TG_ID, statistic=statistic, subscription=subscription, exchange=exchange, status_sub=True)
            session.add(user)
            await session.commit()

async def main():
    await check_db()
    await create_table()
    await create_user()


if __name__ == "__main__":
    asyncio.run(main())
