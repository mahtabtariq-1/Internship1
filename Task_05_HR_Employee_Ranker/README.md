# Task 05 — HR Employee Ranker

## Topic
Algorithms, Sorting & Comprehensions

## What This Task Does
HR wants employees ranked by performance score, then by experience as a tiebreaker,
then by name alphabetically. The system also supports quickly searching for a specific
employee by name using Binary Search.

## Concepts Used
- `sorted()` with multi-key `lambda`
- Sorting with `key` and `reverse`
- Sorting complex objects (list of dicts)
- Binary Search implementation from scratch
- `enumerate()` for rank display

## How to Run
```bash
python hr_employee_ranker.py
```

## Sample Output
```
Employee Rankings:
Rank   Name                   Score   Exp
---------------------------------------------
1      Ali Hassan                95     3 yrs
2      Bilal Ahmed               95     3 yrs
3      Usman Khan                88     7 yrs
...

Searching for: 'Hamza Riaz'
Found! Name: Hamza Riaz, Score: 72, Exp: 6 yrs, Rank: #7
```
