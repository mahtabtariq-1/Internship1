#!/usr/bin/env python3
# Final Project: Academic Portal - Terminal Application
# Approach: Combines ALL concepts - OOP, file handling, exceptions, decorators,
# generators, comprehensions, sorting, asyncio, logging, .env config, custom modules.

import os
import sys
import asyncio
import logging
import functools
import time
from datetime import datetime

# load .env before importing modules
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    print("[WARN] python-dotenv not installed. Using defaults.")

# ensure reports dir exists before logging setup
os.makedirs(os.path.join(os.path.dirname(__file__), "reports"), exist_ok=True)

# ---- Setup Logging ----
log_level = os.getenv("LOG_LEVEL", "INFO")
logging.basicConfig(
    level=getattr(logging, log_level),
    format="[%(asctime)s] %(levelname)s [%(name)s] %(message)s",
    datefmt="%H:%M:%S",
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler("reports/portal.log")
    ]
)
logger = logging.getLogger("portal")

# import custom modules
sys.path.insert(0, os.path.dirname(__file__))

# ensure reports dir exists before logging setup
os.makedirs("reports", exist_ok=True)
from modules import load_students_from_csv, Student, ScholarshipStudent
from modules.exceptions import StudentNotFoundError

PORTAL_NAME   = os.getenv("PORTAL_NAME", "Academic Portal")
PASSING_MARKS = float(os.getenv("PASSING_MARKS", 50))
ADMIN_PASSWORD= os.getenv("ADMIN_PASSWORD", "admin")


# ---- Decorators ----
def log_action(func):
    """Logs every function call with timing."""
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        logger.debug(f"Calling: {func.__name__}")
        start = time.time()
        result = func(*args, **kwargs)
        elapsed = round((time.time() - start) * 1000, 1)
        logger.debug(f"Done: {func.__name__} [{elapsed}ms]")
        return result
    return wrapper

def require_admin(func):
    """Simple admin check decorator."""
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        pwd = input("  Enter admin password: ")
        if pwd != ADMIN_PASSWORD:
            logger.warning(f"Unauthorized access attempt on '{func.__name__}'")
            print("  [!] Access Denied.")
            return
        return func(*args, **kwargs)
    return wrapper


# ---- Generator: yields only failed students ----
def failed_students_stream(students):
    for s in students:
        if "FAIL" in s.status or "RISK" in s.status:
            yield s


# ---- Async: load multiple CSV files concurrently ----
async def load_file_async(filepath):
    """Async wrapper around file loading (simulates async I/O)."""
    logger.info(f"Loading: {filepath}")
    await asyncio.sleep(0.1)   # simulate async I/O delay
    students, errors = load_students_from_csv(filepath)
    return students, errors, os.path.basename(filepath)


async def load_all_files(data_folder):
    """Loads all CSV files in the data folder concurrently."""
    csv_files = [
        os.path.join(data_folder, f)
        for f in os.listdir(data_folder)
        if f.endswith(".csv")
    ]
    if not csv_files:
        logger.warning("No CSV files found in data folder.")
        return [], []

    tasks = [load_file_async(fp) for fp in csv_files]
    results = await asyncio.gather(*tasks)

    all_students = []
    all_errors = []
    for students, errors, fname in results:
        logger.info(f"  {fname}: {len(students)} loaded, {len(errors)} errors")
        all_students.extend(students)
        all_errors.extend(errors)

    return all_students, all_errors


# ---- Report generation ----
@log_action
def generate_report(students, errors):
    """Generates a timestamped text report."""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    report_path = f"reports/report_{timestamp}.txt"

    passed = [s for s in students if s.status == "PASS"]
    failed = list(failed_students_stream(students))
    fined  = [s for s in students if s.fine > 0]

    # sort by average descending using sorted()
    ranked = sorted(students, key=lambda s: s.average, reverse=True)

    # top performers using comprehension
    top3 = [s for s in ranked if s.average >= 80][:3]

    # total fines using reduce-style comprehension
    total_fines = sum(s.fine for s in students)

    with open(report_path, "w") as f:
        f.write(f"{PORTAL_NAME}\n")
        f.write(f"Report Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        f.write("=" * 60 + "\n\n")

        f.write(f"OVERALL SUMMARY\n")
        f.write(f"  Total Students  : {len(students)}\n")
        f.write(f"  Passed          : {len(passed)}\n")
        f.write(f"  Failed          : {len(failed)}\n")
        f.write(f"  Total Fines     : Rs. {total_fines}\n\n")

        f.write("RANKED LIST (by average)\n")
        f.write(f"  {'Rank':<5} {'Name':<22} {'Avg':>5} {'Status'}\n")
        f.write("  " + "-" * 50 + "\n")
        for i, s in enumerate(ranked, 1):
            f.write(f"  {i:<5} {s.name:<22} {s.average:>5} {s.status}\n")

        f.write("\nFAILED STUDENTS\n")
        if failed:
            for s in failed:
                f.write(f"  - {s.name} ({s.person_id}): Avg={s.average} | {s.status}\n")
        else:
            f.write("  None. All students passed!\n")

        f.write("\nFINES\n")
        if fined:
            for s in fined:
                f.write(f"  - {s.name}: {s.late_days} late days -> Rs. {s.fine}\n")
        else:
            f.write("  No fines.\n")

        f.write("\nTOP PERFORMERS (Avg >= 80)\n")
        for s in top3:
            f.write(f"  * {s.name} - {s.average}\n")

        if errors:
            f.write(f"\nERRORS DURING LOADING ({len(errors)})\n")
            for e in errors:
                f.write(f"  [ERR] {e}\n")

    return report_path, len(passed), len(failed), total_fines


# ---- Search by name (binary search on sorted list) ----
@log_action
def search_student(students, name):
    sorted_list = sorted(students, key=lambda s: s.name.lower())
    low, high = 0, len(sorted_list) - 1
    target = name.lower().strip()

    while low <= high:
        mid = (low + high) // 2
        mid_name = sorted_list[mid].name.lower()
        if mid_name == target:
            return sorted_list[mid]
        elif mid_name < target:
            low = mid + 1
        else:
            high = mid - 1
    return None


# ---- Terminal Menu ----
def print_header():
    print("\n" + "=" * 58)
    print(f"   {PORTAL_NAME}")
    print(f"   {datetime.now().strftime('%A, %d %B %Y')}")
    print("=" * 58)

def show_menu():
    print("\n  [1] View All Students")
    print("  [2] Search Student by Name")
    print("  [3] View Failed Students")
    print("  [4] View Fines Report")
    print("  [5] Generate Full Report (Admin)")
    print("  [6] Top 5 by Average")
    print("  [0] Exit")
    return input("\n  Choose option: ").strip()

@log_action
def view_all(students):
    ranked = sorted(students, key=lambda s: s.average, reverse=True)
    print(f"\n  {'#':<4} {'Name':<22} {'Dept':<20} {'Avg':>5}  Status")
    print("  " + "-" * 68)
    for i, s in enumerate(ranked, 1):
        print(f"  {i:<4} {s.name:<22} {s.department:<20} {s.average:>5}  {s.status}")

@log_action
def view_failed(students):
    failed = list(failed_students_stream(students))
    if not failed:
        print("\n  No failed students! Great performance.")
        return
    print(f"\n  Failed Students ({len(failed)}):")
    for s in failed:
        print(f"  -> {s.name} ({s.person_id}) | Avg: {s.average} | {s.status}")

@log_action
def view_fines(students):
    fined = [s for s in students if s.fine > 0]
    if not fined:
        print("\n  No fines. All submissions were on time.")
        return
    total = sum(s.fine for s in fined)
    print(f"\n  {'Name':<22} {'Late Days':>10}  {'Fine':>10}")
    print("  " + "-" * 48)
    for s in fined:
        print(f"  {s.name:<22} {s.late_days:>10}  Rs. {s.fine:>7,.0f}")
    print("  " + "-" * 48)
    print(f"  {'TOTAL':<34} Rs. {total:>7,.0f}")

@log_action
def view_top5(students):
    top = sorted(students, key=lambda s: s.average, reverse=True)[:5]
    print(f"\n  Top 5 Students by Average:")
    for i, s in enumerate(top, 1):
        print(f"  {i}. {s.name:<22} Avg: {s.average}")


# ---- Main Entry Point ----
async def startup():
    print_header()
    print("\nLoading student data...")
    students, errors = await load_all_files("data")

    if not students:
        print("No student data loaded. Exiting.")
        return

    print(f"Loaded {len(students)} student records ({len(errors)} errors)")

    while True:
        choice = show_menu()

        if choice == "1":
            view_all(students)

        elif choice == "2":
            name = input("  Enter student name: ")
            result = search_student(students, name)
            if result:
                print(f"\n  Found:\n{result.get_summary()}")
            else:
                print(f"  Student '{name}' not found.")

        elif choice == "3":
            view_failed(students)

        elif choice == "4":
            view_fines(students)

        elif choice == "5":
            path, passed, failed, fines = generate_report(students, errors)
            print(f"\n  Report saved: {path}")
            print(f"  Passed: {passed} | Failed: {failed} | Total Fines: Rs. {fines}")

        elif choice == "6":
            view_top5(students)

        elif choice == "0":
            print("\n  Goodbye!\n")
            logger.info("Portal session ended.")
            break
        else:
            print("  Invalid option. Try again.")


if __name__ == "__main__":
    asyncio.run(startup())
