from aiogram import BaseMiddleware
from aiogram.types import Message
from cachetools import TTLCache
from collections.abc import Awaitable
from collections.abc import Callable
from typing import Any

from source.constants import ThrottlingConstants as const


class MessageThrottlingMiddleware(BaseMiddleware):
    def __init__(self, time_limit: int = const.message_time_limit) -> None:
        self.limit = TTLCache(maxsize=1_000, ttl=time_limit)

    async def __call__(
        self,
        handler: Callable[[Message, dict[str, Any]], Awaitable[Any]],
        event: Message,
        data: dict[str, Any],
    ) -> Any:
        user_id = event.from_user.id
        if user_id in self.limit:
            return None
        self.limit[user_id] = None
        return await handler(event, data)
