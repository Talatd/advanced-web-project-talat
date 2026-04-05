# AI Agent Planning Document
**Project:** SmartBasket E-Commerce
**Course:** Advanced Web Development (Homework 2 Phase 2 Planning)

## 1. Project Overview

### Website Topic and Purpose
SmartBasket is a modern, premium e-commerce platform focusing on high-end gadgets, wearables, and productivity tools. The primary purpose of this website is to provide an intuitive, futuristic shopping experience that abstracts away the complexity of finding the right technology for specific needs.

### Target Users
The platform targets two main demographics:
1. **Tech Enthusiasts & Gamers**: Looking for bleeding-edge technology like 4K monitors, high-performance GPUs, and mechanical peripherals.
2. **Professionals & Creatives**: Seeking productivity monitors, smart wearables, and advanced tracking devices but who may not know which specific technical specifications perfectly fit their workflow.

### Core Features of the Website (Draft Built)
- Sleek, performant 'Glassmorphism' dark-mode UI.
- Real-time cart system.
- Live-searchable interactive product catalog with category matching constraints.
- Preparation UI framework for advanced AI incorporation.

---

## 2. AI Agent Concept

### What problem will the AI agent solve?
Currently, e-commerce shoppers are burdened with overwhelming choices and confusing specifications (e.g., comparing RTX 4070 vs RTX 4080 or calculating refresh rates). The AI agent solves *Decision Fatigue* and *Technical Intimidation*. Instead of hunting through filters, the user simply states their use-case ("I need a laptop for video editing and occasional gaming under $2000") and the AI curates the perfect basket.

### What type of agent will it be?
The integrated entity will act as a **Smart Recommender & Shopping Advisor**. It functions dynamically by evaluating the user's plain-text prompt, analyzing the product database, cross-referencing compatibility (e.g., not recommending a high refresh monitor if the selected system cannot output it), and suggesting items accompanied by a rationale.

### How users will interact with the agent
The agent primarily uses a **Chat-Based Modal / Background Automation** workflow.
- **Chat Interface:** Users click the floating "Ask AI" button to open a conversation modal. They type their prompt naturally.
- **Background Action:** The AI responds naturally, explains its reasoning ("I chose the Quantum R-12 because its GPU accelerates rendering..."), and automatically appends a dynamic "Add Suggested Bundle to Cart" button directly inside the chat flow.

---

## 3. System Architecture (High-Level)

### Frontend (User Interface)
- **React.js Application**: Handles dynamic UI state (Cart, User Input, Modal rendering).
- Contains an `AIAssistantModal` module which holds the websocket or REST socket connection to the AI backend. It renders the AI's markdown responses and interactive recommendation cards.

### Backend Application (Agent Hub planned for future)
- **Node.js / Express or Python / FastAPI**: A microservice layer that receives the query.
- Extracts parameters via LLM (Large Language Model) function calling.

### External APIs or Services
- **OpenAI API (or Alternative LLMs like Llama 3 via Replicate):** The core intelligence used to parse user queries, compare them against stringified JSON product sheets, and generate actionable tool calls (e.g., `recommendProduct(product_id)`).

### Simple Architecture Flow
```mermaid
graph TD
    A[User types query in React UI] -->|HTTP POST| B[Backend API Proxy (Node.js/Python)]
    B -->|System Prompt & Product JSON Data| C[LLM External API (OpenAI)]
    C -->|Returns JSON recommendations logic| B
    B -->|Formats presentation response| A
    A -->|AI Modal renders 'Add to Cart' button dynamically| D[User Cart State Updates]
```
