# Task 08 — API Middleware Simulator

## Topic
Decorators & Logging

## What This Task Does
A backend team needs reusable function wrappers that handle execution timing,
input/output logging, and role-based access control — without touching the original
functions. All wrappers are stackable and all activity goes through the `logging`
module, not print statements.

## Concepts Used
- Functions as first-class objects and closures
- Writing basic decorators with `@`
- Decorators that accept arguments (`require_role`)
- `functools.wraps` — preserving function metadata
- Stacking multiple decorators (`@timer`, `@log_io`, `@require_role`)
- `logging` module with log levels: DEBUG, INFO, WARNING
- File and console handlers running simultaneously

## How to Run
```bash
python api_middleware.py
```

Also creates `api_activity.log` with all logged activity.

## Sample Output
```
[16:10:01] INFO - [ACCESS OK] 'get_all_users' | User: Ali Hassan Role: admin
[16:10:01] WARNING - [ACCESS DENIED] 'get_all_users' | Role 'viewer' not in ['admin', 'manager']
[16:10:01] INFO - [TIMER] 'get_all_users' executed in 50.81ms
```
