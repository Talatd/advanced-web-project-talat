"""
SmartBasket Product Catalog Data
Mirrors the frontend product data for CrewAI agent access
"""

PRODUCT_CATALOG = [
    {
        "id": 1,
        "name": "Quantum R-12 Gaming Laptop",
        "price": 18999,
        "category": "Laptops",
        "description": "High-performance gaming laptop with RTX 4070, perfect for AI development and modern AAA titles.",
        "specs": {
            "gpu": "RTX 4070",
            "display": "15.6 inch 165Hz IPS",
            "ram": "32GB DDR5",
            "storage": "1TB NVMe SSD",
            "connectivity": ["USB-C", "USB-A", "HDMI 2.1", "WiFi 6E", "Bluetooth 5.3"],
            "use_cases": ["gaming", "AI development", "video editing", "3D rendering"]
        }
    },
    {
        "id": 2,
        "name": "Nebula Smart Watch",
        "price": 3299,
        "category": "Wearables",
        "description": "Advanced biometric tracking with AI-enhanced health insights and a vivid AMOLED display.",
        "specs": {
            "display": "1.4 inch AMOLED",
            "sensors": ["heart rate", "SpO2", "sleep tracking", "GPS"],
            "battery": "7 day standby",
            "connectivity": ["Bluetooth 5.2", "WiFi"],
            "use_cases": ["fitness tracking", "health monitoring", "notifications", "daily wear"]
        }
    },
    {
        "id": 3,
        "name": "Aura Noise-Cancelling Headphones",
        "price": 2499,
        "category": "Audio",
        "description": "Immersive sound with adaptive environmental AI noise cancellation and extreme comfort.",
        "specs": {
            "driver": "40mm custom dynamic",
            "anc": "Adaptive AI Noise Cancellation",
            "battery": "30 hours",
            "connectivity": ["Bluetooth 5.3", "3.5mm jack", "USB-C"],
            "use_cases": ["music", "gaming", "calls", "commute", "focus work"]
        }
    },
    {
        "id": 4,
        "name": "Titan Mechanical Keyboard",
        "price": 1299,
        "category": "Peripherals",
        "description": "Tactile, responsive mechanical switches with customizable per-key ARGB lighting.",
        "specs": {
            "switches": "Cherry MX Brown equivalent",
            "layout": "Full-size 104 keys",
            "lighting": "Per-key ARGB",
            "connectivity": ["USB-C wired", "Bluetooth", "2.4GHz wireless"],
            "use_cases": ["gaming", "typing", "programming", "office work"]
        }
    },
    {
        "id": 5,
        "name": "VisionPro 4K Monitor",
        "price": 8500,
        "category": "Monitors",
        "description": "Color-accurate 4K display, HDR1000, tailored for designers, developers, and creators.",
        "specs": {
            "resolution": "3840x2160 4K UHD",
            "panel": "IPS, HDR1000",
            "color": "100% DCI-P3, Delta E<1",
            "refresh_rate": "144Hz",
            "connectivity": ["HDMI 2.1", "DisplayPort 1.4", "USB-C PD 90W"],
            "use_cases": ["design", "video editing", "development", "content creation", "gaming"]
        }
    },
    {
        "id": 6,
        "name": "Atheris Wireless Mouse",
        "price": 899,
        "category": "Peripherals",
        "description": "Ultra-lightweight wireless mouse with sub-millisecond AI-predicted tracking latency.",
        "specs": {
            "sensor": "25K DPI optical",
            "weight": "58g",
            "battery": "70 hours",
            "connectivity": ["2.4GHz wireless", "Bluetooth", "USB-C charging"],
            "use_cases": ["gaming", "productivity", "general use"]
        }
    }
]

def get_catalog_string():
    """Returns a formatted string of the product catalog for LLM consumption"""
    catalog_str = ""
    for p in PRODUCT_CATALOG:
        catalog_str += f"\n--- Product #{p['id']} ---\n"
        catalog_str += f"Name: {p['name']}\n"
        catalog_str += f"Price: ${p['price']}\n"
        catalog_str += f"Category: {p['category']}\n"
        catalog_str += f"Description: {p['description']}\n"
        if 'specs' in p:
            catalog_str += f"Specs: {p['specs']}\n"
    return catalog_str

def get_product_by_name(name):
    """Find a product by partial name match"""
    name_lower = name.lower()
    for p in PRODUCT_CATALOG:
        if name_lower in p['name'].lower():
            return p
    return None

def get_products_by_category(category):
    """Get all products in a category"""
    return [p for p in PRODUCT_CATALOG if p['category'].lower() == category.lower()]
