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

async def get_db():
    async with SessionLocal() as session:
        yield session
