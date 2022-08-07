from typing import Any, Dict, List, Optional, Union

from pydantic import AnyHttpUrl, BaseSettings, EmailStr, Field, PostgresDsn, validator

#This file is set up to establish the boilerplate for connecting to the db and setting up certain other settings
#for the project, such as '/api/ being the root api url string. An ENV file is used to make the code more portable.


class Settings(BaseSettings):
    API_STR: str = "/api/"
    SECRET_KEY: str = "e92c425584f88cf73e0c823a3c4e5aafe760746e245c5cecd041de033efa4949"
    expire_minutes = 15
    expire_num_cycles = 4
    ACCESS_TOKEN_EXPIRE_MINUTES: int = expire_minutes * expire_num_cycles
    SERVER_NAME: str = "localhost"
    SERVER_HOST: AnyHttpUrl = "http://localhost"

    BACKEND_CORS_ORIGINS: List[AnyHttpUrl] = [
        "http://localhost:5000",
        "http://localhost:3000",
    ]

    PROJECT_NAME: str = "CURT_API"

    POSTGRES_SERVER: str = Field(..., env="POSTGRES_SERVER")
    POSTGRES_USER: str = Field(..., env="POSTGRES_USER")
    POSTGRES_PASSWORD: str = Field(..., env="POSTGRES_PASSWORD")
    POSTGRES_DB: str = Field(..., env="POSTGRES_DB")

    SQLALCHEMY_DATABASE_URI: Optional[PostgresDsn] = None

    @validator("SQLALCHEMY_DATABASE_URI", pre=True)
    def assemble_db_connection(cls, v: Optional[str], values: Dict[str, Any]) -> Any:
        if isinstance(v, str):
            return v
        return PostgresDsn.build(
            scheme="postgresql",
            user=values.get("POSTGRES_USER"),
            password=values.get("POSTGRES_PASSWORD"),
            host=values.get("POSTGRES_SERVER"),
            path=f"{values.get('POSTGRES_DB') or ''}",
        )

    SMTP_TLS: bool = True
    SMTP_PORT: int | None = None
    SMTP_HOST: str | None = None
    SMTP_USER: str | None = None
    SMTP_PASSWORD: str | None = None

    FIRST_SUPERUSER: str = "cthomas@example.com"
    FIRST_SUPERUSER_PASSWORD: str = Field(..., env="FIRST_SUPERUSER_PASSWORD")
    PYTEST_USER_ID: str = "user@example.com"
    PYTEST_PASSWORD: str = Field(..., env="PYTEST_PASSWORD")
    PYTEST_USER_ID: int = 1

    LOCAL_API_KEY: str = None
    ENVIRONMENT: str = None
    TEST = "TEST"

    class Config:
        case_sensitive = True
        env_file = ".env"


settings = Settings()
