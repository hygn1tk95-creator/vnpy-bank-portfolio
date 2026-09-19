import time

from vnpy.event import Event, EventEngine
from vnpy.trader.constant import Direction, Exchange, Offset, OrderType, Product
from vnpy.trader.engine import MainEngine
from vnpy.trader.event import EVENT_CONTRACT
from vnpy.trader.object import ContractData, OrderRequest

from vnpy_paperaccount import PaperAccountApp
from vnpy_riskmanager import RiskManagerApp


VT_SYMBOL = "000001.SZSE"


def create_order_request(volume: int) -> OrderRequest:
    return OrderRequest(
        symbol="000001",
        exchange=Exchange.SZSE,
        direction=Direction.LONG,
        type=OrderType.LIMIT,
        volume=volume,
        price=10.0,
        offset=Offset.OPEN,
    )


def main() -> None:
    event_engine = EventEngine()
    main_engine = MainEngine(event_engine)

    try:
        # 顺序保证：风险检查先于模拟账户接收订单。
        main_engine.add_app(PaperAccountApp)
        main_engine.add_app(RiskManagerApp)

        contract = ContractData(
            symbol="000001",
            exchange=Exchange.SZSE,
            name="平安银行（演示合约）",
            product=Product.EQUITY,
            size=1,
            pricetick=0.01,
            gateway_name="DEMO",
        )
        event_engine.put(Event(EVENT_CONTRACT, contract))

        deadline = time.monotonic() + 1
        while not main_engine.get_contract(VT_SYMBOL):
            if time.monotonic() > deadline:
                raise TimeoutError("Demo contract was not registered.")
            time.sleep(0.01)

        risk_engine = main_engine.get_engine("RiskManager")
        assert risk_engine is not None

        # 150 股不符合 A 股整手规则，应在风控层被拦截。
        rejected_orderid = main_engine.send_order(create_order_request(150), "PAPER")
        assert rejected_orderid == "", "Invalid order should be rejected."

        # 100 股、金额 1,000 元，符合规则，应进入模拟账户。
        accepted_orderid = main_engine.send_order(create_order_request(100), "PAPER")
        assert accepted_orderid.startswith("PAPER."), "Valid order was not accepted."

        rule = risk_engine.rules["A股整手与金额检查"]

        print("Rejected 150-share order: PASSED")
        print(f"Accepted 100-share order: {accepted_orderid}")
        print(f"Custom rule rejected count: {rule.rejected_count}")
        print("Paper trading risk-control demo: PASSED")

    finally:
        main_engine.close()


if __name__ == "__main__":
    main()