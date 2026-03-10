# Task 8: API Middleware Simulator
# Approach: Build reusable decorators for timing, logging I/O, and role-based
# access control. All decorators are stackable. Uses logging module (not print).

import time
import logging
import functools

# ---- Setup logging (file + console at same time) ----
logger = logging.getLogger("api_middleware")
logger.setLevel(logging.DEBUG)

# console handler
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.DEBUG)
console_format = logging.Formatter("[%(asctime)s] %(levelname)s - %(message)s", "%H:%M:%S")
console_handler.setFormatter(console_format)

# file handler
file_handler = logging.FileHandler("api_activity.log")
file_handler.setLevel(logging.DEBUG)
file_handler.setFormatter(console_format)

logger.addHandler(console_handler)
logger.addHandler(file_handler)


# ---- Decorator 1: Execution Timer ----
def timer(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        start = time.time()
        result = func(*args, **kwargs)
        end = time.time()
        elapsed = round((end - start) * 1000, 2)
        logger.info(f"[TIMER] '{func.__name__}' executed in {elapsed}ms")
        return result
    return wrapper


# ---- Decorator 2: Input/Output Logger ----
def log_io(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        logger.debug(f"[IO] Calling '{func.__name__}' | args={args} kwargs={kwargs}")
        result = func(*args, **kwargs)
        logger.debug(f"[IO] '{func.__name__}' returned: {result}")
        return result
    return wrapper


# ---- Decorator 3: Role-Based Access Control (with argument) ----
def require_role(allowed_roles):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            # expect first arg or kwarg to be 'user' dict
            user = kwargs.get("user") or (args[0] if args else None)
            if not isinstance(user, dict) or user.get("role") not in allowed_roles:
                role = user.get("role", "none") if isinstance(user, dict) else "none"
                logger.warning(f"[ACCESS DENIED] '{func.__name__}' | Role '{role}' not in {allowed_roles}")
                return {"error": "Access Denied", "required_roles": allowed_roles}
            logger.info(f"[ACCESS OK] '{func.__name__}' | User: {user.get('name')} Role: {user.get('role')}")
            return func(*args, **kwargs)
        return wrapper
    return decorator


# ---- Simulated API functions (original functions untouched) ----

@timer
@log_io
@require_role(["admin", "manager"])
def get_all_users(user):
    # simulate some delay
    time.sleep(0.05)
    return {"users": ["Ali", "Sara", "Bilal", "Fatima"], "count": 4}


@timer
@log_io
@require_role(["admin"])
def delete_user(user, target_id):
    time.sleep(0.02)
    return {"deleted": target_id, "status": "success"}


@timer
@log_io
@require_role(["admin", "manager", "viewer"])
def get_dashboard_stats(user):
    time.sleep(0.03)
    return {"active_users": 120, "orders_today": 45, "revenue": "Rs. 150,000"}


# ---- Test the API middleware ----
print("=" * 58)
print("        API MIDDLEWARE SIMULATOR")
print("=" * 58 + "\n")

admin_user   = {"name": "Ali Hassan",  "role": "admin"}
manager_user = {"name": "Sara Khan",   "role": "manager"}
viewer_user  = {"name": "Hamza Riaz",  "role": "viewer"}
random_user  = {"name": "Unknown Guy", "role": "guest"}

print(">> Test 1: Admin accessing get_all_users")
r1 = get_all_users(user=admin_user)
print(f"   Result: {r1}\n")

print(">> Test 2: Manager accessing get_all_users")
r2 = get_all_users(user=manager_user)
print(f"   Result: {r2}\n")

print(">> Test 3: Viewer trying to access get_all_users (should fail)")
r3 = get_all_users(user=viewer_user)
print(f"   Result: {r3}\n")

print(">> Test 4: Admin deleting a user")
r4 = delete_user(user=admin_user, target_id=42)
print(f"   Result: {r4}\n")

print(">> Test 5: Manager trying to delete a user (should fail)")
r5 = delete_user(user=manager_user, target_id=42)
print(f"   Result: {r5}\n")

print(">> Test 6: Guest accessing dashboard (should fail)")
r6 = get_dashboard_stats(user=random_user)
print(f"   Result: {r6}\n")

print(">> Test 7: Viewer accessing dashboard")
r7 = get_dashboard_stats(user=viewer_user)
print(f"   Result: {r7}\n")

print("\nAll activity saved to: api_activity.log")
