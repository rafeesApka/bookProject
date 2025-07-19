from motor.motor_asyncio import AsyncIOMotorClient
from .config import MONGO_DB_URL, DB_NAME

client = AsyncIOMotorClient(MONGO_DB_URL)
db = client[DB_NAME]
# db = client.DB_NAME
