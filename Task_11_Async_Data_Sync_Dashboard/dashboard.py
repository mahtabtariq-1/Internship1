# Task 11: Async Data Sync Dashboard
# Approach: asyncio to pull data from 3 mock sources simultaneously,
# merge results, display combined summary.
# Credentials stored in .env file, loaded with python-dotenv.
# Run inside: python dashboard.py

import asyncio
import os
import sys

# try loading dotenv
try:
    from dotenv import load_dotenv
    load_dotenv()
    dotenv_loaded = True
except ImportError:
    dotenv_loaded = False
    print("[WARN] python-dotenv not installed. Install with: pip install python-dotenv --break-system-packages")
    print("[WARN] Proceeding with fallback config.\n")

# ---- Load config from .env ----
DB_HOST   = os.getenv("DB_HOST", "localhost")
DB_PORT   = os.getenv("DB_PORT", "5432")
API_KEY   = os.getenv("API_KEY", "no-key")
DB_NAME   = os.getenv("DB_NAME", "unknown")

print("=" * 58)
print("       ASYNC DATA SYNC DASHBOARD")
print("=" * 58)
print(f"\nConfig loaded from .env:")
print(f"  DB_HOST : {DB_HOST}:{DB_PORT}")
print(f"  DB_NAME : {DB_NAME}")
print(f"  API_KEY : {API_KEY[:8]}****")   # hide part of key


# ---- Mock async data sources ----

async def fetch_sales_data():
    """Simulates pulling from a sales database."""
    print("\n[Source 1] Fetching sales data...")
    await asyncio.sleep(1.5)   # simulated network delay
    data = {
        "source": "Sales DB",
        "total_orders": 245,
        "total_revenue": 1850000,
        "top_product": "iPhone 15",
        "avg_order_value": 7551,
    }
    print("[Source 1] Sales data received!")
    return data

async def fetch_inventory_data():
    """Simulates pulling from inventory system."""
    print("[Source 2] Fetching inventory data...")
    await asyncio.sleep(2.0)   # slower source
    data = {
        "source": "Inventory System",
        "total_products": 580,
        "out_of_stock": 23,
        "low_stock_alerts": 45,
        "warehouse_capacity": "68%",
    }
    print("[Source 2] Inventory data received!")
    return data

async def fetch_user_analytics():
    """Simulates pulling from an analytics API."""
    print("[Source 3] Fetching user analytics...")
    await asyncio.sleep(0.8)   # faster source
    data = {
        "source": "Analytics API",
        "active_users_today": 1240,
        "new_signups": 88,
        "bounce_rate": "32%",
        "avg_session": "4m 12s",
    }
    print("[Source 3] Analytics data received!")
    return data


async def merge_and_display(results):
    """Merges the results from all sources and shows a combined dashboard."""
    sales, inventory, analytics = results

    print("\n" + "=" * 58)
    print("          COMBINED DASHBOARD SUMMARY")
    print("=" * 58)

    print("\n[SALES]")
    print(f"  Total Orders     : {sales['total_orders']}")
    print(f"  Total Revenue    : Rs. {sales['total_revenue']:,}")
    print(f"  Avg Order Value  : Rs. {sales['avg_order_value']:,}")
    print(f"  Top Product      : {sales['top_product']}")

    print("\n[INVENTORY]")
    print(f"  Total Products   : {inventory['total_products']}")
    print(f"  Out of Stock     : {inventory['out_of_stock']}")
    print(f"  Low Stock Alerts : {inventory['low_stock_alerts']}")
    print(f"  Warehouse Usage  : {inventory['warehouse_capacity']}")

    print("\n[USER ANALYTICS]")
    print(f"  Active Users     : {analytics['active_users_today']}")
    print(f"  New Signups      : {analytics['new_signups']}")
    print(f"  Bounce Rate      : {analytics['bounce_rate']}")
    print(f"  Avg Session      : {analytics['avg_session']}")

    print("\n[COMBINED ALERTS]")
    if inventory["out_of_stock"] > 20:
        print(f"  *** WARNING: {inventory['out_of_stock']} products are out of stock!")
    if analytics["new_signups"] > 50:
        print(f"  *** GOOD: High signup rate today ({analytics['new_signups']} new users)")
    print("  All sources synced successfully.")


async def main():
    print("\nPulling data from 3 sources simultaneously...\n")

    # gather runs all three concurrently
    results = await asyncio.gather(
        fetch_sales_data(),
        fetch_inventory_data(),
        fetch_user_analytics()
    )

    await merge_and_display(results)
    print("\nDashboard sync complete.")


if __name__ == "__main__":
    asyncio.run(main())
