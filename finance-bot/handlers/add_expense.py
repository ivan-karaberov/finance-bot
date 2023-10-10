from aiogram.types import Message

from templates import render_template


async def add_expense(message: Message) -> None:
    if message.text == "/add_expense":
        await message.answer(render_template("add_expense.j2"))
    else:
        await message.answer(message.text[12:])
