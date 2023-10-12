from aiogram.types import Message

from templates import render_template
from services.expenses import _delete_expense

async def delete_expense(message: Message) -> None:
    str = message.text.split()
    if len(str) > 1 and str[1].isnumeric():
        await _delete_expense(int(str[1]))
        await message.answer(render_template('delete_expense.j2'))
    else:
        await message.answer(render_template('delete_expense_incorrect.j2'))
