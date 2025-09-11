from aiogram import Dispatcher

from .message_throttling import \
    MessageThrottlingMiddleware as MessageThrottlingMiddleware
from .callback_throttling import \
    CallbackThrottlingMiddleware as CallbackThrottlingMiddleware
from .reporting import ErrorReportingMiddleware as ErrorReportingMiddleware
from source.config import settings

__all__ = [
    "ErrorReportingMiddleware",
    "MessageThrottlingMiddleware",
    "setup_middlewares",
]


def setup_middlewares(dp: Dispatcher) -> Dispatcher:
    dp.error.middleware(ErrorReportingMiddleware(settings.tg.admin_ids))
    dp.message.middleware(MessageThrottlingMiddleware())
    dp.callback_query.middleware(CallbackThrottlingMiddleware())
    return dp
