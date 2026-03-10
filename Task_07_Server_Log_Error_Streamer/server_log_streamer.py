# Task 7: Server Log Error Streamer
# Approach: Simulate a large log file with a generator. Read line by line,
# yield only critical/error entries, group by error type, show running count.
# No full file loading into memory.

import itertools
import random

# ---- Simulate writing a large log file ----
def create_sample_log(filepath, num_lines=200):
    levels = ["INFO", "DEBUG", "WARNING", "ERROR", "CRITICAL", "INFO", "INFO", "DEBUG"]
    error_types = [
        "NullPointerException",
        "DatabaseConnectionError",
        "TimeoutError",
        "AuthenticationFailure",
        "NullPointerException",   # repeated to show grouping
        "DatabaseConnectionError",
    ]
    services = ["auth-service", "payment-api", "user-service", "db-handler"]

    with open(filepath, "w") as f:
        for i in range(1, num_lines + 1):
            level = random.choice(levels)
            service = random.choice(services)
            if level in ("ERROR", "CRITICAL"):
                err = random.choice(error_types)
                line = f"[2026-03-08 {i:02d}:{random.randint(0,59):02d}:00] {level} [{service}] {err}: Something went wrong at line {i}\n"
            else:
                line = f"[2026-03-08 {i:02d}:{random.randint(0,59):02d}:00] {level} [{service}] Request handled successfully - req_id={i}\n"
            f.write(line)

create_sample_log("server.log")

# ---- Generator: reads log line by line, yields only error/critical ----
def stream_errors(filepath):
    """Generator that yields only ERROR and CRITICAL lines."""
    try:
        with open(filepath, "r") as f:
            for line in f:
                line = line.strip()
                if "ERROR" in line or "CRITICAL" in line:
                    yield line
    except FileNotFoundError:
        print(f"Log file not found: {filepath}")
        return

# ---- Extract error type from a log line ----
def get_error_type(line):
    # lines have format: [...] LEVEL [service] ErrorType: ...
    parts = line.split("]")
    if len(parts) >= 3:
        rest = parts[2].strip()
        # get first word (error type name)
        err = rest.split(":")[0].strip()
        return err
    return "Unknown"

# ---- Main streaming logic ----
print("=" * 58)
print("        SERVER LOG ERROR STREAMER")
print("=" * 58)
print("Streaming errors from server.log...\n")

error_groups = {}
running_count = 0

error_stream = stream_errors("server.log")

# use itertools.islice to show live first 10 errors, then count rest
print(f"{'Count':<7} {'Level':<10} {'Error Type':<28} {'Service'}")
print("-" * 70)

for line in error_stream:
    running_count += 1
    err_type = get_error_type(line)

    # group by error type
    if err_type not in error_groups:
        error_groups[err_type] = 0
    error_groups[err_type] += 1

    # extract level and service for display
    try:
        level = line.split("]")[1].strip().split("[")[0].strip()
        service = line.split("[")[2].split("]")[0]
    except IndexError:
        level = "?"
        service = "?"

    # show live running count for each error
    print(f"#{running_count:<6} {level:<10} {err_type:<28} {service}")

print("\n" + "=" * 58)
print("SUMMARY - Errors by Type:")
print("-" * 40)
# sort by count descending
sorted_groups = sorted(error_groups.items(), key=lambda x: x[1], reverse=True)
for err_type, count in sorted_groups:
    bar = "#" * count
    print(f"  {err_type:<28}: {count:>3} {bar}")

print(f"\nTotal critical/error entries: {running_count}")
print("(File was read line by line — no full load into memory)")
