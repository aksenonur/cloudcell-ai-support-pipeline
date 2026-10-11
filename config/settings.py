import os
from dotenv import load_dotenv

load_dotenv()

class Settings:
    OPENAI_API_KEY: str = os.getenv("OPENAI_API_KEY", "")
    APP_ENV: str = os.getenv("APP_ENV", "development")

settings = Settings()