"""
SmartBasket CrewAI Backend Server
FastAPI server that exposes the CrewAI recommendation engine to the React frontend.
Handles CORS, request validation, and provides both real CrewAI and demo endpoints.
"""

import os
import json
import re
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

app = FastAPI(
    title="SmartBasket CrewAI API",
    description="AI-powered shopping recommendation API using CrewAI multi-agent system",
    version="1.0.0"
)

# CORS middleware - allow React dev server
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins (dev mode)
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class QueryRequest(BaseModel):
    """Request model for AI recommendation queries"""
    query: str


class RecommendationResponse(BaseModel):
    """Response model for AI recommendations"""
    success: bool
    query: str
    result: str
    recommended_product_ids: list
    agent_info: dict


# =====================================================
#  DEMO MODE: Simulated CrewAI responses
#  (Used when OpenAI API key is not configured)
# =====================================================

DEMO_RESPONSES = {
    "gaming": {
        "result": """## 🎮 CrewAI Recommendation Report

### Agent 1: Product Recommender Analysis
After analyzing your gaming needs, I've identified the best products from our catalog:

**🔥 Top Pick: Quantum R-12 Gaming Laptop ($18,999)**
- RTX 4070 GPU handles all modern AAA titles at ultra settings
- 165Hz display for smooth competitive gaming
- 32GB DDR5 RAM for multitasking while streaming

**🎧 Essential Add-on: Aura Noise-Cancelling Headphones ($2,499)**
- Immersive audio with spatial sound for competitive advantage
- AI noise cancellation blocks out distractions
- 30-hour battery for marathon gaming sessions

**⌨️ Recommended: Titan Mechanical Keyboard ($1,299)**
- Cherry MX Brown switches for precise, tactile gaming input
- Per-key ARGB lighting syncs with your games
- Wireless & wired connectivity options

---

### Agent 2: Budget Analyst Report
**Total Bundle Cost: $22,797**
- This is a premium gaming setup with excellent value per component
- The Quantum R-12 alone replaces the need for a separate desktop
- Bundle savings recommendation: All three items complement each other perfectly

---

### Agent 3: Compatibility Check ✅
All products are fully compatible:
- ✅ Headphones connect via Bluetooth 5.3 to the laptop
- ✅ Keyboard connects via USB-C or Bluetooth to the laptop
- ✅ All products support the same wireless ecosystem
- ✅ No additional adapters or accessories needed""",
        "recommended_product_ids": [1, 3, 4]
    },
    "productivity": {
        "result": """## 💼 CrewAI Recommendation Report

### Agent 1: Product Recommender Analysis
For your productivity setup, I recommend the following curated selections:

**🖥️ Top Pick: VisionPro 4K Monitor ($8,500)**
- 100% DCI-P3 color accuracy (Delta E<1) for precise work
- 4K UHD resolution gives you maximum screen real estate
- USB-C PD 90W charges your laptop while connected
- HDR1000 for stunning visual clarity

**💻 Power Base: Quantum R-12 Gaming Laptop ($18,999)**
- 32GB DDR5 RAM handles heavy multitasking
- RTX 4070 accelerates rendering and AI workloads
- Connects seamlessly to the VisionPro via USB-C or HDMI 2.1

**⌨️ Comfort Essential: Titan Mechanical Keyboard ($1,299)**
- Cherry MX Brown tactile switches reduce typing fatigue
- Full-size layout with numpad for data entry
- Wireless connectivity keeps desktop clean

---

### Agent 2: Budget Analyst Report
**Total Bundle Cost: $28,798**
- Premium workstation-class setup at consumer prices
- The monitor alone is worth the investment for professional color work
- USB-C PD on monitor eliminates the need for a separate charger

---

### Agent 3: Compatibility Check ✅
- ✅ Laptop HDMI 2.1 drives the monitor at full 4K 144Hz
- ✅ USB-C PD charges laptop from monitor (single cable setup!)
- ✅ Keyboard connects wirelessly via Bluetooth or included USB dongle
- ✅ All peripherals support multi-device switching""",
        "recommended_product_ids": [5, 1, 4]
    },
    "default": {
        "result": """## 🤖 CrewAI Recommendation Report

### Agent 1: Product Recommender Analysis
Based on your requirements, here are my top recommendations from SmartBasket:

**🌟 Versatile Choice: Quantum R-12 Gaming Laptop ($18,999)**
- Handles everything from gaming to content creation
- RTX 4070 GPU and 32GB DDR5 RAM
- Portable powerhouse for any use case

**🎧 Daily Companion: Aura Noise-Cancelling Headphones ($2,499)**
- AI-powered noise cancellation adapts to your environment
- Premium audio quality for work calls and entertainment
- 30-hour battery outlasts your workday

**⌚ Smart Addition: Nebula Smart Watch ($3,299)**
- AI-enhanced health insights and biometric tracking
- Stay connected with notifications without touching your phone
- GPS tracking and 7-day battery life

---

### Agent 2: Budget Analyst Report
**Total Bundle Cost: $24,797**
- Balanced tech ecosystem covering work, play, and fitness
- Each product serves a distinct purpose with no overlap
- Best value combination for an all-inclusive tech upgrade

---

### Agent 3: Compatibility Check ✅
- ✅ Watch syncs via Bluetooth to the laptop
- ✅ Headphones connect via Bluetooth 5.3 or 3.5mm jack
- ✅ All devices support simultaneous Bluetooth connections
- ✅ Complete ecosystem with no compatibility issues""",
        "recommended_product_ids": [1, 3, 2]
    },
    "budget": {
        "result": """## 💰 CrewAI Recommendation Report (Budget-Friendly)

### Agent 1: Product Recommender Analysis
I've selected the best value products within a budget-conscious approach:

**🖱️ Best Value: Atheris Wireless Mouse ($899)**
- Sub-millisecond AI-predicted tracking at this price point is unbeatable
- Ultra-lightweight 58g design for all-day comfort
- 70-hour battery life and triple connectivity (2.4GHz, Bluetooth, USB-C)

**⌨️ Smart Pairing: Titan Mechanical Keyboard ($1,299)**
- Premium mechanical switches typically cost much more
- Per-key ARGB lighting adds a premium feel
- Triple connectivity matches the mouse ecosystem

**🎧 Quality Audio: Aura Noise-Cancelling Headphones ($2,499)**
- Best-in-class AI noise cancellation
- 30 hours battery - charge once a week
- Versatile: great for work, gaming, and commute

---

### Agent 2: Budget Analyst Report
**Total Bundle Cost: $4,697**
- Exceptional value peripheral setup under $5,000
- Each product is best-in-class for its price range
- These peripherals will last 3-5 years minimum

---

### Agent 3: Compatibility Check ✅
- ✅ Mouse and keyboard both support 2.4GHz wireless (can share receiver concepts)
- ✅ Headphones work via Bluetooth alongside wireless peripherals
- ✅ All charge via USB-C (one cable type for everything!)
- ✅ Compatible with any laptop or desktop system""",
        "recommended_product_ids": [6, 4, 3]
    },
    "monitor": {
        "result": """## 🖥️ CrewAI Recommendation Report

### Agent 1: Product Recommender Analysis
For a monitor-focused setup, here is the optimal recommendation:

**🖥️ Top Pick: VisionPro 4K Monitor ($8,500)**
- Professional-grade 100% DCI-P3 color accuracy
- HDR1000 with local dimming for stunning contrast
- 144Hz refresh rate - smooth for both design work and gaming
- USB-C PD 90W lets you charge a laptop while using it as a display

**🖱️ Desk Companion: Atheris Wireless Mouse ($899)**
- Perfect complement for precise design work
- 25K DPI optical sensor for pixel-perfect accuracy
- Ultra-lightweight for long editing sessions

---

### Agent 2: Budget Analyst Report
**Total Bundle Cost: $9,399**
- The VisionPro is a long-term investment for any creative professional
- At 144Hz with HDR1000, it eliminates the need for separate gaming/work monitors
- The Atheris mouse adds premium precision at a fraction of the monitor's cost

---

### Agent 3: Compatibility Check ✅
- ✅ Monitor supports HDMI 2.1, DisplayPort 1.4, and USB-C
- ✅ Mouse connects wirelessly (no cable clutter on a clean desk setup)
- ✅ USB-C PD means single-cable laptop connectivity
- ✅ Both products are universally compatible with all major systems""",
        "recommended_product_ids": [5, 6]
    },
    "wearable": {
        "result": """## ⌚ CrewAI Recommendation Report

### Agent 1: Product Recommender Analysis
After analyzing your request for a smart watch / wearable, here is my top recommendation:

**⌚ Top Pick: Nebula Smart Watch ($3,299)**
- Stunning vivid AMOLED display — looks premium on your wrist
- Advanced biometric tracking: heart rate, SpO2, sleep analysis
- AI-enhanced health insights give you actionable daily feedback
- Built-in GPS for accurate outdoor activity tracking
- 7-day battery life — charge once a week
- Bluetooth 5.2 + WiFi for seamless phone connectivity
- Stylish design suitable for both sport and formal wear

This is the only smart wearable in our catalog and it is an outstanding choice for anyone looking for a premium, stylish, and feature-rich smart watch.

---

### Agent 2: Budget Analyst Report
**Total Cost: $3,299**
- The Nebula Smart Watch is competitively priced for its feature set
- AMOLED display + AI health features rival watches costing 2x more
- At this price point, you get flagship-level biometrics and GPS
- Excellent long-term value with 7-day battery reducing daily hassle

---

### Agent 3: Compatibility Check ✅
- ✅ Watch connects via Bluetooth 5.2 to any smartphone (iOS/Android)
- ✅ Built-in WiFi allows standalone notifications
- ✅ Standalone GPS — no phone needed for outdoor tracking
- ✅ Standard magnetic charger — no proprietary cables
- ✅ Full ecosystem compatibility with all major platforms""",
        "recommended_product_ids": [2]
    },
    "headphone": {
        "result": """## 🎧 CrewAI Recommendation Report

### Agent 1: Product Recommender Analysis
You're looking for audio gear — here's the best option in our catalog:

**🎧 Top Pick: Aura Noise-Cancelling Headphones ($2,499)**
- Adaptive AI noise cancellation that learns your environment
- 40mm custom dynamic drivers for rich, detailed sound
- 30-hour battery life — lasts an entire work week
- Bluetooth 5.3 + 3.5mm jack + USB-C connectivity
- Incredibly comfortable for all-day wear
- Perfect for music, gaming, calls, commute, and focus work

**⌚ Smart Companion: Nebula Smart Watch ($3,299)**
- Control your music playback directly from your wrist
- Track your listening habits alongside health metrics
- Bluetooth connectivity pairs seamlessly with the headphones

---

### Agent 2: Budget Analyst Report
**Total Bundle Cost: $5,798**
- The Aura headphones alone are an excellent value at $2,499
- Best-in-class ANC at this price point
- The watch adds smart control and health tracking

---

### Agent 3: Compatibility Check ✅
- ✅ Headphones support multipoint Bluetooth — connect to two devices at once
- ✅ 3.5mm jack provides universal wired backup
- ✅ USB-C charging matches modern device ecosystem
- ✅ Watch and headphones coexist on Bluetooth without interference""",
        "recommended_product_ids": [3, 2]
    },
    "keyboard": {
        "result": """## ⌨️ CrewAI Recommendation Report

### Agent 1: Product Recommender Analysis
For a keyboard-focused recommendation, here's the perfect setup:

**⌨️ Top Pick: Titan Mechanical Keyboard ($1,299)**
- Cherry MX Brown equivalent switches — tactile and satisfying
- Full-size 104-key layout with dedicated numpad
- Per-key ARGB lighting with customizable effects
- Triple connectivity: USB-C wired, Bluetooth, and 2.4GHz wireless
- Built for gaming, typing, programming, and office work

**🖱️ Perfect Pairing: Atheris Wireless Mouse ($899)**
- Complete your desk setup with a matching wireless mouse
- 25K DPI optical sensor for precise control
- Ultra-lightweight 58g for all-day comfort
- Same triple connectivity as the keyboard

---

### Agent 2: Budget Analyst Report
**Total Bundle Cost: $2,198**
- Very affordable premium peripheral bundle
- Both products offer triple connectivity — rare at this price
- Mechanical keyboard + precision mouse = complete desk upgrade

---

### Agent 3: Compatibility Check ✅
- ✅ Both devices support 2.4GHz, Bluetooth, and USB-C
- ✅ Can share a single USB receiver for wireless
- ✅ USB-C charging for both — one cable type
- ✅ Compatible with Windows, macOS, and Linux""",
        "recommended_product_ids": [4, 6]
    },
    "mouse": {
        "result": """## 🖱️ CrewAI Recommendation Report

### Agent 1: Product Recommender Analysis
Looking for a mouse? Here's the best option in our catalog:

**🖱️ Top Pick: Atheris Wireless Mouse ($899)**
- 25K DPI optical sensor — pixel-perfect precision
- Ultra-lightweight at just 58g for fatigue-free use
- 70-hour battery on a single charge
- Triple connectivity: 2.4GHz wireless, Bluetooth, USB-C
- AI-predicted tracking eliminates latency
- Perfect for gaming, productivity, and general use

**⌨️ Ideal Companion: Titan Mechanical Keyboard ($1,299)**
- Complete your input setup with a premium mechanical keyboard
- Matching wireless ecosystem (2.4GHz + Bluetooth + USB-C)
- Per-key ARGB lighting enhances your desk aesthetic

---

### Agent 2: Budget Analyst Report
**Total Bundle Cost: $2,198**
- The Atheris mouse alone at $899 is outstanding value
- Sub-millisecond tracking usually costs 2-3x more
- Adding the keyboard creates a cohesive premium setup under $2,200

---

### Agent 3: Compatibility Check ✅
- ✅ Mouse and keyboard share the same wireless technology
- ✅ Both charge via USB-C
- ✅ Bluetooth allows connection to multiple devices
- ✅ Platform agnostic — works with any OS""",
        "recommended_product_ids": [6, 4]
    }
}


def get_demo_response(query: str) -> dict:
    """Get a simulated CrewAI response based on keyword matching"""
    query_lower = query.lower()
    
    if any(word in query_lower for word in ["watch", "saat", "wearable", "fitness", "health", "biometric", "smartwatch", "smart watch"]):
        return DEMO_RESPONSES["wearable"]
    elif any(word in query_lower for word in ["headphone", "headset", "audio", "sound", "music", "noise cancel", "kulaklık", "ses"]):
        return DEMO_RESPONSES["headphone"]
    elif any(word in query_lower for word in ["keyboard", "klavye", "typing", "mechanical"]):
        return DEMO_RESPONSES["keyboard"]
    elif any(word in query_lower for word in ["mouse", "fare", "tracking", "pointer"]):
        return DEMO_RESPONSES["mouse"]
    elif any(word in query_lower for word in ["game", "gaming", "gamer", "fps", "esport", "oyun"]):
        return DEMO_RESPONSES["gaming"]
    elif any(word in query_lower for word in ["work", "productivity", "office", "professional", "edit", "design", "create", "iş", "çalışma"]):
        return DEMO_RESPONSES["productivity"]
    elif any(word in query_lower for word in ["cheap", "budget", "affordable", "under", "inexpensive", "save", "ucuz", "bütçe"]):
        return DEMO_RESPONSES["budget"]
    elif any(word in query_lower for word in ["monitor", "display", "screen", "4k", "ekran", "monitör"]):
        return DEMO_RESPONSES["monitor"]
    elif any(word in query_lower for word in ["laptop", "bilgisayar", "computer", "notebook"]):
        return DEMO_RESPONSES["gaming"]
    else:
        return DEMO_RESPONSES["default"]


def extract_product_ids(result_text: str) -> list:
    """Extract product IDs mentioned in the result text"""
    # Try to find product names and map to IDs
    product_map = {
        "quantum": 1, "laptop": 1,
        "nebula": 2, "watch": 2, "wearable": 2,
        "aura": 3, "headphone": 3, "audio": 3,
        "titan": 4, "keyboard": 4,
        "visionpro": 5, "monitor": 5, "display": 5,
        "atheris": 6, "mouse": 6,
    }
    
    found_ids = set()
    text_lower = result_text.lower()
    for keyword, pid in product_map.items():
        if keyword in text_lower:
            found_ids.add(pid)
    
    return list(found_ids)


# =====================================================
#  API ENDPOINTS
# =====================================================

@app.get("/")
async def root():
    """Health check endpoint"""
    return {
        "status": "online",
        "service": "SmartBasket CrewAI API",
        "version": "1.0.0",
        "agents": [
            "Product Recommender",
            "Budget Analyst",
            "Compatibility Checker"
        ]
    }


@app.get("/api/health")
async def health_check():
    """API health check with mode info"""
    api_key = os.getenv("OPENAI_API_KEY", "")
    has_key = bool(api_key and api_key != "your_openai_api_key_here")
    
    return {
        "status": "healthy",
        "mode": "live" if has_key else "demo",
        "message": "CrewAI is ready" if has_key else "Running in demo mode (no API key configured)"
    }


@app.post("/api/recommend", response_model=RecommendationResponse)
async def get_recommendations(request: QueryRequest):
    """
    Main endpoint: Get AI-powered product recommendations.
    Uses CrewAI agents if OpenAI API key is available, otherwise falls back to demo mode.
    """
    if not request.query.strip():
        raise HTTPException(status_code=400, detail="Query cannot be empty")
    
    # ==========================================
    #  LANGGRAPH ORCHESTRATOR INTERCEPTION
    # ==========================================
    from graph import run_graph
    try:
        graph_out = run_graph(request.query)
        # If LangGraph detected a support query, handle it instantly without CrewAI
        if graph_out.get("intent_detected") == "support":
            return RecommendationResponse(
                success=True,
                query=request.query,
                result=graph_out["result"],
                recommended_product_ids=[],
                agent_info={
                    "mode": "langgraph_support",
                    "message": "LangGraph Orchestrator routed this to Customer Support.",
                    "agents_used": [
                        "LangGraph Router", 
                        "Customer Support Node"
                    ]
                }
            )
    except Exception as e:
        print(f"LangGraph interception warning: {e}")
        pass
        
    # ==========================================
    #  PRODUCT RECOMMENDATION (CrewAI / Smart Engine)
    # ==========================================
    api_key = os.getenv("OPENAI_API_KEY", "")
    use_live = bool(api_key and api_key != "your_openai_api_key_here")
    
    if use_live:
        # --- LIVE MODE: Real CrewAI execution ---
        try:
            from crew import kickoff_crew
            result = kickoff_crew(request.query)
            result_str = str(result)
            product_ids = extract_product_ids(result_str)
            
            return RecommendationResponse(
                success=True,
                query=request.query,
                result=result_str,
                recommended_product_ids=product_ids,
                agent_info={
                    "mode": "live",
                    "agents_used": [
                        "LangGraph Router",
                        "Product Recommender (CrewAI)",
                        "Budget Analyst (CrewAI)", 
                        "Compatibility Checker (CrewAI)"
                    ],
                    "process": "routing -> sequential"
                }
            )
        except Exception as e:
            # Fallback to smart recommender on error
            from recommender import generate_recommendation
            rec = generate_recommendation(request.query)
            return RecommendationResponse(
                success=True,
                query=request.query,
                result=rec["result"] + f"\n\n> ⚠️ *Note: Live CrewAI encountered an error ({str(e)[:100]}). Showing smart fallback.*",
                recommended_product_ids=rec["recommended_product_ids"],
                agent_info={
                    "mode": "demo_fallback",
                    "error": str(e)[:200],
                    "agents_used": [
                        "LangGraph Router",
                        "Product Recommender (smart engine fallback)",
                    ]
                }
            )
    else:
        # --- SMART DEMO MODE: Dynamic AI-like recommendation ---
        from recommender import generate_recommendation
        rec = generate_recommendation(request.query)
        return RecommendationResponse(
            success=True,
            query=request.query,
            result=rec["result"],
            recommended_product_ids=rec["recommended_product_ids"],
            agent_info={
                "mode": "demo",
                "message": "Smart recommendation engine active. Configure OPENAI_API_KEY in .env for full CrewAI.",
                "agents_used": [
                    "LangGraph Router",
                    "Smart Recommender Engine (Demo)"
                ]
            }
        )


@app.get("/api/agents")
async def get_agents_info():
    """Get information about the CrewAI agents"""
    try:
        import yaml
        config_path = os.path.join(os.path.dirname(__file__), "config", "agents.yaml")
        with open(config_path, 'r', encoding='utf-8') as f:
            agents_config = yaml.safe_load(f)
        return {"agents": agents_config}
    except Exception as e:
        return {"error": str(e)}


@app.get("/api/tasks")
async def get_tasks_info():
    """Get information about the CrewAI tasks"""
    try:
        import yaml
        config_path = os.path.join(os.path.dirname(__file__), "config", "tasks.yaml")
        with open(config_path, 'r', encoding='utf-8') as f:
            tasks_config = yaml.safe_load(f)
        return {"tasks": tasks_config}
    except Exception as e:
        return {"error": str(e)}


@app.get("/api/products")
async def get_products():
    """Get the product catalog"""
    from products import PRODUCT_CATALOG
    return {"products": PRODUCT_CATALOG}


# =====================================================
#  SERVER STARTUP
# =====================================================

if __name__ == "__main__":
    import uvicorn
    host = os.getenv("HOST", "0.0.0.0")
    port = int(os.getenv("PORT", 8000))
    print(f"\n🚀 SmartBasket CrewAI Server starting on http://{host}:{port}")
    print(f"📋 API Docs: http://{host}:{port}/docs")
    uvicorn.run(app, host=host, port=port)
