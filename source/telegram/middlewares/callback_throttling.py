from aiogram import BaseMiddleware
from aiogram.types import CallbackQuery
from cachetools import TTLCache
from collections.abc import Awaitable
from collections.abc import Callable
from typing import Any

from source.constants import ThrottlingConstants as const

class CallbackThrottlingMiddleware(BaseMiddleware):
    def __init__(self, time_limit: int = const.callback_time_limit) -> None:
        self.limit = TTLCache(maxsize=10_00, ttl=time_limit)

    async def __call__(
        self,
        handler: Callable[[CallbackQuery, dict[str, Any]], Awaitable[Any]],
        event: CallbackQuery,
        data: dict[str, Any],
    ) -> Any:
        user_id = event.from_user.id
        if user_id in self.limit:
            await event.answer("")
            return None
        self.limit[user_id] = None
        return await handler(event, data)
    