from .canvas_routes import canvas_router as canvas_router
from .group_routes import group_router as group_router
from .login_routes import login_router
from .org_routes import org_router as org_router
from .user_routes import user_router as user_router

ROUTERS = [canvas_router, login_router, org_router, user_router, group_router]