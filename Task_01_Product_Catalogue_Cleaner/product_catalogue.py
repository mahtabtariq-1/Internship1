# Task 1: Product Catalogue Cleaner
# Approach: The supplier gives us a messy list of products with mixed types,
# duplicates, and missing prices. We clean it up, convert prices to float,
# remove duplicates, handle missing values, and group by category.

raw_products = [
    {"name": "Laptop", "category": "Electronics", "price": "75000"},
    {"name": "Mouse", "category": "Electronics", "price": 1500},
    {"name": "Notebook", "category": "Stationery", "price": "200"},
    {"name": "Laptop", "category": "Electronics", "price": "75000"},   # duplicate
    {"name": "Pen", "category": "Stationery", "price": None},          # missing price
    {"name": "Headphones", "category": "Electronics", "price": "3500.50"},
    {"name": "Eraser", "category": "Stationery", "price": ""},         # empty price
    {"name": "Desk Chair", "category": "Furniture", "price": "12000"},
    {"name": "Desk Chair", "category": "Furniture", "price": "12000"}, # duplicate
    {"name": "Keyboard", "category": "Electronics", "price": 2500},
    {"name": "Bookshelf", "category": "Furniture", "price": "8500"},
    {"name": "Ruler", "category": None, "price": "50"},                # missing category
]

print("=" * 50)
print("     PRODUCT CATALOGUE CLEANER")
print("=" * 50)

cleaned = []
seen = set()  # to track duplicates
skipped = []

for item in raw_products:
    name = item.get("name", "").strip()
    category = item.get("category")
    price = item.get("price")

    # skip if no name
    if not name:
        continue

    # handle missing category
    if not category:
        category = "Uncategorized"

    # try to convert price to float
    try:
        if price is None or price == "":
            raise ValueError("missing price")
        price = float(price)
    except (ValueError, TypeError):
        skipped.append(name)
        continue

    # check for duplicate using name+category combo
    key = (name.lower(), category.lower())
    if key in seen:
        continue
    seen.add(key)

    cleaned.append({
        "name": name,
        "category": category,
        "price": price
    })

# group products by category into a dict
catalogue = {}
for product in cleaned:
    cat = product["category"]
    if cat not in catalogue:
        catalogue[cat] = []
    catalogue[cat].append({"name": product["name"], "price": product["price"]})

# print the summary
print(f"\nTotal raw entries   : {len(raw_products)}")
print(f"After cleaning      : {len(cleaned)}")
print(f"Skipped (bad price) : {len(skipped)} -> {skipped}")

print("\n--- Grouped Catalogue ---\n")
for cat, items in catalogue.items():
    print(f"[{cat}]")
    for p in items:
        print(f"   {p['name']:<20} Rs. {p['price']:.2f}")
    print()
