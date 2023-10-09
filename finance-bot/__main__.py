import asyncio

from aiogram import Bot, Dispatcher
from aiogram.filters import Command

import config
import handlers

COMMAND_HANDLERS = {
    "start": handlers.start,
    "help": handlers.help,
}


def register_message_handlers(dp: Dispatcher) -> None:
    for key, value in COMMAND_HANDLERS.items():
        dp.message.register(value, Command(key))


async def main() -> None:
    bot = Bot(config.TOKEN)
    dp = Dispatcher()
    register_message_handlers(dp)
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot, allowed_updates=dp.resolve_used_update_types())


if __name__ == "__main__":
    asyncio.run(main())
