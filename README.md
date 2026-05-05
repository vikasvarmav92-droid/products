# NZ Ecommerce & Dropshipping Product Opportunity Scanner

Monorepo with:
- **FastAPI** backend
- **PostgreSQL** persistence
- **Next.js** dashboard
- **Celery** daily scan scheduler

## Features Implemented
- Query input endpoint for keyword/category scans.
- Query expansion placeholder (LLM-ready).
- Modular provider interfaces and mock providers.
- Real connector placeholders for Google Trends, TikTok, Trade Me, AliExpress.
- Landed-cost and margin estimation for New Zealand.
- Weighted scoring model (0-100).
- Dashboard table for opportunity signals.
- CSV export route.
- Environment variable-driven configuration.

## Project Structure
- `backend/app/providers/base/interfaces.py` - provider abstractions.
- `backend/app/providers/mock/providers.py` - mock data adapters.
- `backend/app/providers/real/` - real connector placeholders.
- `backend/app/services/scanner.py` - scan orchestration and calculations.
- `backend/app/services/scoring.py` - opportunity scoring formula.
- `backend/app/api/routes.py` - REST API + CSV export.
- `frontend/src/app/page.tsx` - dashboard UI.

## Setup
1. Copy env file:
   ```bash
   cp .env.example backend/.env
   ```
2. Start data services:
   ```bash
   docker compose up -d db redis
   ```
3. Install backend dependencies:
   ```bash
   cd backend && python -m venv .venv && source .venv/bin/activate && pip install -r requirements.txt
   ```
4. Run backend:
   ```bash
   uvicorn app.main:app --reload --port 8000
   ```
5. Run celery worker (optional):
   ```bash
   celery -A app.tasks.scheduler.celery_app worker --loglevel=info
   ```
6. Run frontend:
   ```bash
   cd frontend && npm install && npm run dev
   ```

## API Endpoints
- `POST /api/v1/scan` with `{ "query": "pet toys", "max_products": 20 }`
- `GET /api/v1/opportunities`
- `GET /api/v1/opportunities/export`
- `GET /health`

## Notes
- No API keys are hardcoded.
- Swap providers by implementing interfaces and wiring provider factory logic.
