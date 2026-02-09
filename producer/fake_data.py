import random

def generate_fake_request():
    return {
        "ip": f"192.168.1.{random.randint(1, 254)}",
        "method": random.choice(["GET", "POST"]),
        "path": random.choice(["/", "/login", "/products", "/cart"]),
        "status": random.choice([200, 200, 200, 404, 500]),
        "user_agent": random.choice([
            "Mozilla/5.0",
            "Chrome/120.0",
            "Safari/537.36"
        ])
    }
