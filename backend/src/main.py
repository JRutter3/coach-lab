import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic_models.api_models import CanvasSubmission

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.post("/api/v1/canvas-drawing")
async def post_canvas(canvas_data: CanvasSubmission) -> str:
    pass

if __name__ == "__main__":
    uvicorn.run(app, host="localhost", port=8000)