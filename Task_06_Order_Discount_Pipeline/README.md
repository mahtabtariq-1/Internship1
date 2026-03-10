# Task 06 — Order Discount Pipeline

## Topic
Lambda, Map, Filter & Functional Tools

## What This Task Does
An online store needs a data pipeline that takes a raw list of customer orders,
applies category-based discount rules, filters out orders below a minimum threshold,
and returns a processed summary with total revenue — using NO traditional `for` loops.

## Concepts Used
- `lambda` — syntax, use cases
- `map()` with lambda to apply discounts
- `filter()` with lambda to remove low-value orders
- `functools.reduce()` to calculate total revenue
- `sorted()` with lambda as key

## How to Run
```bash
python order_discount_pipeline.py
```

## Sample Output
```
ID       Customer     Category         Original  Disc%      Final
-----------------------------------------------------------------
ORD004   Fatima       Electronics    Rs.  72,000    10%  Rs.64,800.00
ORD001   Ali          Electronics    Rs.  25,000    10%  Rs.22,500.00
...
TOTAL REVENUE                                 Rs.110,400.00
```
