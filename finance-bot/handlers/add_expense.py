from aiogram.types import Message

from templates import render_template
from services.expenses import _add_expense
from exceptions import NotCorrectMessage


async def add_expense(message: Message) -> None:
    try:
        await _add_expense(message.text)
        await message.answer(render_template('add_expense.j2'))
    except NotCorrectMessage:
        await message.answer(render_template("add_expense_incorrect.j2"))
