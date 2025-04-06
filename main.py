from fastapi import FastAPI

from database import close_mongo_connection, connect_to_mongo
from routes.user import (
    router as users_router,  # Import users_router from the appropriate module
)

app = FastAPI()


@app.on_event("startup")
async def startup_event():
    await connect_to_mongo()


@app.on_event("shutdown")
async def shutdown_event():
    await close_mongo_connection()


@app.get("/")
async def root():
    return {"message": "FastAPI is running "}


app.include_router(users_router, prefix="")
