import os
from dotenv import load_dotenv
load_dotenv()

SECRET_KEY = os.getenv("SECRET_KEY", "secret")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30
MONGO_DB_URL = os.getenv("MONGO_DB_URL", "mongodb://localhost:27017")
DB_NAME = "ambulance_db"
