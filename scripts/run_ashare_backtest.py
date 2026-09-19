from datetime import datetime

from vnpy.trader.constant import Interval
from vnpy_ctastrategy.backtesting import BacktestingEngine

from strategies.ashare_dual_ma import AshareDualMaStrategy


def main() -> None:
    """Backtest the long-only strategy with real A-share daily bars."""
    engine = BacktestingEngine()

    engine.set_parameters(
        vt_symbol="000001.SZSE",
        interval=Interval.DAILY,
        start=datetime(2018, 1, 1),
        end=datetime(2025, 12, 31),
        rate=0.0003,
        slippage=0.01,
        size=1,
        pricetick=0.01,
        capital=1_000_000,
    )

    engine.add_strategy(
        AshareDualMaStrategy,
        {
            "fast_window": 20,
            "slow_window": 60,
            "trading_size": 100,
        },
    )

    engine.load_data()
    if not engine.history_data:
        raise RuntimeError("No 000001.SZSE daily bars found in SQLite.")

    engine.run_backtesting()
    result = engine.calculate_result()
    statistics = engine.calculate_statistics(result, output=False)

    print(f"Loaded daily bars: {len(engine.history_data)}")
    print(f"Completed trades: {len(engine.get_all_trades())}")
    print(f"Total net PnL: {statistics['total_net_pnl']:.2f}")
    print(f"Total commission: {statistics['total_commission']:.2f}")
    print(f"Total slippage: {statistics['total_slippage']:.2f}")
    print(f"Max drawdown: {statistics['max_drawdown']:.2f}")
    print(f"Max drawdown percent: {statistics['max_ddpercent']:.2f}%")
    print(f"Sharpe ratio: {statistics['sharpe_ratio']:.2f}")
    print("A-share backtest: PASSED")


if __name__ == "__main__":
    main()