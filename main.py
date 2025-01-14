import asyncio
import logging
import sys
import wikipedia

from aiogram import Bot, Dispatcher, types
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart
from aiogram.types import Message
from aiogram.utils.markdown import hbold

TOKEN = "6782246368:AAFcPnOqfTHQSZO9QTosdcEAcNxL_mNYAbc"
wikipedia.set_lang('uz')
dp = Dispatcher()


@dp.message(CommandStart())
async def command_start_handler(message: Message):
    await message.reply(
        f"Hello, {hbold(message.from_user.full_name)}! I will help you to find out more info about any topic")


@dp.message()
async def echo_handler(message: types.Message):
    try:
        respond = wikipedia.summary(message.text)
        await message.answer(respond)
    except:
        await message.answer("This info doesn't look like a text message")


async def main():
    bot = Bot(TOKEN, parse_mode=ParseMode.HTML)
    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())
