from datetime import datetime

from vnpy.trader.constant import Interval
from vnpy_ctastrategy.backtesting import BacktestingEngine

from strategies.dual_ma_demo import DualMaDemoStrategy


def main() -> None:
    """Run a reproducible backtest against DEMO.CFFEX SQLite data."""
    engine = BacktestingEngine()

    engine.set_parameters(
        vt_symbol="DEMO.CFFEX",
        interval=Interval.MINUTE,
        start=datetime(2026, 1, 5, 9, 30),
        end=datetime(2026, 1, 6, 0, 0),
        rate=0.00003,
        slippage=0.2,
        size=300,
        pricetick=0.2,
        capital=1_000_000,
    )

    engine.add_strategy(
        DualMaDemoStrategy,
        {
            "fast_window": 10,
            "slow_window": 30,
            "trading_size": 1,
        },
    )

    engine.load_data()
    if not engine.history_data:
        raise RuntimeError("No DEMO.CFFEX bars found in the configured database.")

    engine.run_backtesting()
    result = engine.calculate_result()
    statistics = engine.calculate_statistics(result, output=False)

    print(f"Loaded bars: {len(engine.history_data)}")
    print(f"Completed trades: {len(engine.get_all_trades())}")
    print(f"Total net PnL: {statistics['total_net_pnl']:.2f}")
    print(f"Total commission: {statistics['total_commission']:.2f}")
    print(f"Total slippage: {statistics['total_slippage']:.2f}")
    print(f"Max drawdown: {statistics['max_drawdown']:.2f}")
    print(f"Sharpe ratio: {statistics['sharpe_ratio']:.2f}")
    print("Demo backtest: PASSED")


if __name__ == "__main__":
    main()