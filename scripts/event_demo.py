from time import sleep

from vnpy.event import EVENT_TIMER, Event, EventEngine


EVENT_STRATEGY_SIGNAL = "eStrategySignal"


def on_strategy_signal(event: Event) -> None:
    """Handle a custom strategy-signal event."""
    signal: dict = event.data
    print(
        "Signal received:",
        f"symbol={signal['symbol']}, "
        f"direction={signal['direction']}, "
        f"reason={signal['reason']}",
    )


def on_timer(event: Event) -> None:
    """Handle VeighNa's built-in periodic timer event."""
    print(f"Timer event received: {event.type}")


def main() -> None:
    """Start an event engine, publish events, then close it safely."""
    event_engine = EventEngine(interval=1)

    event_engine.register(EVENT_STRATEGY_SIGNAL, on_strategy_signal)
    event_engine.register(EVENT_TIMER, on_timer)

    event_engine.start()

    try:
        signal = {
            "symbol": "IF2606.CFFEX",
            "direction": "LONG",
            "reason": "Demo signal only; no order is sent.",
        }
        event_engine.put(Event(EVENT_STRATEGY_SIGNAL, signal))

        sleep(2.2)
    finally:
        event_engine.stop()
        print("Event engine stopped safely.")


if __name__ == "__main__":
    main()