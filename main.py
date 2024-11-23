import os
import asyncio

from dotenv import load_dotenv
from aiogram import Bot, Dispatcher
from aiogram.filters import Command
from aiogram.types import (
    Message,
    CallbackQuery,
    InlineKeyboardMarkup,
    InlineKeyboardButton
)

load_dotenv()
BOT_TOKEN = os.getenv("BOT_TOKEN")

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

schedule = {
    "Понедельник": "React 11:00 - 12:10\nBackend 12:20-14:10\nБД 14:20 - 15:10\nФилософия 15:20 - 16:10",
    "Вторник": "Алгоритмы 10:00 - 11:10\nБД 11:10 - 13:10",
    "Среда": "Математика 12:20 - 13:10\nАнглийский 13:20 - 15:20",
    "Четверг": "Информатика 11:00 - 13:10\nBackend 13:20 - 15:10",
    "Пятница": "Манасоведение 11:00 - 12:10\nАлгоритмы 12:20 - 14:20"
}

@dp.message(Command("start"))
async def start(message: Message) -> None:
    text = "Выберите день недели:"
    markup = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text=day, callback_data=f"day:{day}")]
        for day in schedule.keys()
    ])
    await message.answer(text=text, reply_markup=markup)

@dp.callback_query(lambda call: call.data.startswith("day:"))
async def send_schedule(call: CallbackQuery) -> None:
    day = call.data.split("day:")[1]
    if day in schedule:
        text = f"Расписание на {day}:\n{schedule[day]}"
        await call.message.answer(text=text)
    else:
        await call.message.answer(text="Неизвестный день!")

async def main() -> None:
    print("Бот запущен")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())