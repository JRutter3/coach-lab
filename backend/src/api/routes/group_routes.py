from database.db_tools import (
    DataNotFoundError,
    delete_group_member,
    get_group_from_database,
    query_groups_by_org,
    update_group_in_database,
    write_group_membership,
    write_group_to_database,
)
from fastapi import APIRouter, HTTPException
from sqlalchemy.exc import IntegrityError

from api.api_models import (
    GroupMembershipSubmission,
    GroupSubmission,
    GroupUpdate,
    StoredGroup,
)
from api.dependencies import DBSession

group_router = APIRouter(prefix="/api/v1/group", tags=["Groups"])


@group_router.post("/")
async def post_group(group: GroupSubmission, db_session: DBSession) -> StoredGroup:
    """Post a group to the database."""
    try:
        resp = await write_group_to_database(group, db_session)
    except IntegrityError:
        raise HTTPException(
            422,
            f"Group with name: {group.name} already exists in org-id: {group.org_id}."
        )
    return resp

@group_router.get("/{group_id}")
async def get_group(group_id: str, db_session: DBSession) -> StoredGroup:
    """Get a group from the database by ID"""
    try:
        resp = await get_group_from_database(group_id, db_session)
    except DataNotFoundError:
        raise HTTPException(
            404,
            f"URL is correct but no group with id {group_id} found."
        )

    return resp

@group_router.get("/")
async def get_all_groups_in_org(
    org_id: str,
    db_session: DBSession
) -> list[StoredGroup]:
    """Queries all groups in a given organization."""
    resp = await query_groups_by_org(org_id, db_session)
    return resp

@group_router.put("/{group_id}")
async def update_group(
    group_id: str,
    group_update: GroupUpdate,
    db_session: DBSession
) -> StoredGroup:
    """Update a group."""
    try:
        resp = await update_group_in_database(group_id, group_update, db_session)
    except DataNotFoundError:
        raise HTTPException(
            404,
            f"URL is correct but no group with id={group_id} found."
        )

    return resp


@group_router.post("/{group_id}/members")
async def add_member_to_group(
    group_id: str,
    group_membership: GroupMembershipSubmission,
    db_session: DBSession,
) -> str:
    """Add a member to the group."""
    try:
        resp = await write_group_membership(group_id, group_membership, db_session)
    except IntegrityError:
        raise HTTPException(
            422,
            (
                f"Could not find either group: {group_id}"
                f" or member {group_membership.user_id}"
            )
        )

    return resp

@group_router.delete("/{group_id}/members/{member_id}")
async def delete_member_from_group(
    group_id: str,
    member_id: str,
    db_session: DBSession,
) -> str:
    """Delete a member from the group."""
    try:
        resp = await delete_group_member(group_id, member_id, db_session)
    except DataNotFoundError:
        raise HTTPException(
            404,
            (
                "URL is correct but could not find mapping between group: {group_id}"
                f" and member: {member_id}"
            )
        )

    return resp