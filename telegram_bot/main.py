from aiogram import Bot, Dispatcher, F, BaseMiddleware
from aiogram.types import Message, CallbackQuery, FSInputFile
from aiogram.client.bot import DefaultBotProperties
from aiogram.filters import CommandStart
import asyncio
import os

from routers.profile_rout import profile_router
import keyboards
from dotenv import load_dotenv
load_dotenv()

class ShadowUserMiddleware(BaseMiddleware):
    def __init__(self, accept_user: int):
        self.accept_user = accept_user

    async def __call__(self, handler, event, data):
        if event.from_user.id != self.accept_user:
            return None
        else:
            return await handler(event, data)

ds = Dispatcher()
ds.include_routers(profile_router)
ds.message.outer_middleware(ShadowUserMiddleware(accept_user=int(os.getenv("TELEGRAM_USER_ID"))))
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

@ds.message(CommandStart())
async def hey(message: Message):
    photo_path = os.path.join(BASE_DIR, "images", "start.jpg")
    main_photo = FSInputFile(photo_path)
    await message.answer_photo(photo=main_photo, caption='<b>Welcome to the Club ⚜️</b>\n\n'
                         'You can only join this bot if you have <b>money</b> and know at least something about <b>crypto</b> 💎\n\n'
                         'In short, here you can connect a bot that will trade for you <i>(not futures)!</i>\n\n<b>Cool, isn’t it? 🔥</b>', reply_markup=keyboards.start)

@ds.callback_query(F.data == "main_menu")
async def hey(callback: CallbackQuery):
    photo_path = os.path.join(BASE_DIR, "images", "start.jpg")
    main_photo = FSInputFile(photo_path)
    await callback.message.delete()
    await callback.message.answer_photo(photo=main_photo, caption='<b>Welcome to the Club ⚜️</b>\n\n'
                         'You can only join this bot if you have <b>money</b> and know at least something about <b>crypto</b> 💎\n\n'
                         'In short, here you can connect a bot that will trade for you <i>(not futures)!</i>\n\n<b>Cool, isn’t it? 🔥</b>', reply_markup=keyboards.start)


async def start_bot():
    bot = Bot(token=os.getenv('TELEGRAM_TOKEN'), default=DefaultBotProperties(parse_mode="HTML"))
    await bot.delete_webhook(drop_pending_updates=True)
    await ds.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(start_bot())

