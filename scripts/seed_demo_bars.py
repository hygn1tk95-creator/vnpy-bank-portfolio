from datetime import datetime, timedelta
from math import sin

from vnpy.trader.constant import Exchange, Interval
from vnpy.trader.database import get_database
from vnpy.trader.object import BarData
from vnpy.trader.utility import ZoneInfo


SYMBOL = "DEMO"
EXCHANGE = Exchange.CFFEX
INTERVAL = Interval.MINUTE
BAR_COUNT = 480


def build_demo_bars() -> list[BarData]:
    """Build deterministic synthetic one-minute bars for pipeline testing."""
    timezone = ZoneInfo("Asia/Shanghai")
    current_time = datetime(2026, 1, 5, 9, 30, tzinfo=timezone)
    previous_close = 1000.0
    bars: list[BarData] = []

    for index in range(BAR_COUNT):
        trend = index * 0.03
        cycle = sin(index / 18) * 8
        close_price = 1000.0 + trend + cycle

        bar = BarData(
            symbol=SYMBOL,
            exchange=EXCHANGE,
            datetime=current_time,
            interval=INTERVAL,
            volume=100 + index % 30,
            turnover=0,
            open_interest=0,
            open_price=previous_close,
            high_price=max(previous_close, close_price) + 0.5,
            low_price=min(previous_close, close_price) - 0.5,
            close_price=close_price,
            gateway_name="DEMO",
        )
        bars.append(bar)

        previous_close = close_price
        current_time += timedelta(minutes=1)

    return bars


def main() -> None:
    """Save deterministic demo bars to the configured vn.py database."""
    bars = build_demo_bars()
    database = get_database()
    database.save_bar_data(bars)

    overviews = database.get_bar_overview()
    demo_overview = next(
        (
            item
            for item in overviews
            if item.symbol == SYMBOL
            and item.exchange == EXCHANGE
            and item.interval == INTERVAL
        ),
        None,
    )

    if demo_overview is None:
        raise RuntimeError("Demo bars were not found after saving.")

    print(f"Saved bars: {BAR_COUNT}")
    print(f"Dataset: {SYMBOL}.{EXCHANGE.value} / {INTERVAL.value}")
    print(f"Database count: {demo_overview.count}")
    print(f"Range: {demo_overview.start} -> {demo_overview.end}")
    print("Demo data ingestion: PASSED")


if __name__ == "__main__":
    main()