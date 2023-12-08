from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import Command
from aiogram.types import Message, InputMediaPhoto
import logging
import asyncio
import os
from dotenv import load_dotenv

load_dotenv()

TOKEN = os.environ.get('TELEGRAM_TOKEN')

if TOKEN is None:
    print("Error: Bot token is not set. Please check your .env file.")
    exit()

bot = Bot(token=TOKEN)
dp = Dispatcher()

async def process_start_command(message: Message):
    await message.answer('''Привет!\nДанный бот создан для предсказания типа опухоли головного мозга на основе МРТ.\nПожалуйста, загрузи снимок''')

async def process_help_command(message: Message):
    await message.answer(
        'Загрузи снимок МРТ головного мозга для оценки наличия опухоли'
    )

async def reply(message: types.Message):
    await message.reply('Пожалуйста загрузи снимок МРТ')

async def photo(message: types.InputMediaPhoto):
    file_id = message.photo[0].file_id
    file = await bot.get_file(file_id)
    await message.reply('Спасибо за загрузку снимка!')

dp.message.register(process_start_command, Command(commands='start'))
dp.message.register(process_help_command, Command(commands='help'))
dp.message.register(photo, F.photo)
dp.message.register(reply)

async def main():
    logging.basicConfig(level=logging.DEBUG)
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())