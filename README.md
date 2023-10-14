# Finance Bot

## Команды бота:

- `/start` — приветственное сообщение
- `/help` — список всех команд
- `/last` — вывод последних 10 трат
- `/day` — вывод статистики трат за день
- `/week` — вывод статистики трат за неделю
- `/month` — вывод статистики трат за месяц
- `/add_expense (sum category)` — добавить трату
- `/delete_expense (id)` — удалить трату по id
- `/set_daily_limit` — установить новый дневной лимит по сумме базовых трат
- `/get_dailt_limit` — узнать дневной лимит по сумме базовых трат

## Запуск

Скопируйте `.env.example` в `.env` и отредактируйте `.env` файл, заполнив в нём все переменные окружения:

```bash
cp finance-bot/.env.example finance-bot/.env
```

Для управления зависимостями используется [poetry](https://python-poetry.org/),
требуется Python 3.10.

Установка зависимостей и запуск бота:

```bash
poetry install
poetry run python finance-bot
```
