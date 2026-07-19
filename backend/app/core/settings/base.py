from pydantic_settings import BaseSettings
from pydantic import ConfigDict, field_validator
from urllib.parse import quote

class Settings(BaseSettings):
    model_config = ConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")

    PROJECT_NAME: str = "AIPAS Backend"
    API_V1_STR: str = "/api/v1"
    APP_ENV: str = "development"
    DEBUG: bool = True

    # Security Config
    JWT_SECRET_KEY: str = "AIPAS_BACKEND_SECRET_KEY_JWT_123!"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60          # 1 hour for access tokens
    REFRESH_TOKEN_EXPIRE_DAYS: int = 7             # 7 days for refresh tokens

    # Account Lockout Policy
    MAX_LOGIN_ATTEMPTS: int = 5
    LOCKOUT_MINUTES: int = 15

    # Database Connection
    DATABASE_URL: str = "postgresql+asyncpg://postgres:postgres@localhost:5432/aipas"

    @field_validator("DATABASE_URL", mode="before")
    @classmethod
    def encode_database_credentials(cls, value: str) -> str:
        """Allow database passwords containing URL-reserved characters.

        A password such as ``pa@ss`` must be percent-encoded in a database
        URL.  Normalising it here preserves existing .env files while giving
        SQLAlchemy an unambiguous host and credential pair.
        """
        if not isinstance(value, str) or "://" not in value:
            return value

        scheme, remainder = value.split("://", 1)
        credentials, separator, host_and_path = remainder.rpartition("@")
        if not separator or ":" not in credentials:
            return value

        username, password = credentials.split(":", 1)
        return f"{scheme}://{quote(username, safe='%')}:{quote(password, safe='%')}@{host_and_path}"

    # CORS configuration
    CORS_ORIGINS: list[str] = ["*"]

    # Storage Layer Configuration
    STORAGE_BACKEND: str = "local"                 # "local" or "s3"
    LOCAL_STORAGE_ROOT: str = "storage_root"
    S3_BUCKET_NAME: str = "aipas-evidence-bucket"
    S3_REGION: str = "us-east-1"

    # AI Service Config
    AI_SERVICE_URL: str = ""
    AI_SERVICE_API_KEY: str = "mock_api_key_123!"
    DUPLICATE_SIMILARITY_THRESHOLD: float = 0.82
