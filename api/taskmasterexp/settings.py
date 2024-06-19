import os

from dotenv import load_dotenv

load_dotenv()

SECRET_KEY = os.environ["SECRET_KEY"]
ALGORITHM = os.getenv("JWT_ALGORITHM", "HS256")
ACCESS_TOKEN_EXPIRE_MINUTES = os.getenv("JWT_ACCESS_TOKEN_EXPIRE_MINUTES", 60)
REFRESH_TOKEN_EXPIRE_MINUTES = os.getenv(
    "JWT_REFRESH_TOKEN_EXPIRE_MINUTES", 60 * 24 * 7
)
PSQL_CONNECTION_STRING = os.getenv("DATABASE_URL", "").replace(
    "postgres", "postgresql+asyncpg"
)
CORS_ORIGINS = [url.strip() for url in os.getenv("CORS_ORIGINS", "").split(",")]
