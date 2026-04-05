# SmartBasket — AI-Powered E-Commerce Platform

> **Advanced Web Development — Homework 2 + CrewAI Integration**

SmartBasket is a premium, glassmorphism-themed e-commerce platform for tech enthusiasts. It features a multi-agent AI shopping assistant powered by **CrewAI** that provides intelligent product recommendations through natural language interaction.

## Features

- 🛒 **Premium E-Commerce UI** — Glassmorphism dark theme with Framer Motion animations
- 🤖 **AI Shopping Assistant** — Chat-based modal powered by 3 CrewAI agents
- 🔍 **Smart Catalog** — Real-time search and category filtering
- 🧠 **Multi-Category Detection** — Understands complex queries like "I need a keyboard and watch"
- 💰 **Budget Awareness** — Extracts budget constraints and filters accordingly
- ✅ **Compatibility Checking** — Verifies all recommended products work together

## Tech Stack

| Layer | Technology |
|-------|-----------|
| Frontend | React.js, Vite, Framer Motion, Lucide React |
| Backend | FastAPI (Python), CrewAI, Uvicorn |
| Styling | Vanilla CSS (Glassmorphism) |
| AI | CrewAI Multi-Agent + Smart Recommendation Engine |

## Setup & Run Instructions

### Prerequisites
- Node.js 18+
- Python 3.10+

### 1. Clone the repository
```bash
git clone <your-github-repo-url>
cd Advanced-Web-Homework2
```

### 2. Install & Run Frontend
```bash
npm install
npm run dev
```
Frontend runs at: `http://localhost:5173/`

### 3. Install & Run Backend
```bash
cd backend
pip install -r requirements.txt
python main.py
```
Backend runs at: `http://localhost:8000/`  
API Docs: `http://localhost:8000/docs`

### 4. (Optional) Enable Live CrewAI
```bash
cp .env.example .env
# Edit .env and add your OpenAI API key
```

## Pages

| Page | Description |
|------|-------------|
| **Home** (`/`) | Hero banner, featured products, CTA buttons |
| **Catalog** (`/catalog`) | Full product grid with search & category filter |
| **Cart** (`/cart`) | Shopping cart with order summary |
| **AI Assistant** (Modal) | Chat interface for AI recommendations |

## Documentation

- [AI Agent Planning Document](./AI_Agent_Planning.md) — Phase 2 planning for AI integration
- [CrewAI Implementation Report](./CREWAI_REPORT.md) — Detailed technical report with architecture, agents, tasks, and test results

## Live Demo

*(Add your Vercel/Netlify deployment URL here)*
