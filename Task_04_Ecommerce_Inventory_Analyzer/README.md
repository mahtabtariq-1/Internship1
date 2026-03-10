# Task 04 — E-Commerce Inventory Analyzer

## Topic
Algorithms, Sorting & Comprehensions

## What This Task Does
A shop owner has a messy product list with duplicates, missing prices, and mixed
categories. This script cleans the data, groups by category, finds the top 5 most
expensive items per category, and produces a summary dictionary — written in a
Pythonic style using comprehensions throughout.

## Concepts Used
- List, dict, and set comprehensions
- Conditional comprehensions: `[x for x in lst if condition]`
- `sorted()` with `key` and `reverse`
- Sorting complex objects (list of dicts)
- `set()` for duplicate removal
- `enumerate()` for ranked display
- `min()`, `max()`, `sum()` with generator expressions

## How to Run
```bash
python ecommerce_inventory.py
```

## Sample Output
```
[Phones] - Top 5 most expensive:
   1. iPhone 15             Rs. 280,000
   2. Samsung S24           Rs. 260,000
   ...

--- Category Summary ---
Phones:
   Items    : 5
   Avg Price: Rs. 159,900.00
```
