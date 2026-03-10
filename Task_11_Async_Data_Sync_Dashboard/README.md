# Task 11 — Async Data Sync Dashboard

## Topic
Paradigms, Concurrency & Environment

## What This Task Does
A data team needs a tool that simultaneously pulls data from three mock sources,
merges the results, and displays a combined summary. Runs inside a virtual environment
with all credentials stored in a `.env` file outside the codebase.

## File Structure
```
Task_11_Async_Data_Sync_Dashboard/
├── dashboard.py    ← Main script
└── .env            ← Config file (DB host, API key, etc.)
```

## Concepts Used
- `asyncio`: `async def`, `await`, `asyncio.run()`, `asyncio.gather()`
- `asyncio.gather()` to run 3 coroutines simultaneously
- `python-dotenv` to load `.env` config
- `os.getenv()` to read environment variables
- `venv` — virtual environment (optional, recommended)

## Setup
```bash
# Install dependency
pip install python-dotenv

# Optional: create virtual environment
python -m venv venv
venv\Scripts\activate        # Windows
source venv/bin/activate     # Linux / Mac
pip install python-dotenv
```

## How to Run
```bash
# IMPORTANT: run from inside this folder
cd Task_11_Async_Data_Sync_Dashboard
python dashboard.py
```

## Sample Output
```
Pulling data from 3 sources simultaneously...

[Source 3] Analytics data received!   ← fastest (0.8s delay)
[Source 1] Sales data received!        ← medium (1.5s delay)
[Source 2] Inventory data received!   ← slowest (2.0s delay)

COMBINED DASHBOARD SUMMARY
...
```
