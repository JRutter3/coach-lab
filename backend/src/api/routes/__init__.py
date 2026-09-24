from .canvas_routes import canvas_router as canvas_router
from .org_routes import org_router as org_router
from .user_routes import user_router as user_router

ROUTERS = [canvas_router, org_router, user_router]