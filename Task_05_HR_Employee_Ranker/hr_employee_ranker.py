# Task 5: HR Employee Ranker
# Approach: Sort employees by performance score desc, then experience desc
# as tiebreaker, then name alphabetically. Binary search to find an employee.

print("=" * 55)
print("          HR EMPLOYEE RANKER")
print("=" * 55)

employees = [
    {"name": "Zara Malik",   "performance": 88, "experience": 5},
    {"name": "Ali Hassan",   "performance": 95, "experience": 3},
    {"name": "Usman Khan",   "performance": 88, "experience": 7},
    {"name": "Fatima Noor",  "performance": 72, "experience": 6},
    {"name": "Bilal Ahmed",  "performance": 95, "experience": 3},   # tiebreaker by name
    {"name": "Sana Javed",   "performance": 65, "experience": 9},
    {"name": "Hamza Riaz",   "performance": 72, "experience": 6},   # tiebreaker by name
    {"name": "Nida Shah",    "performance": 80, "experience": 4},
]

# sort: performance desc, experience desc, name asc
ranked = sorted(
    employees,
    key=lambda e: (-e["performance"], -e["experience"], e["name"])
)

print("\nEmployee Rankings:")
print(f"{'Rank':<6} {'Name':<20} {'Score':>7} {'Exp':>5}")
print("-" * 45)
for i, emp in enumerate(ranked, 1):
    print(f"{i:<6} {emp['name']:<20} {emp['performance']:>7} {emp['experience']:>5} yrs")

# Binary search by name (list must be sorted by name for binary search)
name_sorted = sorted(ranked, key=lambda e: e["name"].lower())

def binary_search_employee(lst, target):
    low = 0
    high = len(lst) - 1
    target = target.lower()

    while low <= high:
        mid = (low + high) // 2
        mid_name = lst[mid]["name"].lower()

        if mid_name == target:
            return lst[mid]
        elif mid_name < target:
            low = mid + 1
        else:
            high = mid - 1

    return None

# search example
search_name = "Hamza Riaz"
result = binary_search_employee(name_sorted, search_name)

print(f"\nSearching for: '{search_name}'")
if result:
    rank_pos = next(i+1 for i, e in enumerate(ranked) if e["name"] == result["name"])
    print(f"Found! Name: {result['name']}, Score: {result['performance']}, "
          f"Exp: {result['experience']} yrs, Rank: #{rank_pos}")
else:
    print("Employee not found.")
