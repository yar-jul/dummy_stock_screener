from datetime import datetime

from fastapi import FastAPI, Depends, Path, Query
from fastapi.middleware.cors import CORSMiddleware

from misc.config import settings
from misc.db import DBService
from misc.schemas import History

app = FastAPI(
    title=settings.PROJECT_NAME,
    description=settings.DESCRIPTION,
    version=settings.VERSION
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://127.0.0.1:5500"],
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*'],
)


@app.get("/")
def ping():
    return {"live": "ok"}


@app.get("/quote/{ticker}", response_model=History)
def quote(
        ticker: str = Path(description="ticker symbol",
                           regex=r"ticker_[0-9][0-9]",
                           example="ticker_00"),
        db_service: DBService = Depends(),
        all_: bool = Query(default=False,
                           description="get all history",
                           alias="all"),
        limit: int = Query(default=100,
                           description="get N entries"),
        start: datetime | None = Query(default=None,
                                       description="start date in ISO 8601 format",
                                       example="2022-10-21T00:00:00"),
        end: datetime | None = Query(default=None,
                                     description="end date in ISO 8601 format",
                                     example="2022-10-22T00:00:00"),
):
    history = db_service.get_prices_history_for_ticker(ticker, get_all=all_, limit=limit,
                                                       start=start, end=end)
    return History(history=history)
