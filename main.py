import asyncio
import logging
import sys
import os
import wikipedia
from aiogram import Bot, Dispatcher, types
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart
from aiogram.types import Message
from aiogram.utils.markdown import hbold
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Get the token from the environment variable
TOKEN = os.getenv("TOKEN")

# Set Wikipedia language to Uzbek
wikipedia.set_lang("uz")

# Initialize Dispatcher (Aiogram 3.x)
dp = Dispatcher()

# Configure logging
logging.basicConfig(level=logging.INFO, stream=sys.stdout)


@dp.message(CommandStart())
async def command_start_handler(message: Message):
    """Handles the /start command."""
    await message.answer(
        f"Salom, {hbold(message.from_user.full_name)}! Men sizga istalgan mavzu haqida ma'lumot topishga yordam beraman. 🔍"
    )


@dp.message()
async def wikipedia_search_handler(message: Message):
    """Handles user messages and searches Wikipedia."""
    try:
        response = wikipedia.summary(message.text, sentences=2)  # Limit summary length
        await message.answer(response)
    except wikipedia.exceptions.DisambiguationError as e:
        await message.answer(f"Bu mavzu juda umumiy. Quyidagi variantlardan birini tanlang: {', '.join(e.options[:5])}")
    except wikipedia.exceptions.PageError:
        await message.answer("Kechirasiz, bu mavzu bo‘yicha ma’lumot topilmadi. Boshqa so‘z kiriting.")
    except Exception as e:
        logging.error(f"Error fetching Wikipedia data: {e}")
        await message.answer("Xatolik yuz berdi. Iltimos, keyinroq urinib ko‘ring.")


async def main():
    """Main function to start the bot."""
    bot = Bot(token=TOKEN, parse_mode=ParseMode.HTML)

    try:
        await dp.start_polling(bot)
    finally:
        await bot.session.close()  # Ensure bot session closes properly


if __name__ == "__main__":
    asyncio.run(main())
