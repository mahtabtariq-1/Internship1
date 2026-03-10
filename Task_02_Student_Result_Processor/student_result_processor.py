# Task 2: Student Result Processor
# Approach: We simulate a folder with CSV files. Some are corrupted, some missing,
# some have invalid data. We read each file safely using try/except, flag failed
# students (marks < 50), and write a clean results file.

import csv
import os

# ---- Custom Exception ----
class InvalidRecordError(Exception):
    pass

# ---- Setup: create sample CSV files to simulate the folder ----
def setup_sample_files():
    os.makedirs("student_files", exist_ok=True)

    # valid file 1
    with open("student_files/class_A.csv", "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["name", "roll_no", "marks"])
        writer.writerows([
            ["Ali Hassan", "101", "78"],
            ["Sara Khan", "102", "45"],
            ["Bilal Ahmed", "103", "91"],
            ["Fatima", "104", "33"],
        ])

    # valid file 2
    with open("student_files/class_B.csv", "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["name", "roll_no", "marks"])
        writer.writerows([
            ["Usman Ali", "201", "60"],
            ["Zara Malik", "202", "abc"],   # invalid marks
            ["Hamza", "203", "55"],
            ["Nida", "204", ""],             # empty marks
        ])

    # corrupted file (bad format)
    with open("student_files/class_C.csv", "w") as f:
        f.write("this is not a valid csv file!!!\n@@@###\n")

    # empty file
    with open("student_files/class_D.csv", "w") as f:
        f.write("")

setup_sample_files()

# ---- Main Processing ----
folder = "student_files"
all_results = []
error_log = []

print("=" * 55)
print("        STUDENT RESULT PROCESSOR")
print("=" * 55)

files = os.listdir(folder)

for filename in files:
    if not filename.endswith(".csv"):
        continue

    filepath = os.path.join(folder, filename)
    print(f"\nReading: {filename}")

    try:
        with open(filepath, "r") as f:
            reader = csv.DictReader(f)

            if reader.fieldnames is None:
                raise InvalidRecordError("File is empty or has no headers")

            for row in reader:
                try:
                    name = row.get("name", "").strip()
                    roll = row.get("roll_no", "").strip()
                    marks_raw = row.get("marks", "").strip()

                    if not name or not roll:
                        raise InvalidRecordError(f"Missing name/roll in row: {row}")

                    marks = float(marks_raw)

                    status = "PASS" if marks >= 50 else "FAIL"
                    all_results.append({
                        "name": name,
                        "roll_no": roll,
                        "marks": marks,
                        "status": status,
                        "source": filename
                    })
                    print(f"  -> {name} ({roll}): {marks} [{status}]")

                except (ValueError, TypeError):
                    msg = f"  [SKIP] Invalid marks for {row.get('name','?')} in {filename}"
                    print(msg)
                    error_log.append(msg)

                except InvalidRecordError as e:
                    msg = f"  [SKIP] {e}"
                    print(msg)
                    error_log.append(msg)

    except FileNotFoundError:
        msg = f"  [ERROR] File not found: {filename}"
        print(msg)
        error_log.append(msg)

    except InvalidRecordError as e:
        msg = f"  [ERROR] {e} in {filename}"
        print(msg)
        error_log.append(msg)

    except Exception as e:
        msg = f"  [ERROR] Could not read {filename}: {e}"
        print(msg)
        error_log.append(msg)

# ---- Write clean results to output file ----
output_file = "clean_results.csv"
with open(output_file, "w", newline="") as f:
    writer = csv.DictWriter(f, fieldnames=["name", "roll_no", "marks", "status", "source"])
    writer.writeheader()
    writer.writerows(all_results)

# ---- Final Summary ----
passed = [s for s in all_results if s["status"] == "PASS"]
failed = [s for s in all_results if s["status"] == "FAIL"]

print("\n" + "=" * 55)
print("SUMMARY")
print("=" * 55)
print(f"Total processed : {len(all_results)}")
print(f"Passed          : {len(passed)}")
print(f"Failed          : {len(failed)}")
print(f"\nFailed Students:")
for s in failed:
    print(f"  - {s['name']} (Roll: {s['roll_no']}) -> {s['marks']} marks")

print(f"\nClean results saved to: {output_file}")

if error_log:
    print(f"\nErrors/Skipped ({len(error_log)}):")
    for e in error_log:
        print(e)
