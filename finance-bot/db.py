import asyncio
import aiofiles
from typing import Any, Iterable
from typing_extensions import LiteralString

import aiosqlite

import config


async def get_db() -> aiosqlite.Connection:
    if not getattr(get_db, "db", None):
        db = await aiosqlite.connect(config.SQLITE_DB_FILE)
        get_db.db = db

    return get_db.db


async def fetch_all(sql: LiteralString,
                    params: Iterable[Any] | None = None) -> list[dict]:
    cursor = await _get_cursor(sql, params)
    rows = await cursor.fetchall()
    results = []
    for row in rows:
        results.append(_get_result_with_columns_names(cursor, row))
    await cursor.close()
    return results


async def fetch_one(sql: LiteralString,
                    params: Iterable[Any] | None = None) -> dict | None:
    cursor = await _get_cursor(sql, params)
    row = await cursor.fetchone()
    if row:
        row = _get_result_with_columns_names(cursor, row)
    await cursor.close()
    return row


async def execute(sql: LiteralString, params: Iterable[Any] | None = None, *,
                  autocommit: bool = True) -> None:
    db = await get_db()
    args = (sql, params)
    await db.execute(*args)
    if autocommit:
        await db.commit()


async def _get_cursor(sql: LiteralString,
                      params: Iterable[Any] | None) -> aiosqlite.Cursor:
    db = await get_db()
    args = (sql, params)
    cursor = await db.execute(*args)
    db.row_factory = aiosqlite.Row
    return cursor


def _get_result_with_columns_names(cursor: aiosqlite.Cursor,
                                   row: aiosqlite.Row) -> dict:
    column_names = [d[0] for d in cursor.description]
    resulting_row = {}
    for index, column in enumerate(column_names):
        resulting_row[column] = row[index]
    return resulting_row


def close_db() -> None:
    asyncio.run(_async_close_db())


async def _async_close_db() -> None:
    await (await get_db()).close()


async def _init_db() -> None:
    """Инициализирует БД"""
    db = await get_db()
    async with aiofiles.open(config.INITIALIZATION_DB_FILE, mode="r") as file:
        sql = await file.read()
    await db.executescript(sql)
    await db.commit()


async def check_db_exists() -> None:
    """Проверяет инициализированна ли БД, если нет инициализирует"""
    row = await fetch_one("SELECT name FROM sqlite_master")
    if row is None:
        await _init_db()


asyncio.run(check_db_exists())
