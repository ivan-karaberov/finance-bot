from aiogram.types import Message

from templates import render_template
from services.expenses import _last

async def last(message: Message) -> None:
    last_expenses = await _last()
    res = ''
    print(last_expenses)
    for expense in last_expenses:
        res += str(expense.id) + ' ' + expense.category_name + ' ' + str(expense.amount) + '\n'
    if len(res):
        await message.answer(res)
    else:
        await message.answer("List Fail")