# Task 4: E-Commerce Inventory Analyzer
# Approach: Clean messy product data using comprehensions, group by category,
# find top 5 most expensive per category, produce a summary dict.
# Heavy use of list/dict comprehensions, zip, enumerate, map, filter.

print("=" * 55)
print("      E-COMMERCE INVENTORY ANALYZER")
print("=" * 55)

raw_inventory = [
    {"name": "iPhone 15", "category": "Phones", "price": 280000},
    {"name": "Samsung S24", "category": "Phones", "price": 260000},
    {"name": "OnePlus 12", "category": "Phones", "price": 190000},
    {"name": "Redmi Note 13", "category": "Phones", "price": 65000},
    {"name": "Nokia 105", "category": "Phones", "price": 4500},
    {"name": "iPhone 15", "category": "Phones", "price": 280000},   # duplicate
    {"name": "Dell XPS", "category": "Laptops", "price": 350000},
    {"name": "HP Pavilion", "category": "Laptops", "price": 130000},
    {"name": "Lenovo IdeaPad", "category": "Laptops", "price": 95000},
    {"name": "Macbook Air", "category": "Laptops", "price": None},   # missing price
    {"name": "Acer Aspire", "category": "Laptops", "price": 85000},
    {"name": "Sony WH1000", "category": "Audio", "price": 55000},
    {"name": "JBL Tune", "category": "Audio", "price": 8000},
    {"name": "Bose QC45", "category": "Audio", "price": 72000},
    {"name": "boAt Rockerz", "category": "Audio", "price": 3500},
    {"name": "Sennheiser HD", "category": "Audio", "price": 40000},
    {"name": "AirPods Pro", "category": None, "price": 65000},       # missing category
]

# step 1: remove items with no price, fix missing categories
cleaned = [
    {
        "name": p["name"],
        "category": p["category"] if p["category"] else "Other",
        "price": float(p["price"])
    }
    for p in raw_inventory
    if p.get("price") is not None
]

# step 2: remove duplicates using set tracking
seen_keys = set()
unique = []
for p in cleaned:
    k = (p["name"].lower(), p["category"].lower())
    if k not in seen_keys:
        seen_keys.add(k)
        unique.append(p)

# step 3: group by category using dict comprehension
categories = list(set(p["category"] for p in unique))

grouped = {
    cat: sorted(
        [p for p in unique if p["category"] == cat],
        key=lambda x: x["price"],
        reverse=True
    )
    for cat in categories
}

# step 4: top 5 per category
top5 = {cat: items[:5] for cat, items in grouped.items()}

# step 5: summary dict using comprehension
summary = {
    cat: {
        "total_items": len(items),
        "avg_price": round(sum(p["price"] for p in items) / len(items), 2),
        "max_price": max(p["price"] for p in items),
        "min_price": min(p["price"] for p in items),
    }
    for cat, items in grouped.items()
}

print(f"\nTotal products (after cleaning): {len(unique)}\n")

for cat, items in top5.items():
    print(f"[{cat}] - Top {len(items)} most expensive:")
    for i, p in enumerate(items, 1):
        print(f"   {i}. {p['name']:<20} Rs. {p['price']:,.0f}")

print("\n--- Category Summary ---")
for cat, stats in summary.items():
    print(f"\n{cat}:")
    print(f"   Items    : {stats['total_items']}")
    print(f"   Avg Price: Rs. {stats['avg_price']:,.2f}")
    print(f"   Max Price: Rs. {stats['max_price']:,.0f}")
    print(f"   Min Price: Rs. {stats['min_price']:,.0f}")
