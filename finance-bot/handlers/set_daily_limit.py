from aiogram.types import Message

from templates import render_template
from services.expenses import _set_daily_limit
from exceptions import NotCorrectMessage


async def set_daily_limit(message: Message) -> None:
    try:
        await _set_daily_limit(message.text)
        await message.answer(render_template('set_daily_limit.j2'))
    except NotCorrectMessage:
        await message.answer(render_template('set_daily_limit_incorrect.j2'))
