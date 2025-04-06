import os

from dotenv import load_dotenv
from motor.motor_asyncio import AsyncIOMotorClient
from pymongo.errors import ConnectionFailure

load_dotenv()
MONGO_URI = os.getenv("MONGO_URI")
DATABASE_NAME = os.getenv("DATABASE_NAME")


class Database:
    client: AsyncIOMotorClient = None
    db = None
    user_collection = None


db_instance = Database()


async def connect_to_mongo():
    try:
        db_instance.client = AsyncIOMotorClient(MONGO_URI)
        db_instance.db = db_instance.client[DATABASE_NAME]
        await db_instance.db.command("ping")
        print("Connected to MongoDB!")
    except ConnectionFailure as e:
        print(f"Failed to connect to MongoDB: {e}")


async def close_mongo_connection():
    if db_instance.client:
        db_instance.client.close()
        print("MongoDB connection closed.")


def get_user_collection():
    if db_instance.db is None:
        raise Exception("Database not initialized. Call connect_to_mongo() first.")
    return db_instance.db["Employees"]
