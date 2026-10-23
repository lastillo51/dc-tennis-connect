
from fastapi import FastAPI

from app.api.routes.courts import router as courts_router


app = FastAPI(
    title="DC Tennis Connect",
    description="Find public tennis courts and connect with players in Washington, D.C.",
    version="0.1.0",
)


app.include_router(courts_router)


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