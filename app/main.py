from fastapi import FastAPI
from app.api.admins import router as admins_router
from app.config import settings

app = FastAPI()

app.include_router(admins_router)


@app.get("/")
def main():
    return {
        "message": "test!",
        "debug": settings.DEBUG,
    }
