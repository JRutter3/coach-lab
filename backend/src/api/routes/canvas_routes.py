from fastapi import APIRouter
from sqlalchemy import text

from api.api_models import CanvasSubmission
from api.dependencies import DBSession

canvas_router = APIRouter(
    tags=["Canvas Routes"],
    prefix="/api/v1/canvas-drawing",
)

@canvas_router.get("/count")
async def get_row_count(
    session: DBSession
) -> int:
    """Post the passed canvas to the database"""
    row_count = await session.execute(text("SELECT COUNT(*) FROM canvases"))
    print(f"Row count: {row_count}")
    return row_count.first()[0]

@canvas_router.post("/")
async def post_canvas(
    canvas_data: CanvasSubmission,
    session: DBSession,
) -> str:
    """Post the passed canvas to the database"""
    print("Hello world")

@canvas_router.get("/{canvas_id}")
async def get_canvas(canvas_id: str) -> CanvasSubmission: ...


@canvas_router.put("/{canvas_id}")
async def put_canvas(canvas_id: str) -> CanvasSubmission: ...