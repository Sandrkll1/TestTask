from dependency_injector import containers, providers
from dotenv import load_dotenv

from src import redis
from src.models.base import Database
from src.settings.auth import AuthSettings
from src.settings.database import DatabaseSettings
from src.settings.redis import RedisSettings
from src.utils.module_package import get_modules_from_package

load_dotenv()


class Container(containers.DeclarativeContainer):
    wiring_config = containers.WiringConfiguration(
        modules=[
            *get_modules_from_package("src.api")
        ]
    )

    db_settings = providers.Singleton(DatabaseSettings)
    auth_settings = providers.Singleton(AuthSettings)
    redis_settings = providers.Singleton(RedisSettings)

    db = providers.Singleton(Database, db_url=db_settings.provided.uri)
    redis_pool = providers.Resource(
        redis.init_redis_pool,
        host=redis_settings.provided.host,
        # password=config.redis_password,
    )
