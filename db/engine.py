from functools import wraps

from sqlalchemy.engine import URL
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlalchemy.orm import registry
from sqlalchemy import AsyncAdaptedQueuePool
from typing import AsyncGenerator

from core.config import Config
from core.logger import setup_logger

db_env = Config.db
logger = setup_logger(__name__)
mapper = registry()


DB_URL = URL.create(
    "postgresql+asyncpg",
    username=db_env.POSTGRES_DB_USER,
    host=db_env.POSTGRES_DB_HOST,
    database=db_env.POSTGRES_DB_NAME
)

logger.info(f"DB URL: {DB_URL}")

Base = mapper.generate_base()

engine = create_async_engine(
    DB_URL,
    echo=False,
    future=True,
    pool_size=75,
    max_overflow=100,
    pool_recycle=400,
    pool_pre_ping=True,
    poolclass=AsyncAdaptedQueuePool
)

async_session_maker = async_sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

async def get_session() -> AsyncGenerator[AsyncSession, None]:
    async with async_session_maker() as session:
        yield session
        await session.close()

def connection(commit=False):
    def _connection(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            async with async_session_maker() as session:
                async with session.begin():
                    result = await func(session, *args, **kwargs)  
                    if commit:
                        await session.commit()
                    return result
        return wrapper
    return _connection