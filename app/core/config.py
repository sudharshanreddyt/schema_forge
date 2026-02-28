from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import PostgresDsn, field_validator
from typing import Any, Optional


class Settings(BaseSettings):
    PROJECT_NAME: str = "Trust Worthy AI Legal Database API"
    API_V1_STR: str = "/api/v1"

    # Database settings (matching .env)
    PG_HOST: str = "localhost"
    PG_USER: str = "postgres"
    PG_PASSWORD: str = "postgres"
    PG_DB: str = "postgres"
    PG_PORT: int = 5432
    SQLALCHEMY_DATABASE_URI: Optional[str] = None

    @field_validator("SQLALCHEMY_DATABASE_URI", mode="before")
    @classmethod
    def assemble_db_connection(cls, v: Optional[str], info: Any) -> Any:
        if isinstance(v, str) and v:
            return v
        
        # Accessing data from the Settings object being built
        # pydantic v2: info.data contains the already-validated fields
        data = info.data
        user = data.get("PG_USER")
        password = data.get("PG_PASSWORD")
        host = data.get("PG_HOST")
        port = data.get("PG_PORT")
        db = data.get("PG_DB")
        
        return f"postgresql://{user}:{password}@{host}:{port}/{db}"

    model_config = SettingsConfigDict(
        env_file=".env", case_sensitive=True, extra="ignore"
    )


settings = Settings()
