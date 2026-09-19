from pathlib import Path

from vnpy.trader.database import get_database
from vnpy.trader.setting import SETTINGS
from vnpy.trader.utility import get_file_path


def main() -> None:
    """Verify that vn.py can initialize and query the local SQLite database."""
    database = get_database()

    filename = SETTINGS["database.database"]
    database_path: Path = get_file_path(filename)

    bar_overviews = database.get_bar_overview()
    tick_overviews = database.get_tick_overview()

    print(f"Database adapter: {type(database).__module__}.{type(database).__name__}")
    print(f"Database path: {database_path}")
    print(f"Database file exists: {database_path.exists()}")
    print(f"Stored bar datasets: {len(bar_overviews)}")
    print(f"Stored tick datasets: {len(tick_overviews)}")
    print("SQLite initialization: PASSED")


if __name__ == "__main__":
    main()