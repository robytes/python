## Architecture

```mermaid
flowchart TD
    A[Developer Git Repository]
    B[Repository Monitor]
    C[(Local SQLite DB<br/>Durable Event Queue)]
    D[Event Shipper<br/>Async / Retry]
    E[Mock API]

    A -->|Poll Git State| B
    B -->|Events| C
    C -->|Unsent Events| D
    D --> E
```

## Initial Project Structure
git-agent/
│
├── agent/
│   ├── __init__.py
│   ├── config.py
│   ├── git_monitor.py
│   ├── storage.py
│   └── main.py
│
├── data/
│
├── requirements.txt
└── README.md