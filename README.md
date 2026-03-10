# Python Internship Assignment — Python I (Refresher)
**Duration:** 25-Feb-2026 to 06-March-2026

A complete set of 12 Python tasks covering core programming concepts from
data types all the way to concurrency and OOP. Each task is in its own folder
with its own README explaining what it does and how to run it.

---

## Repository Structure

```
├── Task_01_Product_Catalogue_Cleaner/
├── Task_02_Student_Result_Processor/
├── Task_03_Project_Directory_Auditor/
├── Task_04_Ecommerce_Inventory_Analyzer/
├── Task_05_HR_Employee_Ranker/
├── Task_06_Order_Discount_Pipeline/
├── Task_07_Server_Log_Error_Streamer/
├── Task_08_API_Middleware_Simulator/
├── Task_09_Banking_System/
├── Task_10_Library_Management_System/
├── Task_11_Async_Data_Sync_Dashboard/
└── Task_12_Final_Project_Academic_Portal/
```

---

## Task Summary

| # | Task | Topic | Run Command |
|---|------|-------|-------------|
| 01 | Product Catalogue Cleaner | Data Types & Data Structures | `python product_catalogue.py` |
| 02 | Student Result Processor | File Handling & Exceptions | `python student_result_processor.py` |
| 03 | Project Directory Auditor | Built-in & Custom Modules | `python audit.py` |
| 04 | E-Commerce Inventory Analyzer | Algorithms & Comprehensions | `python ecommerce_inventory.py` |
| 05 | HR Employee Ranker | Sorting & Binary Search | `python hr_employee_ranker.py` |
| 06 | Order Discount Pipeline | Lambda, Map, Filter, Reduce | `python order_discount_pipeline.py` |
| 07 | Server Log Error Streamer | Generators & Iterators | `python server_log_streamer.py` |
| 08 | API Middleware Simulator | Decorators & Logging | `python api_middleware.py` |
| 09 | Banking System | OOP Foundations | `python banking_system.py` |
| 10 | Library Management System | Inheritance, Polymorphism & Dunder | `python library_management.py` |
| 11 | Async Data Sync Dashboard | Concurrency & asyncio | `python dashboard.py` |
| 12 | Academic Portal (Final Project) | Everything Combined | `python portal.py` |

---

## Requirements

- Python 3.10 or higher
- `python-dotenv` for Task 11 and Task 12:
  ```bash
  pip install python-dotenv
  ```

---

## Important: How to Run Multi-File Tasks

Tasks 3, 11, and 12 use multiple files/modules. Always navigate into their folder first:

```bash
# Task 3
cd Task_03_Project_Directory_Auditor
python audit.py

# Task 11
cd Task_11_Async_Data_Sync_Dashboard
python dashboard.py

# Task 12
cd Task_12_Final_Project_Academic_Portal
python portal.py
```

For all other tasks, you can run them from anywhere as long as you give the correct path.

---

## Topics Covered

- Built-in data types, type casting, type checking
- Lists, Tuples, Sets, Dictionaries and their methods
- File handling: `open()`, `with`, `csv` module
- Exception handling: `try/except/else/finally`, custom exceptions
- Built-in modules: `os`, `math`, `datetime`
- Custom modules and packages with `__init__.py`
- Big O notation, Bubble/Selection/Insertion Sort
- Binary Search from scratch
- List, dict, set comprehensions
- `lambda`, `map()`, `filter()`, `functools.reduce()`
- Generators with `yield`, `itertools`
- Decorators, `functools.wraps`, stacking decorators
- `logging` module with file and console handlers
- OOP: classes, `__init__`, instance/class attributes, `@property`
- Inheritance: single, multilevel, multiple
- Polymorphism, method overriding, duck typing
- Dunder methods: `__str__`, `__repr__`, `__len__`, `__eq__`, `__lt__`, `__iter__`
- Abstract Base Classes with `abc` module
- `asyncio`: `async def`, `await`, `asyncio.gather()`
- `python-dotenv` for `.env` config files
- `venv` virtual environments
