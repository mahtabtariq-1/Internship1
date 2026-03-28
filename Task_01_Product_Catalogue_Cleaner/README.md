# Task 01 — Product Catalogue Cleaner

## Topic
Data Types, Type Casting and Data Structure

## What This Task Does
A supplier sends a raw product list with mixed types, duplicates, and missing values.
This script cleans the data, converts all prices to float, removes duplicates,
handles missing categories, and groups products into a dictionary by category.

## Concepts Used
- Built-in types: `str`, `float`, `None`
- Type casting: `float()`
- `try / except` for invalid price conversion
- Lists, Sets (for duplicate tracking), Dictionaries
- Dict methods: `.get()`, `.append()`
- String methods: `.strip()`, `.lower()`

## How to Run
```bash
python product_catalogue.py
```

## Sample Output
```
==================================================
     PRODUCT CATALOGUE CLEANER
==================================================

Total raw entries   : 12
After cleaning      : 8
Skipped (bad price) : 2 -> ['Pen', 'Eraser']

--- Grouped Catalogue ---

[Electronics]
   Laptop               Rs. 75000.00
   Mouse                Rs. 1500.00
   ...
```
