from aiogram.types import Message

from templates import render_template
from services.expenses import _last


async def last(message: Message) -> None:
    last_expenses = await _last()
    if len(last_expenses):
        await message.answer(render_template("last.j2",
                                             {"expenses": last_expenses}))
    else:
        await message.answer(render_template("last_empty.j2"))
