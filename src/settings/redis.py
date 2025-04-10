from pydantic_settings import BaseSettings, SettingsConfigDict


class RedisSettings(BaseSettings):
    host: str
    port: int

    model_config = SettingsConfigDict(env_prefix="redis_")

    @property
    def url(self) -> str:
        return f"redis://{self.host}:{self.port}/0"
