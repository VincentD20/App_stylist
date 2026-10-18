from app.core.config import settings
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy import create_engine

engine = create_engine(settings.database_url)


class Base(DeclarativeBase):
    pass