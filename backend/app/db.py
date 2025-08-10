# backend/app/db.py
import os
from motor.motor_asyncio import AsyncIOMotorClient
from dotenv import load_dotenv

# Load .env file from backend directory
load_dotenv()

MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017")
client = AsyncIOMotorClient(MONGO_URI)

# Use database named "whatsapp"
db = client.get_database("whatsapp")
processed_messages = db.processed_messages
