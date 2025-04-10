from pydantic_settings import BaseSettings, SettingsConfigDict


class DatabaseSettings(BaseSettings):
    host: str
    port: int = 5432
    name: str
    user: str
    password: str
    driver: str = "asyncpg"
    type: str = "postgresql"

    model_config = SettingsConfigDict(env_prefix="db_")

    @property
    def uri(self) -> str:
        return f"{self.type}+{self.driver}://{self.user}:{self.password}@{self.host}:{self.port}/{self.name}"
