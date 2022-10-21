from datetime import datetime

import uvicorn
from fastapi import FastAPI, Depends, Path, Query

from misc.config import settings
from misc.db import DBService
from misc.schemas import History

app = FastAPI(
    title=settings.PROJECT_NAME,
    description=settings.DESCRIPTION,
    version=settings.VERSION
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
        limit: int | None = Query(100),
        start: datetime | None = Query(default=None,
                                       description="start date in ISO 8601 format",
                                       example="2022-10-21T00:00:00"),
        end: datetime | None = Query(default=None,
                                     description="end date in ISO 8601 format",
                                     example="2022-10-22T00:00:00"),
):
    history = db_service.get_prices_history_for_ticker(ticker, limit=limit, start=start, end=end)
    return History(history=history)


if __name__ == "__main__":
    uvicorn.run("api:app", host="0.0.0.0", port=8007)
