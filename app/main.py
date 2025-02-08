from fastapi import FastAPI
from app.config import settings

app = FastAPI()

@app.get("/")
def main():
    return {
        "message": "test!",
        "debug": settings.DEBUG,
    }