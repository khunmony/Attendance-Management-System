from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    # Reads the repo-root .env (or backend/.env); real environment variables win.
    model_config = SettingsConfigDict(env_file=("../.env", ".env"), extra="ignore")

    database_url: str = "postgresql+psycopg://ams:ams@localhost:5432/ams"
    secret_key: str = "change-me"
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 60
    cors_origins: list[str] = ["http://localhost:5500", "http://127.0.0.1:5500"]

    admin_email: str = "admin@school.local"
    admin_password: str = "ChangeMe123!"


settings = Settings()
