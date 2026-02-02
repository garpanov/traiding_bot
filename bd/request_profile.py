from sqlalchemy import select
from sqlalchemy.orm import joinedload, contains_eager
from sqlalchemy.ext.asyncio import AsyncSession

import models
import models_pd


async def check_created_user_query(data: models_pd.CheckUserPD, session: AsyncSession):
    try:
        user = (await session.execute(select(models.User)
                                    .outerjoin(models.OrderHistory, (models.User.id == models.OrderHistory.user_id) & (models.OrderHistory.status == 1))
                                    .options(contains_eager(models.User.order_history),
                                              joinedload(models.User.statistic))
                                    .where(models.User.id == data.id))).scalars().first()
        if not user:
            return {"result": True, "new_user": True}

        return {"result": True, "new_user": False, "status_sub": user.status_sub, "pnl_day": user.statistic.pnl_24_hours, "open_orders": len(user.order_history)}
    except Exception as e:
        return {"result": False, "error": str(e)}

async def create_user_query(data: models_pd.CreateUserPD, session: AsyncSession) -> dict:
    try:
        exchange = models.Exchanges()
        statistic = models.Statistics()
        subscription = models.Subscription(exchange=exchange)
        user = models.User(id=data.id, statistic=statistic, subscription=subscription, exchange=exchange)
        session.add(user)
        await session.commit()
        return {"result": True}
    except Exception as e:
        return {"result": False, "error": str(e)}

async def check_user_query(data: models_pd.CreateUserPD, session: AsyncSession):
    user = await session.get(models.User, data.id)
    if not user:
        data_for_create = models_pd.CreateUserPD(id=data.id)
        await create_user_query(data_for_create, session)
        user = await session.get(models.User, data.id)

    return user

async def config_sub_query(data: models_pd.ConfigSubPD, session: AsyncSession) -> dict:
    try:
        user = await check_user_query(models_pd.CreateUserPD(id=data.id), session)

        info_sub = (await session.execute(select(models.Subscription)
                                         .where(models.Subscription.id == user.sub_id)
                                         .options(joinedload(models.Subscription.exchange)))).scalars().first()

        info_sub.currency = data.currency
        info_sub.step_order = data.step_order
        info_sub.step_price = data.step_price
        info_sub.max_order = data.max_order
        info_sub.exchange.code = data.code_exchange
        info_sub.exchange.api_key = data.api_key
        info_sub.exchange.secret_key = data.secret_key

        await session.commit()
        return {"result": True}

    except Exception as e:
        return {"result": False, "error": str(e)}


async def change_status_sub_query(data: models_pd.ChangeStatusUserPD, session: AsyncSession) -> dict:
    try:
        user = await check_user_query(models_pd.CreateUserPD(id=data.id), session)
        user.status_sub = not user.status_sub
        await session.commit()
        return {"result": True, "status": user.status_sub}
    except Exception as e:
        return {"result": False, "error": str(e)}

async def user_statistic_query(data: models_pd.CheckUserPD, session: AsyncSession) -> dict:
    try:
        user = (await session.execute(select(models.User)
                                      .outerjoin(models.OrderHistory,
                                                 (models.User.id == models.OrderHistory.user_id))
                                      .options(contains_eager(models.User.order_history),
                                               joinedload(models.User.statistic))
                                      .where(models.User.id == data.id))).scalars().first()
        if not user:
            return {"result": True, "new_user": True}

        else:
            all_order = len(user.order_history)
            open_orders = 0
            for order in user.order_history:
                if order.status == 1:
                    open_orders += 1

            return {"result": True, "new_user": False, "all_orders": all_order, "open_orders": open_orders,
                    "pnl_1": user.statistic.pnl_24_hours, "pnl_7": user.statistic.pnl_7_days, "pnl_30": user.statistic.pnl_30_days}

    except Exception as e:
        return {"result": False, "error": str(e)}



