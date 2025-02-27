from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from sqlalchemy.ext.declarative import declarative_base

SQLALCHEMY_DATABASE_URL = "sqlite+aiosqlite:///./test.db"

engine = create_async_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)

SessionLocal = async_sessionmaker(
    bind=engine,
    expire_on_commit=False
)
Base = declarative_base()


async def init_db():
    """
    Asynchronous context manager for creating a database session.

    If the tables do not exist in the database, this function will create them.
    """
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


async def get_db():
    """
    Asynchronous context manager for creating a database session.

    Yields:
        sqlalchemy.orm.Session: The active database session.
    """
    await init_db()
    async with SessionLocal() as session:
        yield session
