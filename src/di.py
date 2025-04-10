from dependency_injector import containers, providers
from dotenv import load_dotenv

from src import redis
from src.models.base import Database
from src.repositories.auth_repository import AuthRepository
from src.repositories.course_repository import CourseRepository
from src.services.courses import CourseService, FavoriteService
from src.services.user import UserService, AuthService
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
        port=redis_settings.provided.port
        # password=config.redis_password,
    )

    user_service = providers.Factory(UserService, session_factory=db.provided.session)
    auth_service = providers.Factory(AuthService, session_factory=db.provided.session)
    course_service = providers.Factory(CourseService, session_factory=db.provided.session)
    favorite_service = providers.Factory(FavoriteService, session_factory=db.provided.session)

    auth_repository = providers.Factory(
        AuthRepository,
        access_token_expire_minutes=auth_settings.provided.access_token_expire_minutes,
        refresh_token_expire_days=auth_settings.provided.refresh_token_expire_days,
        secrete_key=auth_settings.provided.secret_key,
        algorithm=auth_settings.provided.algorithm,
        user_service=user_service,
        auth_service=auth_service
    )
    course_repository = providers.Factory(
        CourseRepository,
        course_service=course_service,
        favorite_service=favorite_service
    )
