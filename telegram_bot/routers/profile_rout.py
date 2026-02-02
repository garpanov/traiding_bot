from aiogram import Router, F
from aiogram.types import CallbackQuery
import httpx

from . import keyboards_routs
from telegram_bot import model_pd

profile_router = Router()


@profile_router.callback_query(F.data == "profile")
async def profile_info(callback: CallbackQuery):
    await callback.message.delete()

    async with httpx.AsyncClient() as client:
        data = model_pd.CheckUserPD(id=callback.from_user.id)
        response = await client.post("http://bd:8080/check_user", json=data.model_dump())
        result = response.json()

    if result["result"]:
        result_bd = {"is_new_user": result["new_user"], "status_sub": result["status_sub"],
                     "open_orders": result["open_orders"], "pnl": result["pnl_day"]}

        await callback.message.answer(text=f"<b>📌 Account Information</b>\n\n"
                                           f"<b>📄 Status Subscription: {"🟢 Active" if result_bd["status_sub"] else "🛑 Not Active"}</b>\n"
                                           f"<b>💰 Your open orders: {result_bd["open_orders"]}</b>\n\n"
                                           f"<b>📈 PnL (Last Day): ${result_bd["pnl"]}</b>\n",
                                      reply_markup=keyboards_routs.get_keyboard_profile_info(is_profile=not result_bd["is_new_user"],
                                                                                             isActive=result_bd["status_sub"],))

    else:
        await callback.message.answer(text="<b>Sorry, something went wrong 😕\nPlease try again</b>", reply_markup=keyboards_routs.return_menu_keyboard)


@profile_router.callback_query(F.data == "profile_change_active")
async def profile_change_active(callback: CallbackQuery):
    await callback.message.delete()

    async with httpx.AsyncClient() as client:
        data = model_pd.CheckUserPD(id=callback.from_user.id)
        response = await client.post("http://bd:8080/change_status", json=data.model_dump())
        if response.json()["result"]:
            result = (await client.post("http://bd:8080/check_user", json=data.model_dump())).json()
            result_bd = {"is_new_user": result["new_user"], "status_sub": result["status_sub"],
                         "open_orders": result["open_orders"], "pnl": result["pnl_day"]}

            await callback.message.answer(text=f"<b>📌 Account Information</b>\n\n"
                                               f"<b>📄 Status Subscription: {"🟢 Active" if result_bd["status_sub"] else "🛑 Not Active"}</b>\n"
                                               f"<b>💰 Your open orders: {result_bd["open_orders"]}</b>\n\n"
                                               f"<b>📈 PnL (Last Day): ${result_bd["pnl"]}</b>\n",
                                          reply_markup=keyboards_routs.get_keyboard_profile_info(
                                              is_profile=not result_bd["is_new_user"],
                                              isActive=result_bd["status_sub"], ))

        else:
            await callback.message.answer(text="<b>Sorry, something went wrong 😕\nPlease try again</b>",
                                          reply_markup=keyboards_routs.return_menu_keyboard)

@profile_router.callback_query(F.data == "profile_statistics")
async def profile_statistics(callback: CallbackQuery):
    await callback.message.delete()
    async with httpx.AsyncClient() as client:
            data = model_pd.CheckUserPD(id=callback.from_user.id)
            response = (await client.post("http://bd:8080/profile_statistics", json=data.model_dump())).json()
            if response["result"]:

                await callback.message.answer(text=f"<b>📌 Account Statistic</b>\n\n"
                                                   f"<b>📄 Count all orders: {response["all_orders"]}</b>\n"
                                                   f"<b>💰 Your open orders: {response["open_orders"]}</b>\n\n"
                                                   f"<b>📈 PnL (Last Day): ${response["pnl_1"]}</b>\n"
                                                   f"<b>📈 PnL (7 Days): ${response["pnl_7"]}</b>\n"
                                                   f"<b>📈 PnL (30 Days): ${response["pnl_30"]}</b>\n",
                                              reply_markup=keyboards_routs.return_profile_keyboard)

            else:
                await callback.message.answer(text="<b>Sorry, something went wrong 😕\nPlease try again</b>",
                                              reply_markup=keyboards_routs.return_menu_keyboard)


