from aiogram.types import Message

from templates import render_template
from services.expenses import _day

async def day(message: Message) -> None:
    await message.answer(await _day())