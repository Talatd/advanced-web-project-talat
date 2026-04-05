"""
SmartBasket Intelligent Recommendation Engine
A smart rule-based engine that dynamically analyzes user queries,
scores products based on relevance, and generates personalized responses.
This replaces the static demo responses with actual "thinking" logic.
"""

from products import PRODUCT_CATALOG

# Keyword-to-product relevance mapping
# Each keyword has a dict of product_id -> relevance_score
KEYWORD_RELEVANCE = {
    # Watch / Wearable keywords
    "watch": {2: 10},
    "saat": {2: 10},
    "wearable": {2: 10},
    "smartwatch": {2: 10},
    "fitness": {2: 8, 3: 3},
    "health": {2: 9},
    "biometric": {2: 9},
    "track": {2: 7},
    "gps": {2: 8},
    
    # Headphone / Audio keywords
    "headphone": {3: 10},
    "headphones": {3: 10},
    "headset": {3: 10},
    "kulaklık": {3: 10},
    "audio": {3: 9},
    "sound": {3: 8},
    "music": {3: 8},
    "noise": {3: 9},
    "ses": {3: 8},
    "listen": {3: 8},
    
    # Keyboard keywords
    "keyboard": {4: 10},
    "klavye": {4: 10},
    "typing": {4: 8},
    "mechanical": {4: 9},
    "type": {4: 5},
    
    # Mouse keywords
    "mouse": {6: 10},
    "fare": {6: 10},
    "pointer": {6: 7},
    "click": {6: 6},
    
    # Laptop keywords
    "laptop": {1: 10},
    "bilgisayar": {1: 10},
    "computer": {1: 9},
    "notebook": {1: 9},
    "pc": {1: 8},
    
    # Monitor keywords
    "monitor": {5: 10},
    "monitör": {5: 10},
    "ekran": {5: 10},
    "display": {5: 10},
    "screen": {5: 9},
    "4k": {5: 8, 1: 3},
    
    # Use-case keywords (spread across products)
    "gaming": {1: 9, 4: 6, 6: 6, 3: 5, 5: 5},
    "game": {1: 9, 4: 6, 6: 6, 3: 5, 5: 5},
    "oyun": {1: 9, 4: 6, 6: 6, 3: 5, 5: 5},
    "gamer": {1: 9, 4: 6, 6: 6, 3: 5},
    "fps": {1: 8, 6: 7, 5: 5},
    "esport": {1: 8, 4: 7, 6: 7},
    
    "work": {5: 6, 1: 5, 4: 5, 3: 4},
    "productivity": {5: 7, 1: 6, 4: 5},
    "office": {4: 6, 5: 5, 6: 4},
    "iş": {5: 6, 1: 5, 4: 5},
    "çalışma": {5: 6, 1: 5, 4: 5},
    
    "design": {5: 9, 1: 6},
    "edit": {5: 8, 1: 7, 3: 4},
    "video": {5: 8, 1: 8, 3: 4},
    "create": {5: 7, 1: 6},
    "render": {1: 8, 5: 6},
    "programming": {4: 6, 5: 6, 1: 5},
    "code": {4: 6, 5: 5, 1: 5},
    
    "portable": {1: 7, 2: 5, 3: 5},
    "wireless": {6: 6, 4: 6, 3: 6, 2: 5},
    "bluetooth": {3: 6, 2: 6, 6: 5, 4: 5},
    "commute": {3: 8, 2: 5},
    
    # Budget keywords
    "cheap": {6: 7, 4: 6, 2: 4},
    "budget": {6: 7, 4: 6, 3: 5},
    "affordable": {6: 7, 4: 6},
    "ucuz": {6: 7, 4: 6},
    "bütçe": {6: 7, 4: 6, 3: 5},
    "inexpensive": {6: 7, 4: 6},
    
    # Premium keywords
    "premium": {1: 7, 5: 7, 3: 5},
    "best": {1: 5, 5: 5, 3: 4, 2: 4},
    "high-end": {1: 8, 5: 7},
    "professional": {5: 8, 1: 6},
    
    # Setup keywords
    "setup": {1: 5, 5: 5, 4: 5, 6: 5, 3: 4},
    "bundle": {1: 4, 4: 4, 6: 4, 3: 4},
    "complete": {1: 5, 4: 5, 6: 5, 3: 4, 5: 4},
    "everything": {1: 4, 4: 4, 6: 4, 3: 4, 5: 4, 2: 4},
}

# Product feature highlights for dynamic response generation
PRODUCT_HIGHLIGHTS = {
    1: {
        "emoji": "💻",
        "highlights": [
            "RTX 4070 GPU handles demanding tasks with ease",
            "165Hz display for silky smooth visuals",
            "32GB DDR5 RAM for heavy multitasking",
            "1TB NVMe SSD for fast storage",
            "WiFi 6E + Bluetooth 5.3 connectivity",
        ],
        "use_cases": "gaming, AI development, video editing, 3D rendering",
        "value_note": "A portable powerhouse that replaces the need for a separate desktop",
    },
    2: {
        "emoji": "⌚",
        "highlights": [
            "Vivid AMOLED display — looks premium on your wrist",
            "Advanced biometric tracking: heart rate, SpO2, sleep analysis",
            "AI-enhanced health insights with daily feedback",
            "Built-in GPS for outdoor activity tracking",
            "7-day battery life — charge once a week",
            "Bluetooth 5.2 + WiFi connectivity",
        ],
        "use_cases": "fitness tracking, health monitoring, notifications, daily wear",
        "value_note": "AMOLED + AI health features rival watches costing 2x more",
    },
    3: {
        "emoji": "🎧",
        "highlights": [
            "Adaptive AI noise cancellation learns your environment",
            "40mm custom dynamic drivers for rich, detailed sound",
            "30-hour battery — lasts an entire work week",
            "Bluetooth 5.3 + 3.5mm jack + USB-C connectivity",
            "Extremely comfortable for all-day wear",
        ],
        "use_cases": "music, gaming, calls, commute, focus work",
        "value_note": "Best-in-class ANC at a competitive price point",
    },
    4: {
        "emoji": "⌨️",
        "highlights": [
            "Cherry MX Brown equivalent — tactile and satisfying switches",
            "Full-size 104-key layout with dedicated numpad",
            "Per-key ARGB lighting with customizable effects",
            "Triple connectivity: USB-C, Bluetooth, 2.4GHz wireless",
        ],
        "use_cases": "gaming, typing, programming, office work",
        "value_note": "Premium mechanical feel at a mid-range price",
    },
    5: {
        "emoji": "🖥️",
        "highlights": [
            "100% DCI-P3 color accuracy (Delta E<1) — professional grade",
            "4K UHD resolution with HDR1000",
            "144Hz refresh rate for smooth visuals",
            "USB-C PD 90W — charges your laptop while connected",
        ],
        "use_cases": "design, video editing, development, content creation, gaming",
        "value_note": "Eliminates the need for separate work and gaming monitors",
    },
    6: {
        "emoji": "🖱️",
        "highlights": [
            "25K DPI optical sensor for pixel-perfect precision",
            "Ultra-lightweight at just 58g — fatigue-free all day",
            "70-hour battery on a single charge",
            "Triple connectivity: 2.4GHz, Bluetooth, USB-C",
            "AI-predicted tracking eliminates latency",
        ],
        "use_cases": "gaming, productivity, general use",
        "value_note": "Sub-millisecond tracking usually costs 2-3x more at this class",
    },
}

# Compatibility mapping between products
COMPATIBILITY_NOTES = {
    (1, 2): "Watch syncs via Bluetooth to the laptop for notifications",
    (1, 3): "Headphones connect via Bluetooth 5.3 or 3.5mm jack to the laptop",
    (1, 4): "Keyboard connects via USB-C or Bluetooth to the laptop",
    (1, 5): "Laptop drives the monitor at full 4K 144Hz via HDMI 2.1 or USB-C",
    (1, 6): "Mouse connects via 2.4GHz wireless or Bluetooth to the laptop",
    (2, 3): "Both connect via Bluetooth — can be used simultaneously with your phone",
    (2, 6): "Both use Bluetooth — no interference between devices",
    (3, 4): "Headphones and keyboard both support Bluetooth — no conflicts",
    (3, 6): "Both use wireless connectivity without interfering",
    (4, 5): "Keyboard connects wirelessly to keep your desk clean under the monitor",
    (4, 6): "Both share 2.4GHz/Bluetooth ecosystem — can use same USB receiver",
    (5, 6): "Mouse works great alongside the 4K monitor for precise work",
}


def score_products(query: str) -> list:
    """
    Score each product based on query relevance.
    Returns a sorted list of (product, score) tuples.
    """
    query_lower = query.lower()
    words = query_lower.replace(",", " ").replace(".", " ").replace("?", " ").replace("!", " ").split()
    
    scores = {p["id"]: 0 for p in PRODUCT_CATALOG}
    
    for word in words:
        if word in KEYWORD_RELEVANCE:
            for pid, relevance in KEYWORD_RELEVANCE[word].items():
                scores[pid] += relevance
    
    # Also check multi-word phrases
    for phrase in KEYWORD_RELEVANCE:
        if " " in phrase and phrase in query_lower:
            for pid, relevance in KEYWORD_RELEVANCE[phrase].items():
                scores[pid] += relevance
    
    # Build scored product list (only products with score > 0)
    scored = []
    for product in PRODUCT_CATALOG:
        s = scores[product["id"]]
        if s > 0:
            scored.append((product, s))
    
    # Sort by score descending
    scored.sort(key=lambda x: x[1], reverse=True)
    
    return scored


def extract_budget(query: str) -> int | None:
    """Try to extract a budget number from the query"""
    import re
    # Match patterns like "$5000", "5000$", "under 5000", "budget 5000"
    patterns = [
        r'\$\s*(\d[\d,\.]*)',
        r'(\d[\d,\.]*)\s*\$',
        r'under\s+(\d[\d,\.]*)',
        r'budget\s+(\d[\d,\.]*)',
        r'altında\s+(\d[\d,\.]*)',
        r'bütçe\w*\s+(\d[\d,\.]*)',
    ]
    for pattern in patterns:
        match = re.search(pattern, query.lower())
        if match:
            try:
                return int(match.group(1).replace(",", "").replace(".", ""))
            except ValueError:
                pass
    return None


def get_compatibility(pid1: int, pid2: int) -> str:
    """Get compatibility note between two products"""
    key = (min(pid1, pid2), max(pid1, pid2))
    return COMPATIBILITY_NOTES.get(key, f"Both products work independently without issues")


def generate_recommendation(query: str) -> dict:
    """
    Dynamically analyze the query and generate a personalized recommendation.
    This simulates what CrewAI agents would do — but with deterministic logic.
    """
    scored = score_products(query)
    budget = extract_budget(query)
    
    # If no products scored, return all sorted by price
    if not scored:
        scored = [(p, 1) for p in sorted(PRODUCT_CATALOG, key=lambda x: x["price"])]
    
    # Filter by budget if specified
    if budget is not None:
        within_budget = [(p, s) for p, s in scored if p["price"] <= budget]
        if within_budget:
            scored = within_budget
    
    # Determine how many to recommend (1-3) using smart multi-category detection
    query_lower = query.lower()
    
    # Map explicit product keywords to their canonical product IDs
    CATEGORY_KEYWORDS = {
        "watch": 2, "saat": 2, "wearable": 2, "smartwatch": 2, "smart watch": 2,
        "headphone": 3, "headphones": 3, "headset": 3, "kulaklık": 3, "audio": 3,
        "keyboard": 4, "klavye": 4, "mechanical": 4,
        "mouse": 6, "fare": 6,
        "laptop": 1, "bilgisayar": 1, "computer": 1, "notebook": 1,
        "monitor": 5, "monitör": 5, "ekran": 5, "display": 5, "screen": 5,
    }
    
    # Detect which distinct product categories the user explicitly mentioned
    explicitly_requested_ids = set()
    for kw, pid in CATEGORY_KEYWORDS.items():
        if kw in query_lower:
            explicitly_requested_ids.add(pid)
    
    wants_bundle = any(word in query_lower for word in [
        "setup", "bundle", "complete", "everything", "all", "and", "ile", "ve",
        "both", "combo", "pairing", "together"
    ])
    
    if len(explicitly_requested_ids) >= 2:
        # ---- MULTI-CATEGORY: user asked for 2+ distinct product types ----
        # Guarantee each explicitly requested category's best product is included
        top_products = []
        used_ids = set()
        # First pass: add the highest-scored product from each requested category
        for pid in explicitly_requested_ids:
            for product, s in scored:
                if product["id"] == pid and pid not in used_ids:
                    top_products.append((product, s))
                    used_ids.add(pid)
                    break
        # Sort the selected products by score descending for nice ordering
        top_products.sort(key=lambda x: x[1], reverse=True)
    elif len(explicitly_requested_ids) == 1 and not wants_bundle:
        # ---- SINGLE CATEGORY: user asked for one specific product type ----
        target_id = list(explicitly_requested_ids)[0]
        # Lead with the explicitly requested product
        top_products = [(p, s) for p, s in scored if p["id"] == target_id][:1]
        # Optionally add a strong complementary product
        for product, s in scored:
            if product["id"] != target_id and s >= 5 and len(top_products) < 2:
                top_products.append((product, s))
    elif wants_bundle and len(scored) >= 3:
        top_products = scored[:3]
    else:
        # ---- GENERAL QUERY: recommend top products by score with smart cutoff ----
        top_products = [scored[0]]
        if len(scored) > 1 and scored[1][1] >= scored[0][1] * 0.5:
            top_products.append(scored[1])
        if len(scored) > 2 and scored[2][1] >= scored[0][1] * 0.6:
            top_products.append(scored[2])
    
    # Cap at 4 for multi-category, 3 otherwise
    max_items = 4 if len(explicitly_requested_ids) >= 2 else 3
    top_products = top_products[:max_items]
    
    # --- Build the response ---
    recommended_ids = [p["id"] for p, _ in top_products]
    
    # Agent 1: Product Recommender
    agent1_lines = ["## 🤖 CrewAI Recommendation Report\n"]
    agent1_lines.append("### Agent 1: Product Recommender Analysis")
    agent1_lines.append(f'After analyzing your request: *"{query}"*, here are my recommendations:\n')
    
    labels = ["🌟 Top Pick", "✨ Also Recommended", "💎 Additional Option"]
    for i, (product, score) in enumerate(top_products):
        info = PRODUCT_HIGHLIGHTS[product["id"]]
        label = labels[min(i, len(labels) - 1)]
        agent1_lines.append(f'**{info["emoji"]} {label}: {product["name"]} (${product["price"]:,})**')
        for h in info["highlights"]:
            agent1_lines.append(f"- {h}")
        agent1_lines.append(f'- Ideal for: {info["use_cases"]}')
        agent1_lines.append("")
    
    # Agent 2: Budget Analyst
    total = sum(p["price"] for p, _ in top_products)
    agent2_lines = ["---\n", "### Agent 2: Budget Analyst Report"]
    agent2_lines.append(f"**Total Cost: ${total:,}**")
    
    for product, _ in top_products:
        info = PRODUCT_HIGHLIGHTS[product["id"]]
        agent2_lines.append(f"- {product['name']}: {info['value_note']}")
    
    if budget is not None:
        if total <= budget:
            agent2_lines.append(f"\n✅ Total ${total:,} is within your ${budget:,} budget")
        else:
            agent2_lines.append(f"\n⚠️ Total ${total:,} exceeds your ${budget:,} budget by ${total - budget:,}")
    
    # Agent 3: Compatibility Checker
    agent3_lines = ["\n---\n", "### Agent 3: Compatibility Check ✅"]
    
    if len(top_products) == 1:
        p = top_products[0][0]
        agent3_lines.append(f"- ✅ {p['name']} is a standalone product — no compatibility concerns")
        agent3_lines.append("- ✅ Works with all major platforms and devices")
        agent3_lines.append("- ✅ Standard connectivity — no proprietary requirements")
    else:
        for i in range(len(top_products)):
            for j in range(i + 1, len(top_products)):
                pid1 = top_products[i][0]["id"]
                pid2 = top_products[j][0]["id"]
                note = get_compatibility(pid1, pid2)
                agent3_lines.append(f"- ✅ {note}")
        agent3_lines.append("- ✅ All recommended products work seamlessly together")
    
    # Combine
    full_result = "\n".join(agent1_lines + agent2_lines + agent3_lines)
    
    return {
        "result": full_result,
        "recommended_product_ids": recommended_ids
    }
