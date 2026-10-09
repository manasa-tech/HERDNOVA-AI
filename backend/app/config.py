import os
from pathlib import Path
from dotenv import load_dotenv

ROOT_DIR = Path(__file__).resolve().parents[2]
load_dotenv(ROOT_DIR / ".env")

ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY", "")
MODEL = os.getenv("CLAUDE_MODEL", "claude-sonnet-4-5")
DB_PATH = os.getenv("DB_PATH", str(ROOT_DIR / "data" / "farm.db"))
MILK_PRICE_INR = float(os.getenv("MILK_PRICE_INR", "40"))
