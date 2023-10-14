import datetime
import re
from typing import List, NamedTuple, Optional

import pytz

import db
import config
from .categories import Categories

class Message(NamedTuple):
    """Структура распаршенного сообщения о новом расходе"""
    amount: int
    category_text: str


class Expense(NamedTuple):
    """Структура добавленного в БД нового расхода"""
    id: Optional[int]
    amount: int
    category_name: str


async def _add_expense(raw_message: str) -> None:
    """Добавляет новое сообщение.
    Принимает на вход текст сообщения, пришедшего в бот."""
    parsed_message = _parse_message(raw_message)
    if parsed_message is None: 
        print("ОБРАБОТКА") #TODO
        return
    category = await Categories().get_category(parsed_message.category_text)
    await db.execute(
        """INSERT INTO expense(amount, created, category_codename, raw_text)
           VALUES (?, ?, ?, ?)""", 
        [parsed_message.amount, 
        _get_now_formatted(), 
        category.codename ,
        raw_message] 
    )


def _parse_message(raw_message: str) -> Message:
    """Парсит текст пришедшего сообщения о новом расходе."""
    lst = raw_message.split()
    if(len(lst) == 3):
        if lst[1].isnumeric():
            return Message(amount=lst[1], category_text=lst[2])
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


async def _day() -> str:
    now = _get_now_datetime()
    today = f'{now.year:04d}-{now.month:02d}-{now.day}'
    sql = f"""SELECT category_codename, sum(amount) FROM expense
             WHERE date(created) >= '{today}' GROUP BY category_codename;"""
    rows = await db.fetch_all(sql)
    sum = 0
    string = ''
    for row in rows:
        string += row["category_codename"] + ' - ' + str(row["sum(amount)"]) + "руб.\n"
        sum += row["sum(amount)"]
    sql = f"""SELECT sum(amount) FROM expense
              WHERE date(created) >= '{today}' and category_codename in (select codename from category where is_base_expense=true)"""
    rows = await db.fetch_one(sql)
    base_today_expenses = rows["sum(amount)"] if rows["sum(amount)"] else 0
    return (f"{string}"
            f"Всего - {sum} руб."
            f"базовые - {base_today_expenses} руб. из"
            f"{await _get_budget_limit()} руб.")


async def _week() -> str:
    now = _get_now_datetime()
    monday = now - datetime.timedelta(datetime.datetime.weekday(now))
    first_day_of_week = f'{now.year:04d}-{now.month:02d}-{monday.day:02d}'
    sql = f"""SELECT category_codename, sum(amount) FROM expense
             WHERE date(created) >= '{first_day_of_week}' GROUP BY category_codename;"""
    rows = await db.fetch_all(sql)
    sum = 0
    string = ''
    for row in rows:
        string += row["category_codename"] + ' - ' + str(row["sum(amount)"]) + "руб.\n"
        sum += row["sum(amount)"]
    sql = f"""SELECT sum(amount) FROM expense
              WHERE date(created) >= '{first_day_of_week}' and category_codename in (select codename from category where is_base_expense=true)"""
    rows = await db.fetch_one(sql)
    base_today_expenses = rows["sum(amount)"] if rows["sum(amount)"] else 0
    return (f"{string}"
            f"Всего - {sum} руб."
            f"базовые - {base_today_expenses} руб. из"
            f"{(now.day-monday.day) * await _get_budget_limit()} руб.")


async def _month() -> str:
    now = _get_now_datetime()
    first_day_of_month = f'{now.year:04d}-{now.month:02d}-01'
    sql = f"""SELECT category_codename, sum(amount) FROM expense
             WHERE date(created) >= '{first_day_of_moth}' GROUP BY category_codename;"""
    rows = await db.fetch_all(sql)
    sum = 0
    string = ''
    for row in rows:
        string += row["category_codename"] + ' - ' + str(row["sum(amount)"]) + "руб.\n"
        sum += row["sum(amount)"]
    sql = f"""SELECT sum(amount) FROM expense
              WHERE date(created) >= '{first_day_of_month}' and category_codename in (select codename from category where is_base_expense=true)"""
    rows = await db.fetch_one(sql)
    base_today_expenses = rows["sum(amount)"] if rows["sum(amount)"] else 0
    return (f"{string}"
            f"Всего - {sum} руб."
            f"базовые - {base_today_expenses} руб. из"
            f"{now.day * await _get_budget_limit()} руб.")


async def _delete_expense(id: int) -> None:
    sql = f"""DELETE FROM expense WHERE id={id}"""
    await db.execute(sql)


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
    tz = pytz.timezone(config.TIMEZONE)
    return datetime.datetime.now(tz)