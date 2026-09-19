from vnpy.trader.constant import Direction, Exchange, Offset, OrderType
from vnpy.trader.object import OrderRequest
from vnpy_riskmanager.template import RuleTemplate


class AshareOrderValueRule(RuleTemplate):
    """A股买入整手、限价与单笔金额前置风控规则。"""

    name: str = "A股整手与金额检查"

    parameters: dict[str, str] = {
        "lot_size": "A股买入最小整手",
        "max_order_value": "单笔委托金额上限",
    }

    variables: dict[str, str] = {
        "rejected_count": "累计拦截次数",
    }

    def on_init(self) -> None:
        self.lot_size: int = 100
        self.max_order_value: float = 20_000
        self.rejected_count: int = 0

    def check_allowed(self, req: OrderRequest, gateway_name: str) -> bool:
        """订单不符合规则时记录原因并拒绝。"""
        if req.exchange not in {Exchange.SSE, Exchange.SZSE}:
            return True

        if req.type != OrderType.LIMIT:
            self.rejected_count += 1
            self.write_log("A股演示账户仅允许限价单")
            self.put_event()
            return False

        if (
            req.direction == Direction.LONG
            and req.offset == Offset.OPEN
            and req.volume % self.lot_size != 0
        ):
            self.rejected_count += 1
            self.write_log(
                f"A股买入数量{req.volume}不是{self.lot_size}股的整数倍"
            )
            self.put_event()
            return False

        order_value: float = req.price * req.volume
        if order_value > self.max_order_value:
            self.rejected_count += 1
            self.write_log(
                f"委托金额{order_value:.2f}超过上限{self.max_order_value:.2f}"
            )
            self.put_event()
            return False

        return True