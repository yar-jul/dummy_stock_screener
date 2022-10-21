from datetime import datetime, timezone, timedelta
from typing import Generator

import sqlalchemy as sa
from fastapi import Depends
from sqlalchemy import select
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import Session, sessionmaker

from .config import settings

engine = sa.create_engine(settings.DATABASE_URI)
SessionLocal = sessionmaker(engine)

Base = declarative_base()

timezone_info = timezone(timedelta(hours=0))


def get_ticker_table_class(suffix):
    attrs = {
        "__tablename__": f"ticker_{suffix}",
        'id': sa.Column(sa.Integer, primary_key=True, index=True),
        'close': sa.Column(sa.Integer, nullable=False, default=0),
        'date': sa.Column(sa.DateTime(timezone=True), default=datetime.now)
    }
    class_object = type(f"Ticker_{suffix}", (Base,), attrs)

    return class_object


ticker_tables = {}
for number in range(settings.NUMBER_OF_TICKERS):
    ticker_tables[f"ticker_{number:0>2}"] = get_ticker_table_class(f"{number:0>2}")


def init_db() -> None:
    Base.metadata.create_all(engine)


def get_session() -> Generator:
    try:
        session = SessionLocal()
        yield session
    finally:
        session.close()


class DBService:

    def __init__(self, session: Session = Depends(get_session)):
        self.session = session

    def get_prices_history_for_ticker(self, ticker: str,
                                      limit: int | None,
                                      start: datetime | None,
                                      end: datetime | None):
        ticker_table = ticker_tables[ticker]
        history = {}
        if limit is None:  # all
            result = self.session.execute(select(ticker_table).order_by(ticker_table.id.asc()))
            for row in result:
                history[row[0].date.isoformat()] = {"close": row[0].close}
        elif start is None:  # last N entries
            result = self.session.execute(
                select(ticker_table).order_by(ticker_table.id.desc())).first()
            last_id = result[0].id
            result = self.session.execute(select(ticker_table).where(
                ticker_table.id <= last_id, ticker_table.id > last_id - limit))
            for row in result:
                history[row[0].date.isoformat()] = {"close": row[0].close}
        else:  # search with start/end date
            if end is None:
                end = datetime.now(timezone_info)
            result = self.session.execute(
                select(ticker_table).where(ticker_table.date.between(start, end)))
            for row in result:
                history[row[0].date.isoformat()] = {"close": row[0].close}
        return history
