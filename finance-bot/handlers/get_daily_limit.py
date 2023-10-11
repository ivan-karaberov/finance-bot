from aiogram.types import Message

from templates import render_template
from services.expenses import _get_budget_limit

async def get_daily_limit(message: Message) -> None:
    await message.answer(
        render_template("get_daily_limit.j2",
                         {"daily_limit": str(await _get_budget_limit())}
        ))
