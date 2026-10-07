from database.db_tools import (
    DataNotFoundError,
    delete_canvas_from_database,
    get_canvas_from_database,
    query_canvas_by_owner,
    update_canvas_in_database,
    write_canvas_to_database,
)
from fastapi import APIRouter, HTTPException

from api.api_models import CanvasSubmission, CanvasUpdate, MessageResponse, StoredCanvas
from api.dependencies import AuthData, DBSession

canvas_router = APIRouter(
    tags=["Canvas Routes"],
    prefix="/api/v1/canvas-drawing",
)

@canvas_router.post("/")
async def post_canvas(
    canvas_data: CanvasSubmission,
    session: DBSession,
    user_data: AuthData,
) -> StoredCanvas:
    """Post the passed canvas to the database"""
    return await write_canvas_to_database(user_data.id, canvas_data, session)

@canvas_router.get("/{canvas_id}")
async def get_canvas(
    canvas_id: str,
    db_session: DBSession,
    user_data: AuthData
) -> StoredCanvas:
    """Get the canvas from the database by id."""
    try:
        result = await get_canvas_from_database(canvas_id, db_session, user_data.id)
    except DataNotFoundError:
        raise HTTPException(404, f"No canvas with id {canvas_id} found.")
    return result

@canvas_router.get("/")
async def query_canvas(user_data: AuthData, db_session: DBSession) -> list[StoredCanvas]:
    """Query all canvases belonging to a specific user."""
    return await query_canvas_by_owner(user_data.id, db_session)


@canvas_router.put("/{canvas_id}")
async def put_canvas(
    canvas_id: str,
    canvas_update: CanvasUpdate,
    user_data: AuthData,
    db_session: DBSession
) -> StoredCanvas:
    """Update a canvas with the latest data."""
    try:
        result = await update_canvas_in_database(
            canvas_id,
            canvas_update,
            db_session,
            user_data.id,
            )
    except DataNotFoundError:
        raise HTTPException(404, f"No canvas with id: {canvas_id} found.")

    return result

@canvas_router.delete("/{canvas_id}")
async def delete_canvas(
    canvas_id: str,
    user_data: AuthData,
    db_session: DBSession,
) -> MessageResponse:
    """Delete a canvas by ID"""
    await delete_canvas_from_database(canvas_id, db_session, user_data.id)
    return MessageResponse(message=f"Canvas {canvas_id} successfully deleted.")