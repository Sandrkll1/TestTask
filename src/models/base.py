import logging
from contextlib import asynccontextmanager
from typing import AsyncGenerator

from sqlalchemy import text
from sqlalchemy.ext.asyncio import (AsyncEngine, AsyncSession,
                                    create_async_engine)
from sqlalchemy.orm import declarative_base, sessionmaker

logger = logging.getLogger(__name__)

Base = declarative_base()


class Database:
    def __init__(self, db_url: str) -> None:
        self._engine: AsyncEngine = create_async_engine(db_url, pool_size=20, max_overflow=10, echo=False)
        self._session_factory = sessionmaker(self._engine, class_=AsyncSession, expire_on_commit=False)

    @asynccontextmanager
    async def session(self) -> AsyncGenerator[AsyncSession, None]:
        session: AsyncSession = self._session_factory()
        try:
            yield session
            await session.commit()
        except Exception:
            logger.exception("Session rollback because of exception")
            await session.rollback()
            raise
        finally:
            await session.close()

    async def create_tables(self) -> bool:
        logger.info("Creating tables...")
        async with self._engine.begin() as conn:
            for table in Base.metadata.sorted_tables:
                query = text(f"SELECT EXISTS (SELECT FROM information_schema.tables WHERE table_name = '{table.name}')")
                result = await conn.execute(query)
                exists = result.scalar()
                if not exists:
                    await conn.run_sync(Base.metadata.create_all)
                    logger.info("Tables created.")
                    return True
            logger.info("Tables already exist. Skipping creation.")
            return False

    async def initialize_database(self) -> None:
        logger.info("Initializing database")
        await self.create_tables()
