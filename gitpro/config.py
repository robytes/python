from dataclasses import dataclass
from pathlib import Path


@dataclass
class Config:
    repo_path: Path # expects Path object (not plain string): Path("C:/repos/my-app")
    database_path: Path # expects Path object (not plain string) for the SQLite db: Path("C:/git-monitor/data/events.db")
    poll_interval_seconds: int = 2 # controls monitoring interval for Git events
    ship_interval_seconds: int = 5 # controls Event Shipper

# Example usage:
# config = Config(
#     repo_path=Path("C:/repos/my-app"),
#     database_path=Path("C:/git-monitor/events.db"),
#     poll_interval_seconds=10, <-- override default if desired
#     ship_interval_seconds=30 <-- override default if desired
# )