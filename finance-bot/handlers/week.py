from aiogram.types import Message

from templates import render_template
from services.expenses import _week


async def week(message: Message) -> None:
    await message.answer(render_template("week.j2",
                                         {"expenses": await _week()}))
