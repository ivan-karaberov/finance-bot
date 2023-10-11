from aiogram.types import Message

from templates import render_template
from services.expenses import _set_budget_limit

async def set_daily_limit(message: Message) -> None:
    str = message.text.split()
    if str[1].isnumeric():
        await _set_budget_limit(int(str[1]))
        await message.answer(render_template('set_daily_limit.j2'))
    else: 
        await message.answer(render_template('set_daily_limit_incorrect.j2'))
