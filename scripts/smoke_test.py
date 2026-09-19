from vnpy.event import EventEngine
from vnpy.trader.engine import MainEngine


def main() -> None:
    """Verify that VeighNa's core engines can start and stop safely."""
    event_engine = EventEngine()
    main_engine = MainEngine(event_engine)

    try:
        print("Registered gateways:", main_engine.get_all_gateway_names())
        print("Built-in engines:", sorted(main_engine.engines.keys()))
        print("Framework startup check: PASSED")
    finally:
        main_engine.close()


if __name__ == "__main__":
    main()