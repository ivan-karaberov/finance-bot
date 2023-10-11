import datetime
import re
from typing import List, NamedTuple, Optional

import pytz

import db
import config
from .categories import Categories


async def _get_budget_limit() -> int:
    """Возвращает дневной бюджет на день"""
    sql = """SELECT daily_limit FROM budget WHERE codename = 'base'"""
    limit = await db.fetch_one(sql)
    return limit["daily_limit"]


async def _set_budget_limit(sum: int) -> None:
    """Возвращает дневной бюджет на день"""
    sql = f"""UPDATE budget SET daily_limit={sum} WHERE codename = 'base'"""
    await db.execute(sql)



def _get_now_formatted() -> str:
    """Возвращает настоящую Дату и время строкой"""
    return _get_now_datetime().strftime(config.DATETIME_FORMAT)


def _get_now_datetime() -> datetime.datetime:
    """Возвращает настоящую Дату и время"""
    tz = pytz.tz(config.TIMEZONE)
    return datetime.datetime.now(tz)