# LangGraph Entegrasyonu - Kod Açıklamaları

Bu doküman, projeye LangGraph dahil edilirken eklenen ve değiştirilen kodların tam olarak ne işe yaradığını, hangi dosyalarda bulunduğunu detaylı bir şekilde listeler. Sınıfta sunum yaparken veya ödevi savunurken kopya kağıdı olarak kullanabilirsin.

---

## 1. Yeni Oluşturulan Dosya: `backend/graph.py`

Bu dosyanın asıl amacı "Trafik Polisi" gibi çalışmaktır. Gelen soruyu alıp inceleyerek nereye gideceğine (Customer Support mu, Yoksa CrewAI Ürün Önerisi mi) karar verir.

### A. Graph Durumu (State) Tanımlaması
```python
# 1. Define the Graph State
class AgentState(TypedDict):
    query: str             # Kullanıcının sorduğu asıl metin (Örn: "saat öner" veya "kargom nerede")
    intent: str            # Niyet: Soru anlaşıldıktan sonra "recommend" veya "support" olur
    result: str            # Karşı tarafa verilecek son cevap metni
    product_ids: List[int] # Önerilen ürünlerin ID numaraları
```
**Ne İşe Yarar?** LangGraph bir "State Machine" (Durum Makinesi) olarak çalışır. `AgentState` kalıbı, uygulamanın bir düğümden (node) diğer düğüme geçerken taşıdığı değişkenlerdir. Her adımda bu değişkenler güncellenir.

### B. Düğümler (Nodes - İşlemi Yapan Fonksiyonlar)
Uygulamamızdaki duraklardır. Toplam 3 durağımız var.

**Durak 1: Niyet Sınıflandırıcı (Classifier Node)**
```python
def intent_classifier_node(state: AgentState) -> Dict:
    query_lower = state["query"].lower()
    support_keywords = ["order", "track", "help", "return", "refund", "broken", "lost", "where is", "şikayet", "iade", "kargo"]
    
    intent = "recommend" # Varsayılan olarak hep öneri motoruna gönder
    if any(keyword in query_lower for keyword in support_keywords):
        intent = "support" # Eğer destek kelimeleri varsa niyeti 'support' olarak değiştir
        
    return {"intent": intent} # Güncellenmiş durumu geri dön
```
**Ne İşe Yarar?** Gelen mesajı okur. İçinde "kargo, iade, nerede, help" gibi kelimeler geçiyorsa rotayı desteğe (`support`) çevirir. Yoksa ürün önermeye (`recommend`) bırakır.

**Durak 2: Destek Ekibi (Customer Support Node)**
```python
def customer_support_node(state: AgentState) -> Dict:
    response = "## 🛠️ Customer Support Response..." # (Destek metni)
    return {
        "result": response,
        "product_ids": [] # Destek talebinde sepete ürün eklemeyeceğimiz için boş.
    }
```
**Ne İşe Yarar?** Kullanıcının amacı destek olduğunda, bu düğüm devreye girer. Müşteri hizmetleriyle ilgili bağlantıları ve genel mesajları ekrana basar. CrewAI kodunu hiç yormaz.

**Durak 3: CrewAI'a Yönlendirme (Product Recommendation Node)**
```python
def product_recommendation_node(state: AgentState) -> Dict:
    rec = generate_recommendation(state["query"]) # CrewAI veya Smart Engine tetiklenir
    return {
        "result": rec["result"],
        "product_ids": rec["recommended_product_ids"]
    }
```
**Ne İşe Yarar?** Kullanıcı bir ürün arıyorsa, yükü var olan `recommender.py` (Smart Engine / Demo CrewAI) koduna devreden bir nevi köprü görevi görür.

### C. Grafiğin Çizimi (Building the Graph)
```python
workflow = StateGraph(AgentState) # Grafiği başlat
workflow.add_node("classifier", intent_classifier_node)
workflow.add_node("crewai_recommender", product_recommendation_node)
workflow.add_node("customer_support", customer_support_node)

workflow.add_edge(START, "classifier") # 1. Adım: Her zaman sınıflandırıcıdan başla
workflow.add_conditional_edges(        # 2. Adım: Sınıflandırıcının sonucuna göre koşullu yönlen (IF-ELSE)
    "classifier",
    route_by_intent,
    {
        "recommend": "crewai_recommender", # Eğer recommend ise CrewAI'ye git
        "support": "customer_support"      # Eğer support ise Müşteri Desteğine git
    }
)
```
**Ne İşe Yarar?** Bütün fonksiyonları alıp birbirine oklarla bağlayan kısımdır.

---

## 2. Değiştirilen Dosya: `backend/main.py`

Bu dosya API'mizin dışarıya (Arayüze) açılan kapısıdır. Değişikliğin amacı, dışarıdan gelen isteklerin artık *önce* LangGraph filtresinden geçmesidir.

### LangGraph Kesen (Interceptor) Mantığı
```python
    # API endpointsinde (get_recommendations altında) eklenen kod:
    
    from graph import run_graph
    try:
        graph_out = run_graph(request.query) # İsteği önce bizim yepyeni LangGraph'ımıza at.
        
        # Eğer LangGraph "Bu bir destek talebidir (support)" derse;
        if graph_out.get("intent_detected") == "support":
            return RecommendationResponse( # CrewAI kodlarına HİÇ girmeden cevabı direkt React (Arayüze) dön
                success=True,
                query=request.query,
                result=graph_out["result"],
                recommended_product_ids=[],
                agent_info={
                    "mode": "langgraph_support",
                    "message": "LangGraph Orchestrator routed this to Customer Support.",
                    "agents_used": ["LangGraph Router", "Customer Support Node"]
                }
            )
    except Exception as e:
        pass
```
**Ne İşe Yarar?** Kullanıcının mesajı geldiğinde hemen CrewAI çalıştırıp pahalı olan API / LLM çağrısı yapmasını engeller. Araya LangGraph'ı koyarız. LangGraph bir destek mesajı tespit ederse "Hop! Sen CrewAI değilsin" diyerek sonucu doğrudan döner. Eğer ürün önerisiyse, kod akmaya yukarıdan aşağı devam eder ve alt satırlardaki CrewAI kısmına düşer.

---

## 3. Değiştirilen Dosya: `backend/.env.example`

Projenin bir sonraki geliştiricisi (veya hoca) projeyi açtığında, LangGraph adımlarını takip edebilmek (Traceability) için LangSmith'e ihtiyaç duyduğumuzu belirttik.

```env
# LangSmith / LangGraph Integration (Tracing & Observability)
LANGCHAIN_TRACING_V2=true
LANGCHAIN_ENDPOINT="https://api.smith.langchain.com"
LANGCHAIN_API_KEY="your_langsmith_api_key_here"
LANGCHAIN_PROJECT="smartbasket-crewai-langgraph"
```
**Ne İşe Yarar?** LangGraph arka planda çalışırken tüm düğümlerin ne kadar sürdüğünü, içinden hangi verilerin geçtiğini saniye saniye kaydeder. `LANGCHAIN_TRACING_V2=true` komutu ile LangSmith projesi üzerinde harika görsel grafikler çıkarabiliriz. Bu tamamen "Uygulamam çok modern, adımlarını takip edebiliyorum" demektir.
