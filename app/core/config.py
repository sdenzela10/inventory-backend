from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str
    debug: bool

    postgres_db: str
    postgres_user: str
    postgres_password: str
    postgres_host: str
    postgres_port: int

    jwt_secret_key: str
    jwt_algorithm: str
    access_token_expire_minutes: int

    cors_origins: str
    cors_allowed_methods: str
    cors_allowed_headers: str

    auth_cookie_name: str

    cookie_secure: bool
    cookie_httponly: bool
    cookie_samesite: str

    csrf_cookie_name: str
    csrf_header_name: str

    @property
    def database_url(self) -> str:
        return(
            f"postgresql+psycopg://{self.postgres_user}:{self.postgres_password}"
            f"@{self.postgres_host}:{self.postgres_port}/{self.postgres_db}"
        )

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
    )

settings = Settings()