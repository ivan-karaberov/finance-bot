from aiogram.filters import BaseFilter
from aiogram.types import Message


class UserFilter(BaseFilter):
    def __init__(self, access_id: int) -> None:
        self._access_id = access_id

    def __call__(self, message: Message) -> bool:
        if (int(self._access_id) == int(message.chat.id)):
            return True
        return False
