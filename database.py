import motor.motor_asyncio
import os
from dotenv import load_dotenv

load_dotenv()  # Load environment variables from .env

MONGO_URI = os.getenv("MONGO_URI")
DATABASE_NAME = os.getenv("DATABASE_NAME")

client = None  
database = None  


async def connect_to_mongo():

    global client, database
    client = motor.motor_asyncio.AsyncIOMotorClient(MONGO_URI)
    database = client[DATABASE_NAME]
    print("Connected to MongoDB")


async def close_mongo_connection():

    global client
    if client:
        client.close()
        print("Disconnected from MongoDB")
