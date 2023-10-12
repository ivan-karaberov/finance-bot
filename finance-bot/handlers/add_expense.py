from aiogram.types import Message

from templates import render_template
from services.expenses import _add_expense

async def add_expense(message: Message) -> None:
    if message.text == "/add_expense":
        await message.answer(render_template("add_expense.j2"))
    else:
        await _add_expense(message.text)
        await message.answer("Успех")
