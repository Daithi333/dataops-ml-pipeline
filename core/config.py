import os


class Config:

    DB_HOST = os.getenv("DB_HOST", "localhost")
    DB_PORT = os.getenv("DB_PORT", "5432")
    DB_USER = os.getenv("DB_USER", "data_user")
    DB_PW = os.getenv("DB_PW", "data_pass")
    DB_NAME = os.getenv("DB_NAME", "analytics_db")

    DB_URL = f"postgresql://{DB_USER}:{DB_PW}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

    DB_POOL_SIZE = int(os.environ.get("DB_POOL_SIZE", 20))
    DB_MAX_OVERFLOW = int(os.environ.get("DB_MAX_OVERFLOW", 20))
