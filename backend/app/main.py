from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from app.agents.farm_manager import FarmManager
from app.db.database import init_db
from app.tools import farm_tools

app = FastAPI(title="Livestock Multi-Agent Advisor")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
def startup() -> None:
    init_db()


class QueryIn(BaseModel):
    question: str
    language: str = "English"


@app.post("/api/query")
async def query(body: QueryIn):
    return await FarmManager().handle(body.question, body.language)


@app.get("/api/dashboard")
def dashboard():
    return {
        "milk_trend": farm_tools.milk_trend(14),
        "inventory": farm_tools.inventory_alerts(),
        "financials": farm_tools.financial_summary(7),
    }


@app.get("/api/health")
def health():
    return {"status": "ok"}
