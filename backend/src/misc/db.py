from datetime import datetime
from typing import Generator

import sqlalchemy as sa
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from .config import settings

engine = sa.create_engine(settings.DATABASE_URI, echo=True)
SessionLocal = sessionmaker(engine)

Base = declarative_base()


def get_ticker_table_class(suffix):
    attrs = {
        "__tablename__": f"ticker_{suffix}",
        'id': sa.Column(sa.Integer, primary_key=True, index=True),
        'close': sa.Column(sa.Integer, nullable=False, default=0),
        'date': sa.Column(sa.DateTime(timezone=True), default=datetime.now)
    }
    class_object = type(f"Ticker_{suffix}", (Base,), attrs)

    return class_object


ticker_table_list = {}
for number in range(settings.NUMBER_OF_TICKERS):
    ticker_table_list[number] = get_ticker_table_class(f"{number:0>2}")


def init_db() -> None:
    Base.metadata.create_all(engine)


def get_session() -> Generator:
    try:
        session = SessionLocal()
        yield session
    finally:
        session.close()
