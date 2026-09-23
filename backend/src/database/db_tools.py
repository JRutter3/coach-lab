import sqlite3
from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager
from typing import Any, Protocol

from database.db_models import Base
from sqlalchemy import event
from sqlalchemy.ext.asyncio import AsyncEngine, AsyncSession, create_async_engine


class DBConfig(Protocol):
    cnn_str: str
    db_type: str


async def init_db(db_config: DBConfig) -> AsyncEngine:
    """Get an instance of the database engine, used for creating sessions."""
    engine = create_async_engine(db_config.cnn_str)
    if db_config.db_type == "sqlite":
        set_listener = event.listens_for(engine.sync_engine, "connect")
        set_listener(_set_sqlite_pragma)

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    return engine


@asynccontextmanager
async def db_session_manager(db_engine: AsyncEngine) -> AsyncGenerator[AsyncSession]:
    async with AsyncSession(db_engine) as session:
        try:
            yield session
            await session.commit()
        except Exception:
            await session.rollback()
            raise
        finally:
            await session.close()


def _set_sqlite_pragma(dbapi_connection: sqlite3.Connection, connection_record: Any):
    cursor = dbapi_connection.cursor()
    cursor.execute("PRAGMA foreign_keys=ON")
    cursor.close()