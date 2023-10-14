from aiogram.filters import BaseFilter
from aiogram.types import Message


class UserFilter(BaseFilter):
    """Аунтификация пользователя по ID"""

    def __init__(self, access_id: int) -> None:
        self._access_id = access_id

    async def __call__(self, message: Message) -> bool:
        return int(self._access_id) == int(message.chat.id)
