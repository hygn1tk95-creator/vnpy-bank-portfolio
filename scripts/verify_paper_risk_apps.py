from vnpy.event import EventEngine
from vnpy.trader.engine import MainEngine

from vnpy_paperaccount import PaperAccountApp
from vnpy_riskmanager import RiskManagerApp


def main() -> None:
    event_engine = EventEngine()
    main_engine = MainEngine(event_engine)

    try:
        # 顺序不可调换：先模拟账户，后风控。
        main_engine.add_app(PaperAccountApp)
        main_engine.add_app(RiskManagerApp)

        paper_engine = main_engine.get_engine("PaperAccount")
        risk_engine = main_engine.get_engine("RiskManager")

        assert paper_engine is not None, "PaperAccount engine was not registered."
        assert risk_engine is not None, "RiskManager engine was not registered."

        print("Registered applications:", sorted(main_engine.apps.keys()))
        print("PaperAccount engine:", type(paper_engine).__name__)
        print("RiskManager engine:", type(risk_engine).__name__)
        print("Loaded risk rules:", risk_engine.get_all_rule_names())
        print("PaperAccount + RiskManager integration: PASSED")

    finally:
        main_engine.close()


if __name__ == "__main__":
    main()