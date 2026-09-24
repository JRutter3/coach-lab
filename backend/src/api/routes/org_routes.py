from database.db_tools import (
    DataNotFoundError,
    get_all_orgs_from_database,
    update_org_in_database,
    write_org_to_database,
)
from fastapi import APIRouter, HTTPException
from sqlalchemy.exc import IntegrityError

from api.api_models import OrgSubmission, OrgUpdate, StoredOrg
from api.dependencies import DBSession

org_router = APIRouter(prefix="/api/v1/org", tags=["Organization"])


@org_router.post("/")
async def post_org(new_org: OrgSubmission, db_session: DBSession) -> StoredOrg:
    """Post a new org to the database."""
    try:
        resp = await write_org_to_database(new_org, db_session)
    except IntegrityError:
        raise HTTPException(
            422,
            f"Organization: {new_org.name} already exists."
        )
    return resp

@org_router.get("/")
async def get_all_orgs(db_session: DBSession) -> list[StoredOrg]:
    """Get all orgs in the database."""
    return await get_all_orgs_from_database(db_session)

@org_router.get("/{org_id}")
async def get_org_by_id(org_id: str, db_session: DBSession) -> StoredOrg:
    """Get a single org by organization id"""
    try:
        resp = await get_org_by_id(org_id, db_session)
    except DataNotFoundError:
        raise HTTPException(
            404,
            f"URL is correct but no org with id {org_id} found."
        )
    return resp

@org_router.put("/{org_id}")
async def update_org(
    org_id: str,
    org_update: OrgUpdate,
    db_session: DBSession
) -> StoredOrg:
    """Update an org by org_id with an OrgUpdate object."""
    try:
        resp = await update_org_in_database(org_id, org_update, db_session)
    except DataNotFoundError:
        raise HTTPException(
            404,
            f"URL is correct but no org with id {org_id} found."
        )

    return resp
