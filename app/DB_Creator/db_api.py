from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from sqlalchemy.orm import declarative_base
from config import DB_USER, DB_NAME, DB_PASS, DB_PORT, DB_HOST


DATABASE_URL = f"postgresql+asyncpg://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}"


engine = create_async_engine(DATABASE_URL)
async_session_maker = async_sessionmaker(engine, class_=AsyncSession)


Base = declarative_base()

async def get_async_session():
    try:
        async with async_session_maker() as session:
            yield session
    finally:
        await session.close()