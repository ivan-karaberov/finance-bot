import datetime
from typing import List, NamedTuple, Optional

import pytz

import db
import config
from .categories import Categories
from exceptions import NotCorrectMessage, DoesNotExists


class Message(NamedTuple):
    """Структура распаршенного сообщения о новом расходе"""
    amount: int
    category_text: str


class Expense(NamedTuple):
    """Структура добавленного в БД нового расхода"""
    id: Optional[int]
    amount: int
    category_name: str


class Statistic(NamedTuple):
    base: int
    all_expense: int
    daily_limit: int
    statisctic: List[Expense]


async def _day() -> str:
    now = _get_now_datetime()
    today = f'{now.year:04d}-{now.month:02d}-{now.day}'
    return await _get_statisctic(today, 1)


async def _week() -> str:
    now = _get_now_datetime()
    monday = now - datetime.timedelta(datetime.datetime.weekday(now))
    first_day_of_week = f'{now.year:04d}-{now.month:02d}-{monday.day:02d}'
    return await _get_statisctic(first_day_of_week, (now.day-monday.day))


async def _month() -> str:
    now = _get_now_datetime()
    first_day_of_month = f'{now.year:04d}-{now.month:02d}-01'
    return await _get_statisctic(first_day_of_month, now.day)


async def _get_statisctic(date: str, _daily_limit: int):
    sql = f"""SELECT id, category_codename, sum(amount) FROM expense
             WHERE date(created) >= '{date}' GROUP BY category_codename;"""
    rows = await db.fetch_all(sql)

    sum = 0
    lst: List[Expense] = []

    for row in rows:
        lst.append(
            Expense(
                id=row["id"],
                amount=row["sum(amount)"],
                category_name=row["category_codename"]
            )
        )
        sum += row["sum(amount)"]

    sql = f"""SELECT sum(amount) FROM expense
              WHERE date(created) >= '{date}' and category_codename in
              (select codename from category where is_base_expense=true)"""
    rows = await db.fetch_one(sql)
    base_today_expenses = rows["sum(amount)"] if rows["sum(amount)"] else 0

    return Statistic(
        all_expense=sum,
        statisctic=lst,
        base=base_today_expenses,
        daily_limit=_daily_limit * await _get_daily_limit()
    )


async def _add_expense(raw_message: str) -> None:
    parsed_message = _parse_message(raw_message, 2)
    if parsed_message is None:
        raise NotCorrectMessage
    category = await Categories().get_category(parsed_message.category_text)
    sql = """INSERT INTO expense(amount, created, category_codename, raw_text)
             VALUES (?, ?, ?, ?)"""
    await db.execute(sql, [parsed_message.amount, _get_now_formatted(),
                           category.codename, raw_message])


async def _delete_expense(raw_message: str) -> None:
    message = _parse_message(raw_message, 1)
    if message is None:
        raise NotCorrectMessage

    sql = f"""SELECT id FROM expense WHERE id={message.amount}"""
    row = await db.fetch_one(sql)
    if row is None:
        raise DoesNotExists

    sql = f"""DELETE FROM expense WHERE id={message.amount}"""
    await db.execute(sql)


def _parse_message(raw_message: str, params_count: int) -> Message | None:
    """Парсит текст пришедшего сообщения"""
    message = raw_message.split()
    if params_count == 1:
        if (len(message) >= 2):
            if message[1].isnumeric():
                return Message(amount=message[1], category_text="")
    elif params_count == 2:
        if (len(message) >= 3):
            if message[1].isnumeric():
                return Message(amount=message[1], category_text=message[2])
    return None


async def _last() -> List[Expense]:
    sql = """SELECT id, amount, category_codename FROM expense
             ORDER BY created desc limit 10"""
    rows = await db.fetch_all(sql)
    results = []
    for row in rows:
        results.append(
            Expense(
                id=row["id"],
                amount=row["amount"],
                category_name=row["category_codename"]
            )
        )
    return results


async def _set_daily_limit(raw_message: str) -> None:
    """Обновляет дневной лимит на день"""
    message = _parse_message(raw_message, 1)
    if message is None:
        raise NotCorrectMessage
    sql = f"""UPDATE budget SET daily_limit={message.amount}
              WHERE codename = 'base'"""
    await db.execute(sql)


async def _get_daily_limit() -> int:
    """Возвращает дневной лимит на день"""
    sql = """SELECT daily_limit FROM budget WHERE codename = 'base'"""
    limit = await db.fetch_one(sql)
    return limit["daily_limit"] if limit else 0


def _get_now_formatted() -> str:
    """Возвращает настоящую Дату и время строкой"""
    return _get_now_datetime().strftime(config.DATETIME_FORMAT)


def _get_now_datetime() -> datetime.datetime:
    """Возвращает настоящую Дату и время"""
    tz = pytz.timezone(config.TIMEZONE)
    return datetime.datetime.now(tz)
