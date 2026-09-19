from datetime import datetime

from vnpy.trader.constant import Exchange, Interval
from vnpy.trader.database import get_database
from vnpy.trader.datafeed import get_datafeed
from vnpy.trader.object import HistoryRequest


SYMBOL = "000001"
EXCHANGE = Exchange.SZSE
INTERVAL = Interval.DAILY
START = datetime(2018, 1, 1)
END = datetime(2025, 12, 31)


def main() -> None:
    """Download A-share daily bars from TuShare and save them to SQLite."""
    request = HistoryRequest(
        symbol=SYMBOL,
        exchange=EXCHANGE,
        interval=INTERVAL,
        start=START,
        end=END,
    )

    datafeed = get_datafeed()
    if not datafeed.init():
        raise RuntimeError("TuShare initialization failed. Check local vt_setting.json.")

    bars = datafeed.query_bar_history(request)
    if not bars:
        raise RuntimeError("No A-share daily bars were returned by TuShare.")

    database = get_database()
    database.save_bar_data(bars)

    overview = next(
        (
            item
            for item in database.get_bar_overview()
            if item.symbol == SYMBOL
            and item.exchange == EXCHANGE
            and item.interval == INTERVAL
        ),
        None,
    )

    if overview is None:
        raise RuntimeError("Downloaded bars were not found in SQLite.")

    print(f"Downloaded bars: {len(bars)}")
    print(f"Dataset: {SYMBOL}.{EXCHANGE.value} / {INTERVAL.value}")
    print(f"Stored bars: {overview.count}")
    print(f"Range: {overview.start} -> {overview.end}")
    print("A-share daily data ingestion: PASSED")


if __name__ == "__main__":
    main()