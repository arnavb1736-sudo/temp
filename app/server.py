from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.config import Config
from app.scheduler import start_scheduler


@asynccontextmanager
async def lifespan(app: FastAPI):
    start_scheduler()
    yield


app = FastAPI(
    title="Elevastra LinkedIn Agent",
    version="1.0.0",
    lifespan=lifespan,
)


@app.get("/")
def root():
    return {
        "message": "Elevastra LinkedIn Agent Running"
    }


@app.get("/health")
def health():
    return {
        "status": "online"
    }


@app.get("/status")
def status():
    return {
        "scheduler": "running",
        "draft_interval": Config.DRAFT_CHECK_INTERVAL,
        "publish_interval": Config.PUBLISH_CHECK_INTERVAL,
        "auto_generation": Config.ENABLE_AUTO_GENERATION,
        "auto_publish": Config.ENABLE_AUTO_PUBLISH,
    }