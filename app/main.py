from fastapi import FastAPI

from app.api.routes.courts import router as courts_router

from pathlib import Path

from fastapi.staticfiles import StaticFiles

from app.web.routes import router as web_router


BASE_DIR = Path(__file__).resolve().parent

app = FastAPI(
    title="DC Tennis Connect",
    description="Find public tennis courts and connect with players in Washington, D.C.",
    version="0.1.0",
)


app.mount(
    "/static",
    StaticFiles(directory=str(BASE_DIR / "static")),
    name="static",
)

app.include_router(courts_router)
app.include_router(web_router)

@app.get("/")
def read_root():
    return {
        "application": "DC Tennis Connect",
        "message": "Welcome to DC Tennis Connect!",
    }


@app.get("/health")
def health_check():
    return {
        "status": "healthy",
    }