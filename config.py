import os
from dotenv import load_dotenv

load_dotenv()

SECRET_KEY = os.getenv("SECRET_KEY")
DB_PATH = os.getenv("DB_PATH", "tasks.db")

if not SECRET_KEY:
    raise RuntimeError("SECRET_KEY is missing. Check your .env file.")