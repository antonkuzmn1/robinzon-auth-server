from fastapi import FastAPI
# from app.api.admins import router as admins_router
# from app.api.companies import router as companies_router
# from app.api.users import router as users_router
from app.config import settings

print(settings)
print(type(settings))
print(f"app before init: {globals().get('app', None)}")
app = FastAPI()
print(f"app after init: {type(app)}")

# app.include_router(admins_router)
# app.include_router(companies_router)
# app.include_router(users_router)


@app.get("/")
def main():
    print(f"settings is of type: {type(settings)}")
    return {
        "message": "test!",
        "debug": settings.DEBUG,
        "test": 10,
    }
