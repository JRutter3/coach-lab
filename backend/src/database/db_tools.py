import sqlite3
from collections.abc import AsyncGenerator
from contextlib import asynccontextmanager
from typing import Any, Protocol

from api.api_models import (
    CanvasSubmission,
    CanvasUpdate,
    GroupMembershipSubmission,
    GroupSubmission,
    GroupUpdate,
    OrgSubmission,
    OrgUpdate,
    StoredCanvas,
    StoredGroup,
    StoredOrg,
    StoredUser,
    UserRoleEnum,
    UserSubmission,
    UserUpdate,
)
from database.db_models import (
    Base,
    Canvas,
    Group,
    GroupMembership,
    Organization,
    OrgMembership,
    User,
)
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
    return StoredUser.model_validate(new_user, from_attributes=True)

async def get_user_from_database(user_id: str, db_session: AsyncSession) -> StoredUser:
    """Get the user with the passed ID from the database."""
    db_user = await _get_raw_user(user_id, db_session)
    return StoredUser.model_validate(db_user, from_attributes=True)

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
    return StoredUser.model_validate(user, from_attributes=True)

##### Organization Table Operations #####
async def write_org_to_database(
    org: OrgSubmission,
    db_session: AsyncSession
) -> StoredOrg:
    """Write a new organization to the database."""
    new_org = Organization(name=org.name)
    db_session.add(new_org)
    await db_session.flush()
    return StoredOrg.model_validate(new_org, from_attributes=True)

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
    return StoredOrg.model_validate(raw_org, from_attributes=True)

async def get_all_orgs_from_database(
    db_session: AsyncSession,
) -> list[StoredOrg]:
    stmt = select(*Organization.__table__.columns)
    result = [
        StoredOrg.model_validate(org, from_attributes=True)
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
    return StoredOrg.model_validate(raw_org, from_attributes=True)

##### Group table operations #####
async def write_group_to_database(
    group: GroupSubmission,
    db_session: AsyncSession
) -> StoredGroup:
    """Writes a new group to the database."""
    new_group = Group(
        name=group.name,
        org_id=group.org_id,
    )

    db_session.add(new_group)
    await db_session.flush()
    return StoredGroup.model_validate(new_group, from_attributes=True)

async def _get_raw_group(group_id:str, db_session: AsyncSession) -> Group:
    group = await db_session.get(Group, group_id)
    if group is None:
        raise DataNotFoundError(f"No group with id {group_id} found.")
    return group

async def get_group_from_database(
    group_id: str,
    db_session: str,
) -> StoredGroup:
    """Get a group from its ID from the database."""
    group = await _get_raw_group(group_id, db_session)
    return StoredGroup.model_validate(group, from_attributes=True)

async def query_groups_by_org(
    org_id: str,
    db_session: AsyncSession
) -> list[StoredGroup]:
    """Query groups by org_id."""
    stmt = select(Group).where(Group.org_id == org_id)

    return [
        StoredGroup.model_validate(group, from_attributes=True)
        for group in await db_session.scalars(stmt)
    ]

async def update_group_in_database(
    group_id: str,
    group_update: GroupUpdate,
    db_session: AsyncSession,
) -> StoredGroup:
    """Update a group to match the group updates."""
    group = await _get_raw_group(group_id, db_session)
    group.org_id = group_update.group_id or group.org_id
    group.name = group_update.name or group.name

    await db_session.flush()
    return StoredGroup.model_validate(group, from_attributes=True)

##### Group Membership Operations #####
async def write_group_membership(
    group_id: str,
    group_submission: GroupMembershipSubmission,
    db_session: AsyncSession,
) -> str:
    """Write membership of a user into a group."""
    group_membership = GroupMembership(
        user_id=group_submission.user_id,
        group_id=group_id,
        role=group_submission.role,
    )
    db_session.add(group_membership)
    await db_session.flush()
    return "User successfully added to group."

async def write_org_membership(
    user_id: str,
    org_id: str,
    user_role: UserRoleEnum,
    db_session: AsyncSession,
) -> str:
    org_membership = OrgMembership(
        user_id=user_id,
        org_id=org_id,
        role=user_role,
    )

    db_session.add(org_membership)
    await db_session.flush()
    return "User successfully added to org."

async def delete_group_member(
    group_id: str,
    user_id: str,
    db_session: AsyncSession,
) -> str:
    target_member = await db_session.get(GroupMembership, (user_id, group_id))
    if target_member is None:
        raise DataNotFoundError(
            f"No membership between user {user_id} and group {group_id}"
        )

    await db_session.delete(target_member)
    return f"Group: {group_id}, Member: {user_id} mapping deleted."


##### Canvas Operations #####
async def write_canvas_to_database(
    canvas: CanvasSubmission,
    db_session: AsyncSession
) -> StoredCanvas:
    """Add a new canvas to the database."""
    new_canvas = Canvas(
        name=canvas.name,
        template=canvas.template,
        data=canvas.data.model_dump(),
        owner_id=canvas.owner_id,
        visibility=canvas.visibility,
        group_id=canvas.group_id,
        org_id=canvas.org_id,
    )

    db_session.add(new_canvas)
    await db_session.flush()
    return StoredCanvas.model_validate(new_canvas, from_attributes=True)

async def _get_raw_canvas(canvas_id: str, db_session: AsyncSession) -> Canvas:
    canvas = await db_session.get(Canvas, canvas_id)
    if canvas is None:
        raise DataNotFoundError(f"No such canvas with ID: {canvas_id}. Found")
    return canvas

async def get_canvas_from_database(
    canvas_id: str,
    db_session: AsyncSession,
) -> StoredCanvas:
    """Get the canvas from the database."""
    resp = await _get_raw_canvas(canvas_id, db_session)
    return StoredCanvas.model_validate(resp, from_attributes=True)

async def query_canvas_by_owner(
    owner_id: str,
    db_session: AsyncSession,
) -> list[StoredCanvas]:
    """Query canvases by owner."""
    stmt = select(Canvas).where(Canvas.owner_id == owner_id)
    result = [
        StoredCanvas.model_validate(canvas, from_attributes=True)
        for canvas in (await db_session.scalars(stmt))
    ]
    return result

    
async def update_canvas_in_database(
    canvas_id: str,
    canvas_data: CanvasUpdate,
    db_session: AsyncSession
) -> StoredCanvas:
    """Update the canvas data in the database."""
    canvas = await _get_raw_canvas(canvas_id, db_session)
    canvas.name = canvas_data.name or canvas.name
    canvas.template = canvas_data.template or canvas.template
    canvas.data = canvas_data.data or canvas.data
    canvas.owner_id = canvas_data.owner_id or canvas.owner_id
    canvas.group_id = canvas_data.group_id or canvas.group_id
    canvas.org_id = canvas_data.org_id or canvas.org_id

    await db_session.flush()
    return StoredCanvas.model_validate(canvas, from_attributes=True)
