from loguru import logger

from .core import db_manager
from .models import *
from .repositories import *
from .tools.uow import AbstractUnitOfWork as AbstractUnitOfWork
from .tools.uow import UnitOfWork as UnitOfWork

__all__ = [
    "AbstractUnitOfWork",
    "UnitOfWork",
    "create_tables",
    "db_manager",
    "drop_tables",
]


async def create_tables():
    async with db_manager.engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
        logger.info("Tables created successfully")


async def drop_tables():
    async with db_manager.engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        logger.info("Tables dropped successfully")
