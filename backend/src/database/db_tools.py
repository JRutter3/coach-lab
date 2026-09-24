import sqlite3
from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager
from typing import Any, Protocol

from api.api_models import (
    OrgSubmission,
    OrgUpdate,
    StoredOrg,
    StoredUser,
    UserSubmission,
    UserUpdate,
)
from database.db_models import Base, Group, Organization, User
from sqlalchemy import event, select
from sqlalchemy.ext.asyncio import AsyncEngine, AsyncSession, create_async_engine


class DBConfig(Protocol):
    cnn_str: str
    db_type: str

class DataNotFoundError(Exception): ...

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


##### User Table Operations #####

async def _get_raw_user(user_id: str, db_session: AsyncSession) -> User:
    db_user = await db_session.get(User, user_id)
    if db_user is None:
        raise DataNotFoundError(f"Could not find user with ID: {user_id}")
    return db_user

async def write_user_to_database(api_user: UserSubmission, db_session: AsyncSession) -> StoredUser:
    """Writes a new user to the database."""
    new_user = User(
        email=api_user.email,
        first_name=api_user.first_name,
        last_name=api_user.last_name
    )
    db_session.add(new_user)
    await db_session.flush()
    return StoredUser.model_validate(
        new_user,
        from_attributes=True
    )

async def get_user_from_database(user_id: str, db_session: AsyncSession) -> StoredUser:
    """Get the user with the passed ID from the database."""
    db_user = await _get_raw_user(user_id, db_session)
    return StoredUser.model_validate(
        db_user,
        from_attributes=True
    )

async def query_users_by_email(email: str, db_session: AsyncSession) -> StoredUser:
    """Get the user with the passed email from the database."""
    stmt = select(User).where(User.email == email.lower())
    user = await db_session.scalar(stmt)
    if user is None:
        raise DataNotFoundError(f"Could not find user with email: {email}")

    return StoredUser.model_validate(
        user,
        from_attributes=True
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
    user.email = user_update.email or user.email
    await db_session.flush()

    return StoredUser.model_validate(
        user,
        from_attributes=True
    )

##### Organization Table Operations #####
async def write_org_to_database(
    org: OrgSubmission,
    db_session: AsyncSession
) -> StoredOrg:
    """Write a new organization to the database."""
    new_org = Organization(name=org.name)
    db_session.add(new_org)
    await db_session.flush()
    return StoredOrg.model_validate(
        new_org,
        from_attributes=True
    )

async def _get_raw_org(
    org_id: str,
    db_session: AsyncSession,
) -> Organization:
    """Get the raw organization ORM from the DB."""
    db_org = await db_session.get(Organization, org_id)
    if db_org is None:
        raise DataNotFoundError(f"No organization with id={org_id} found.")

    return db_org

async def get_org_from_database(
    org_id: str,
    db_session: AsyncSession,
) -> StoredOrg:
    raw_org = await _get_raw_org(org_id, db_session)
    return StoredOrg.model_validate(
        raw_org,
        from_attributes=True
    )

async def get_all_orgs_from_database(
    db_session: AsyncSession,
) -> list[StoredOrg]:
    stmt = select(*Organization.__table__.columns)
    result = [
        StoredOrg.model_validate(
            org,
            from_attributes=True
        )
        for org in (await db_session.execute(stmt))
    ]
    return result


async def update_org_in_database(
    org_id: str,
    org_update: OrgUpdate,
    db_session: AsyncSession,
) -> StoredOrg:
    raw_org = await db_session.get(Organization, org_id)
    if raw_org is None:
        raise DataNotFoundError(f"No organization with id={org_id} found.")
    raw_org.name = org_update.name or raw_org.name
    await db_session.flush()
    return StoredOrg.model_validate(
        raw_org,
        from_attributes=True
    )