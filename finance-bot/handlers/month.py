from aiogram.types import Message

from templates import render_template
from services.expenses import _month

async def month(message: Message) -> None:
    await message.answer(await _month())