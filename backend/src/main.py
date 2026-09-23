import uvicorn
from api.canvas_routes import canvas
from api.lifespan import app_lifespan
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware


def get_application() -> FastAPI:
    app = FastAPI(lifespan=app_lifespan)

    app.add_middleware(
        CORSMiddleware,
        allow_origins=["http://localhost:5173"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    app.include_router(canvas)
    return app


app = get_application()



if __name__ == "__main__":
    uvicorn.run(app, host="localhost", port=8000)