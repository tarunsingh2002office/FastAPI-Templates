from pathlib import Path
from pydantic_settings import BaseSettings

class BaseAppSettings(BaseSettings):
    BASE_DIR: Path = Path(__file__).resolve().parent.parent
    MEDIA_URL: str = "/media/"
    MEDIA_ROOT: Path = BASE_DIR / "media"
    STATIC_URL: str = "static/"
    class Config:
        env_file = ".env"
        extra = "ignore"  # Ignore extra fields in the .env file


class DatabaseSettings(BaseSettings):
    MONGODB_URI: str
    DB_NAME: str
    class Config:
        env_file = ".env"
        extra = "ignore"  # Ignore extra fields in the .env file


class JWTSettings(BaseSettings):
    SUGAR_VALUE: str
    class Config:
        env_file = ".env"
        extra = "ignore"  # Ignore extra fields in the .env file


# Instantiate settings
base_settings = BaseAppSettings()
db_settings = DatabaseSettings()
jwt_settings = JWTSettings()
# if __name__ == "__main__":
#     print(base_settings.BASE_DIR)
#     print(db_settings.MONGODB_URI)
