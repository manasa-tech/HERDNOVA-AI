# Multi-Agent Livestock Farm Decision Support

An AI farm advisor where specialist agents (Health, Nutrition, Breeding, Inventory, Finance)
are coordinated by a Farm Manager agent. A farmer asks a question in plain language and gets
one prioritised action plan with an estimated financial impact.

## Structure

```
livestock-multiagent/
├── backend/            FastAPI + agent orchestration
│   ├── app/
│   │   ├── main.py             API routes
│   │   ├── config.py           Settings from .env
│   │   ├── db/                 SQLite schema, connection, synthetic seeder
│   │   ├── tools/farm_tools.py Data-access tools the agents call
│   │   └── agents/             Base agent, specialists, Farm Manager orchestrator
│   └── tests/
├── frontend/           React (Vite) chat UI + agent dashboard
├── data/               farm.db is created here (gitignored)
└── docs/               Architecture notes
```

## Quick start

### 1. Backend
```bash
cd backend
python -m venv .venv && source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -r requirements.txt
cp ../.env.example ../.env                          # then add your ANTHROPIC_API_KEY
python -m app.db.seed                               # creates synthetic farm data
uvicorn app.main:app --reload --port 8000
```

### 2. Frontend
```bash
cd frontend
npm install
npm run dev                                         # http://localhost:5173
```

Open the app and try: "Milk production has decreased this week."

## Notes
- The system supports decisions and does not replace a veterinarian.
- Swap the synthetic seed for real farm records by writing to the same tables in `backend/app/db/schema.sql`.
