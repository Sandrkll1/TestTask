from pydantic import Field
from pydantic_settings import BaseSettings


class AuthSettings(BaseSettings):
    secret_key: str = Field(validation_alias="jws_secret_key")
    algorithm: str = Field("HS256", validation_alias="jws_algorithm")
    access_token_expire_minutes: int = Field(30, validation_alias="jws_access_token_expire_minutes")
    refresh_token_expire_days: int = Field(7, validation_alias="jws_refresh_token_expire_days")
