import asyncio
import logging
import traceback

from aiogram import Bot, Dispatcher
from aiogram.filters import Command

import config
import handlers
from db import close_db
from services.filters import UserFilter

COMMAND_HANDLERS = {
    "start": handlers.start,
    "help": handlers.help,
    "add_expense": handlers.add_expense,
    "delete_expense": handlers.delete_expense,
    "get_daily_limit": handlers.get_daily_limit,
    "set_daily_limit": handlers.set_daily_limit,
    "last": handlers.last,
    "week": handlers.week,
    "month": handlers.month,
    "day": handlers.day,
}

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO
)

logger = logging.getLogger(__name__)


def register_message_handlers(dp: Dispatcher) -> None:
    for key, value in COMMAND_HANDLERS.items():
        dp.message.register(
            value,
            UserFilter(access_id=config.TELEGRAM_ACCESS_ID),
            Command(key)
        )


async def main() -> None:
    bot = Bot(config.TOKEN)
    dp = Dispatcher()
    register_message_handlers(dp)
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot, allowed_updates=dp.resolve_used_update_types())


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except Exception:
        logger.warning(traceback.format_exc())
    finally:
        close_db()
