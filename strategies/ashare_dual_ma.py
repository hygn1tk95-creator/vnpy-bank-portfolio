from vnpy.trader.object import BarData, TradeData
from vnpy_ctastrategy import ArrayManager, CtaTemplate


class AshareDualMaStrategy(CtaTemplate):
    """
    Long-only moving-average crossover strategy for A-share daily bars.

    It is designed for research and paper-trading demonstrations only.
    """

    author = "Huiming Zhuo"

    fast_window = 20
    slow_window = 60
    trading_size = 100

    fast_ma = 0.0
    slow_ma = 0.0
    last_buy_date = ""

    parameters = ["fast_window", "slow_window", "trading_size"]
    variables = ["fast_ma", "slow_ma", "last_buy_date"]

    def on_init(self) -> None:
        """Initialize indicator storage."""
        self.am = ArrayManager()
        self.write_log("A-share long-only dual-MA strategy initialized.")

    def on_bar(self, bar: BarData) -> None:
        """Process one completed daily bar."""
        self.cancel_all()

        self.am.update_bar(bar)
        if not self.am.inited:
            return

        fast_values = self.am.sma(self.fast_window, array=True)
        slow_values = self.am.sma(self.slow_window, array=True)

        self.fast_ma = float(fast_values[-1])
        self.slow_ma = float(slow_values[-1])

        fast_previous = float(fast_values[-2])
        slow_previous = float(slow_values[-2])

        cross_up = self.fast_ma > self.slow_ma and fast_previous <= slow_previous
        cross_down = self.fast_ma < self.slow_ma and fast_previous >= slow_previous

        price_tick = self.get_pricetick()
        current_date = str(bar.datetime.date())

        if cross_up and self.pos == 0:
            self.buy(bar.close_price + price_tick, self.trading_size)

        elif cross_down and self.pos > 0 and current_date != self.last_buy_date:
            self.sell(bar.close_price - price_tick, self.pos)

        self.put_event()

    def on_trade(self, trade: TradeData) -> None:
        """Record the actual buy date to enforce the T+1 selling constraint."""
        if trade.direction.value == "多" and trade.offset.value == "开":
            self.last_buy_date = str(trade.datetime.date())

        self.put_event()