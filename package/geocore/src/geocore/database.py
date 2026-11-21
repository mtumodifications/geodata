from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from .config import DB_URL

if not DB_URL:
    raise ValueError("DB_URL is not configured")

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
