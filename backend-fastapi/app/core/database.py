import os
from motor.motor_asyncio import AsyncIOMotorClient

MONGO_URI = os.getenv("MONGO_URI", "mongodb://santi:santi123@localhost:27017/autostock?authSource=admin")

client = AsyncIOMotorClient(MONGO_URI)
db = client["autostock"]
