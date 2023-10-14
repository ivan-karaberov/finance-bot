from aiogram.types import Message

from templates import render_template
from services.expenses import _delete_expense
from exceptions import NotCorrectMessage, DoesNotExists


async def delete_expense(message: Message) -> None:
    try:
        await _delete_expense(message.text)
        await message.answer(render_template('delete_expense.j2'))
    except DoesNotExists:
        await message.answer(render_template("delete_expense_not_exists.j2"))
    except NotCorrectMessage:
        await message.answer(render_template("delete_expense_incorrect.j2"))
