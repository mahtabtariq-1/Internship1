# Task 10 — Library Management System

## Topic
OOP: Inheritance, Polymorphism & Dunder Methods

## What This Task Does
A library system that manages books, members, and borrowing records.
Books are borrowed and returned. Members have borrow limits. Overdue books trigger
fines. Different membership tiers have different rules and privileges.

## Class Hierarchy
```
Person (Abstract Base Class)
└── Member (Abstract)
    └── BasicMember      ← 2 books max, Rs. 20/day fine
        └── PremiumMember  ← 5 books max, 50% fine discount
            └── VIPMember    ← 10 books max, 3-day grace + Rs. 5/day
```

## Concepts Used
- Single Inheritance, Multilevel Inheritance
- Method Overriding (`calculate_fine` per tier)
- `super()` to call parent methods
- `abc` module and `@abstractmethod`
- Duck typing in practice
- Dunder methods: `__str__`, `__repr__`, `__len__`, `__lt__`, `__iter__`, `__getitem__`, `__eq__`

## How to Run
```bash
python library_management.py
```

## Sample Output
```
[OK] Ali Hassan borrowed 'Clean Code'
[RETURN] 'Python Crash Course' returned by Ali Hassan | Overdue: 6 days | Fine: Rs. 120
[RETURN] 'The Pragmatic Programmer' returned by Sara Khan | Overdue: 11 days | Fine: Rs. 110.0
```
