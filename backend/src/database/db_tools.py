import sqlite3
from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager
from typing import Any, Protocol

from api.api_models import StoredUser, UserSubmission, UserUpdate
from database.db_models import Base, User
from sqlalchemy import event, select
from sqlalchemy.ext.asyncio import AsyncEngine, AsyncSession, create_async_engine


class DBConfig(Protocol):
    cnn_str: str
    db_type: str

class UserNotFoundError(Exception): ...

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


async def write_user_to_database(api_user: UserSubmission, db_session: AsyncSession) -> StoredUser:
    """Writes a new user to the database."""
    new_user = User(
        email=api_user.e_mail,
        first_name=api_user.first_name,
        last_name=api_user.last_name
    )
    db_session.add(new_user)
    await db_session.flush()
    return StoredUser.model_construct(
        user_id=new_user.id,
        first_name=new_user.first_name,
        last_name=new_user.last_name,
        e_mail=new_user.email,
    )


async def get_user_from_database(user_id: str, db_session: AsyncSession) -> StoredUser:
    """Get the user with the passed ID from the database."""
    db_user = await _get_raw_user(user_id, db_session)
    return StoredUser.model_construct(
        user_id=db_user.id,
        first_name=db_user.first_name,
        last_name=db_user.last_name,
        e_mail=db_user.email
    )

async def _get_raw_user(user_id: str, db_session: AsyncSession) -> User:
    db_user = await db_session.get(User, user_id)
    if db_user is None:
        raise UserNotFoundError(f"Could not find user with ID: {user_id}")
    return db_user


async def query_users_by_email(email: str, db_session: AsyncSession) -> StoredUser:
    """Get the user with the passed email from the database."""
    stmt = select(User).where(User.email == email.lower())
    user = await db_session.scalar(stmt)
    if user is None:
        raise UserNotFoundError(f"Could not find user with email: {email}")

    return StoredUser.model_construct(
        user_id=user.id,
        first_name=user.first_name,
        last_name=user.last_name,
        e_mail=user.email,
    )

async def update_user_in_database(
    user_id: str,
    user_update: UserUpdate,
    db_session: AsyncSession
) -> StoredUser:
    """Update the user with the passed update."""
    user = await _get_raw_user(user_id, db_session)
    user.first_name = user_update.first_name or user.first_name
    user.last_name = user_update.last_name or user.last_name
    user.email = user_update.e_mail or user.email
    await db_session.flush()

    return StoredUser.model_construct(
        user_id=user.id,
        first_name=user.first_name,
        last_name=user.last_name,
        e_mail=user.email,
    )