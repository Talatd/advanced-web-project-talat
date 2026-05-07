"""
SmartBasket MCP (Model Context Protocol) sunucusu.

Harici MCP istemcilerinin (ör. Cursor IDE) ürün kataloğu ve LangGraph tabanlı
öneri/destek akışına standart araçlar ve kaynaklar üzerinden erişmesini sağlar.
"""

from __future__ import annotations

import json
import os
from pathlib import Path

from dotenv import load_dotenv
from mcp.server.fastmcp import FastMCP

load_dotenv(Path(__file__).resolve().parent / ".env")

mcp = FastMCP(
    "SmartBasket",
    instructions=(
        "SmartBasket e-ticaret asistanı: ürün kataloğu, LangGraph ile yönlendirilmiş "
        "ürün önerisi ve müşteri desteği. Türkçe ve İngilizce sorular desteklenir."
    ),
)


@mcp.tool()
def list_products(category: str | None = None) -> str:
    """
    Katalogdaki ürünleri listeler.
    category verilirse (ör. Monitors, Laptops) yalnızca o kategorideki ürünler döner.
    """
    from products import PRODUCT_CATALOG, get_products_by_category

    if category and category.strip():
        items = get_products_by_category(category.strip())
    else:
        items = list(PRODUCT_CATALOG)
    return json.dumps(items, ensure_ascii=False, indent=2)


@mcp.tool()
def get_product(product_id: int) -> str:
    """Tek bir ürünü sayısal ID ile döndürür."""
    from products import PRODUCT_CATALOG

    for p in PRODUCT_CATALOG:
        if p["id"] == product_id:
            return json.dumps(p, ensure_ascii=False, indent=2)
    return json.dumps({"error": f"product_not_found: id={product_id}"}, ensure_ascii=False)


@mcp.tool()
def smartbasket_route(query: str) -> str:
    """
    Kullanıcı mesajını LangGraph üzerinden işler: 'recommend' veya 'support' niyeti,
    metin yanıtı ve önerilen ürün ID listesi. FastAPI tarafındaki graph.invoke akışı ile uyumludur.
    """
    if not query or not str(query).strip():
        return json.dumps({"error": "query_empty"}, ensure_ascii=False)

    from graph import run_graph

    out = run_graph(query.strip())
    payload = {
        "intent_detected": out.get("intent_detected"),
        "recommended_product_ids": out.get("recommended_product_ids", []),
        "result": out.get("result", ""),
    }
    return json.dumps(payload, ensure_ascii=False)


@mcp.tool()
def catalog_summary() -> str:
    """Tüm katalog için LLM tarafından okunabilecek düz metin özet."""
    from products import get_catalog_string

    return get_catalog_string()


@mcp.resource("smartbasket://catalog")
def catalog_resource() -> str:
    """Salt okunur katalog (URI üzerinden okunur)."""
    from products import get_catalog_string

    return get_catalog_string()


@mcp.resource("smartbasket://health")
def health_resource() -> str:
    """Yapılandırma özeti: canlı/demo modu için API anahtarı varlığı (değerler yazılmaz)."""
    openai = os.getenv("OPENAI_API_KEY", "")
    google = os.getenv("GOOGLE_API_KEY", "")
    live = bool(
        (openai and openai != "your_openai_api_key_here")
        or (google and google != "your_google_api_key_here")
    )
    return json.dumps(
        {
            "mode": "live" if live else "demo",
            "openai_configured": bool(openai and openai != "your_google_api_key_here"),
            "google_configured": bool(google and google != "your_google_api_key_here"),
        },
        indent=2,
    )


if __name__ == "__main__":
    mcp.run()
