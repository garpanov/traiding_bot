from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.orm import joinedload, contains_eager
import datetime
import httpx

from models_pd import ListCheckPricePD, BuyCrypto, SellCrypto
import models

async def buy_crypto_query(user_id: int, currency: str, subscription: models.Subscription,
                           session: AsyncSession, exchange: models.Exchanges):
    try:
        async with httpx.AsyncClient() as client:
            data = BuyCrypto(user_id=user_id, currency=currency, api_key=exchange.api_key, api_private=exchange.secret_key,
                             count_usdt=subscription.step_price, nonce_api=exchange.nonce_api, nonce_secret=exchange.nonce_secret)

            result = (await client.post("http://binance_service:7070/buy_crypto", json=data.model_dump())).json()

            if result["status"]:
                count_cur = float(result["data"]["quantity_crypto"])
                count_usdt = float(result["data"]["value_usdt"])
                commission_buy_usdt = float(result["data"]["commission_usdt"])
                buy_price = float(result["data"]["price_usdt"])
                order = models.OrderHistory(user_id=user_id, currency=currency, count_cur=count_cur,
                                            count_usdt=count_usdt, commission_buy_usdt=commission_buy_usdt,
                                            buy_price=buy_price)

                session.add(order)
                await session.commit()
                return {"status": True}
    except Exception as e:
        return {"status": False, "error": str(e)}

async def sell_crypto_query(user_id: int, currency: str, id_order: int, exchange: models.Exchanges,
                                subscription: models.Subscription, session: AsyncSession):
    try:
        order: models.OrderHistory | None = await session.get(models.OrderHistory, id_order)
        if order:
            async with httpx.AsyncClient() as client:
                data = SellCrypto(user_id=user_id, currency=currency, api_key=exchange.api_key,
                                 api_private=exchange.secret_key,
                                 count_curr=order.count_cur, nonce_api=exchange.nonce_api,
                                 nonce_secret=exchange.nonce_secret)

                result = (await client.post("http://binance_service:7070/sell_crypto", json=data.model_dump())).json()

                if result["status"]:
                    sell_count_net_usdt = result["data"]["cummulativeQuoteQty"] - float(result['data']["fills"][0]["commission"])
                    pnl_usdt = result["data"]["cummulativeQuoteQty"] - sell_count_net_usdt - order.commission_buy_usdt
                    order.status = 0
                    order.sell_price = float(result["data"]["fills"][0]["price"])
                    order.pnl_usdt = pnl_usdt
                    order.date_sell = datetime.datetime.now()
                    order.commission_sell_usdt = float(result['data']["fills"][0]["commission"])
                    await session.commit()
                    return {"status": True}

                else:
                    return {"status": False, "error": "Not buy"}

    except Exception as e:
        return {"status": False, "error": str(e)}


async def search_user_with_currency_query(data: ListCheckPricePD, session: AsyncSession):
    try:
        data = [item.model_dump() for item in data.data]
        for item in data:
            result = await session.execute(
                select(models.User)
                .join(models.User.subscription)
                .join(models.Subscription.exchange)
                .outerjoin(
                    models.OrderHistory,
                    (models.User.id == models.OrderHistory.user_id) & (models.OrderHistory.status == 1)
                )
                .options(
                    contains_eager(models.User.order_history),
                    joinedload(models.User.subscription),
                    joinedload(models.User.exchange)
                )
                .where(
                    models.User.status_sub == True,
                    models.Exchanges.code == item["code_exchange"],
                    models.Subscription.currency == item["currency"]
                )
            )
            users = result.unique().scalars().all() # all users who have active status and in settings set this currency

            if users:
                for user in users: # get one user
                    intervale_price = user.subscription.step_order

                    if not user.order_history: # if user doesn't have active order - buy
                        await buy_crypto_query(user.id, currency=user.subscription.currency, session=session,
                                               subscription=user.subscription, exchange=user.exchange)

                    else:
                        order_without_changes = []
                        for order in user.order_history: # for start - close needed orders and write not changed orders
                            if (item["price"] - order.buy_price) >= intervale_price:
                                await sell_crypto_query(user.id, currency=user.subscription.currency, session=session,
                                               subscription=user.subscription, id_order=order.id, exchange=user.exchange)
                            elif (item["price"] - order.buy_price) < intervale_price:
                                order_without_changes.append(order)

                        if order_without_changes: # in not changed orders search order with minimum buying price
                            minimum_price_order = None
                            for order in order_without_changes:
                                if not minimum_price_order:
                                    minimum_price_order = order

                                if order.buy_price < minimum_price_order.buy_price:
                                    minimum_price_order = order

                            if (minimum_price_order.buy_price - item["price"]) >= intervale_price: # if minimum buying price is higher than price in real time - buy
                                await buy_crypto_query(user_id=user.id, currency=item["currency"],
                                                       subscription= user.subscription, session=session, exchange=user.exchange)

                        else:
                            await buy_crypto_query(user.id, currency=user.subscription.currency, session=session,
                                                   subscription=user.subscription, exchange=user.exchange)


        return {"status": True}

    except Exception as e:
        return {"status": False, "error": str(e)}