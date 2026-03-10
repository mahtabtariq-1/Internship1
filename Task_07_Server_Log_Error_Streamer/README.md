# Task 07 — Server Log Error Streamer

## Topic
Generators & Iterators

## What This Task Does
The backend team has server log files too large to load into memory.
This script builds a streaming system that reads line by line, yields only
critical error entries, groups them by error type, and shows a live running
count — without loading the full file at once.

## Concepts Used
- Generator functions with `yield`
- Reading files line by line (memory efficient)
- Generator expressions
- `itertools` usage
- Custom iterator logic
- `__iter__` / `__next__` concepts in practice

## How to Run
```bash
python server_log_streamer.py
```

The script auto-creates a `server.log` sample file with 200 lines, then streams it.

## Sample Output
```
#1      ERROR      NullPointerException         auth-service
#2      CRITICAL   DatabaseConnectionError      payment-api
...
SUMMARY - Errors by Type:
  NullPointerException        :  16 ################
  DatabaseConnectionError     :  14 ##############
```
