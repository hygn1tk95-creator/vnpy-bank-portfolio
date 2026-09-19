from vnpy.trader.object import BarData
from vnpy_ctastrategy import ArrayManager, CtaTemplate


class DualMaDemoStrategy(CtaTemplate):
    """
    Demo-only moving-average crossover strategy.

    This strategy trades only when the fast moving average crosses
    the slow moving average. It is used for framework verification,
    not for investment decisions.
    """

    author = "b115"

    fast_window = 10
    slow_window = 30
    trading_size = 1

    fast_ma = 0.0
    slow_ma = 0.0

    parameters = ["fast_window", "slow_window", "trading_size"]
    variables = ["fast_ma", "slow_ma"]

    def on_init(self) -> None:
        """Run once when the strategy instance is initialized."""
        self.am = ArrayManager()
        self.write_log("DualMaDemoStrategy initialized.")

    def on_bar(self, bar: BarData) -> None:
        """Run once for every completed one-minute bar."""
        self.cancel_all()

        self.am.update_bar(bar)
        if not self.am.inited:
            return

        fast_ma_values = self.am.sma(self.fast_window, array=True)
        slow_ma_values = self.am.sma(self.slow_window, array=True)

        self.fast_ma = float(fast_ma_values[-1])
        self.slow_ma = float(slow_ma_values[-1])

        fast_ma_previous = float(fast_ma_values[-2])
        slow_ma_previous = float(slow_ma_values[-2])

        cross_up = self.fast_ma > self.slow_ma and fast_ma_previous <= slow_ma_previous
        cross_down = self.fast_ma < self.slow_ma and fast_ma_previous >= slow_ma_previous

        price_tick = self.get_pricetick()

        if cross_up:
            if self.pos < 0:
                self.cover(bar.close_price + price_tick, abs(self.pos))
            if self.pos <= 0:
                self.buy(bar.close_price + price_tick, self.trading_size)

        elif cross_down:
            if self.pos > 0:
                self.sell(bar.close_price - price_tick, abs(self.pos))
            if self.pos >= 0:
                self.short(bar.close_price - price_tick, self.trading_size)

        self.put_event()