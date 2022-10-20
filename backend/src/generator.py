import time
from datetime import datetime, timezone, timedelta
from random import random

from sqlalchemy import select

from misc.config import settings
from misc.db import init_db, get_session, ticker_table_list


def generate_movement():
    movement = -1 if random() < 0.5 else 1
    return movement


def get_current_price(last_price):
    movement = generate_movement()

    if last_price == 0 and movement < 0:  # optional
        return 0

    return last_price + movement


def main() -> None:
    current_timestamp = int(time.time())
    timezone_info = timezone(timedelta(hours=0))
    session = next(get_session())

    while True:
        for ticker_table in ticker_table_list.values():
            row = session.execute(select(ticker_table).order_by(ticker_table.id.desc())).first()

            if row is None:
                current_price = 0
            else:
                current_price = get_current_price(row[0].close)

            ticker = ticker_table(
                close=current_price,
                date=datetime.fromtimestamp(current_timestamp, tz=timezone_info)
            )

            session.add(ticker)
            session.commit()
            session.refresh(ticker)

        if (time.time() - current_timestamp) < 1:
            time.sleep(settings.DELAY)
        current_timestamp += 1


if __name__ == '__main__':
    init_db()
    main()
