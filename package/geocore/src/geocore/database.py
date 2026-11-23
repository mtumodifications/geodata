from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker

from geocore.config import DB_URL

if not DB_URL:
    raise ValueError("DB_URL is not configured")


class Base(DeclarativeBase):
    pass


engine = create_engine(
    DB_URL,
    echo=True,
    pool_pre_ping=True,
)

SessionLocal = sessionmaker(
    bind=engine,
    autoflush=False,
    expire_on_commit=False,
)
