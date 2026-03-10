# Task 6: Order Discount Pipeline
# Approach: Use map(), filter(), and functools.reduce() with lambda functions
# to build a pipeline — no traditional for loops anywhere.
# Orders get category-based discounts, low-value orders filtered out,
# then total revenue calculated.

from functools import reduce

print("=" * 55)
print("        ORDER DISCOUNT PIPELINE")
print("=" * 55)

raw_orders = [
    {"id": "ORD001", "customer": "Ali",    "category": "Electronics", "amount": 25000},
    {"id": "ORD002", "customer": "Sara",   "category": "Clothing",    "amount": 3500},
    {"id": "ORD003", "customer": "Bilal",  "category": "Food",        "amount": 850},
    {"id": "ORD004", "customer": "Fatima", "category": "Electronics", "amount": 72000},
    {"id": "ORD005", "customer": "Hamza",  "category": "Clothing",    "amount": 1200},
    {"id": "ORD006", "customer": "Nida",   "category": "Food",        "amount": 420},
    {"id": "ORD007", "customer": "Usman",  "category": "Electronics", "amount": 9000},
    {"id": "ORD008", "customer": "Zara",   "category": "Clothing",    "amount": 6800},
    {"id": "ORD009", "customer": "Hassan", "category": "Food",        "amount": 5500},
    {"id": "ORD010", "customer": "Aisha",  "category": "Electronics", "amount": 500},  # too low
]

# discount rules by category
discount_rules = {
    "Electronics": 0.10,  # 10% off
    "Clothing":    0.15,  # 15% off
    "Food":        0.05,  # 5% off
}

MIN_ORDER = 1000  # filter out orders below this

# Step 1: Apply discount using map + lambda
apply_discount = lambda order: {
    **order,
    "discount_pct": discount_rules.get(order["category"], 0),
    "discounted_amount": round(
        order["amount"] * (1 - discount_rules.get(order["category"], 0)), 2
    )
}

discounted_orders = list(map(apply_discount, raw_orders))

# Step 2: Filter out orders below minimum threshold
filtered_orders = list(filter(
    lambda o: o["discounted_amount"] >= MIN_ORDER,
    discounted_orders
))

# Step 3: Calculate total revenue using reduce
total_revenue = reduce(
    lambda acc, o: acc + o["discounted_amount"],
    filtered_orders,
    0
)

# Step 4: Sort by discounted amount descending (using sorted + lambda)
final_orders = sorted(filtered_orders, key=lambda o: o["discounted_amount"], reverse=True)

# ---- Print Results ----
print(f"\nTotal orders received : {len(raw_orders)}")
print(f"After filtering (<Rs. {MIN_ORDER}): {len(filtered_orders)}")

print(f"\n{'ID':<8} {'Customer':<12} {'Category':<14} {'Original':>10} {'Disc%':>6} {'Final':>10}")
print("-" * 65)
for o in final_orders:
    print(f"{o['id']:<8} {o['customer']:<12} {o['category']:<14} "
          f"Rs.{o['amount']:>8,}  {int(o['discount_pct']*100):>4}%  Rs.{o['discounted_amount']:>8,.2f}")

print("-" * 65)
print(f"{'TOTAL REVENUE':<45} Rs.{total_revenue:>8,.2f}")

removed = list(filter(lambda o: o["discounted_amount"] < MIN_ORDER, discounted_orders))
print(f"\nRemoved orders (below threshold):")
list(map(lambda o: print(f"  - {o['id']} ({o['customer']}): Rs. {o['discounted_amount']}"), removed))
