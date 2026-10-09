"""Data-access tools. Each agent calls these to read its own slice of farm data.

All functions return plain Python objects so they serialise straight into LLM prompts.
"""
from app.config import MILK_PRICE_INR
from app.db.database import get_conn


def _query(sql: str, params: tuple = ()) -> list[dict]:
    conn = get_conn()
    rows = [dict(r) for r in conn.execute(sql, params).fetchall()]
    conn.close()
    return rows


def milk_trend(days: int = 14) -> list[dict]:
    return _query(
        """SELECT date, ROUND(SUM(litres), 1) AS total_litres
           FROM milk_yield WHERE date >= date('now', ?)
           GROUP BY date ORDER BY date""",
        (f"-{days} days",),
    )


def cow_milk_drop(days: int = 7, top_n: int = 5) -> list[dict]:
    """Compare each cow's average yield in the last `days` vs the `days` before that."""
    return _query(
        """SELECT cow_id,
                  ROUND(AVG(CASE WHEN date >= date('now', ?) THEN litres END), 2) AS recent_avg,
                  ROUND(AVG(CASE WHEN date <  date('now', ?) AND date >= date('now', ?) THEN litres END), 2) AS previous_avg
           FROM milk_yield
           WHERE date >= date('now', ?)
           GROUP BY cow_id
           ORDER BY (recent_avg - previous_avg) ASC
           LIMIT ?""",
        (f"-{days} days", f"-{days} days", f"-{2*days} days", f"-{2*days} days", top_n),
    )


def recent_health_events(days: int = 14) -> list[dict]:
    return _query(
        """SELECT cow_id, date, event_type, notes
           FROM health_events WHERE date >= date('now', ?)
           ORDER BY date DESC""",
        (f"-{days} days",),
    )


def feed_changes(days: int = 30) -> list[dict]:
    return _query(
        "SELECT date, feed_type, quantity_kg, protein_pct, notes FROM feed_logs "
        "WHERE date >= date('now', ?) ORDER BY date",
        (f"-{days} days",),
    )


def breeding_status() -> list[dict]:
    return _query(
        """SELECT id AS cow_id, lactation_stage, days_in_milk, pregnant, expected_calving
           FROM cows WHERE lactation_stage IN ('late', 'dry') OR pregnant = 1"""
    )


def inventory_alerts() -> list[dict]:
    return _query(
        """SELECT item, category, quantity, unit, safe_level,
                  CASE WHEN quantity < safe_level THEN 'BELOW SAFE LEVEL' ELSE 'OK' END AS status
           FROM inventory ORDER BY category, item"""
    )


def financial_summary(days: int = 7) -> dict:
    expenses = _query(
        """SELECT category, ROUND(SUM(amount_inr), 2) AS total_inr
           FROM expenses WHERE date >= date('now', ?) GROUP BY category""",
        (f"-{days} days",),
    )
    litres = _query(
        """SELECT
             ROUND(COALESCE(SUM(CASE WHEN date >= date('now', ?) THEN litres END), 0), 1) AS recent_litres,
             ROUND(COALESCE(SUM(CASE WHEN date <  date('now', ?) AND date >= date('now', ?) THEN litres END), 0), 1) AS baseline_litres
           FROM milk_yield WHERE date >= date('now', ?)""",
        (f"-{days} days", f"-{days} days", f"-{2*days} days", f"-{2*days} days"),
    )[0]
    lost_litres = max(litres["baseline_litres"] - litres["recent_litres"], 0)
    return {
        "expenses_by_category": expenses,
        "recent_litres": litres["recent_litres"],
        "baseline_litres": litres["baseline_litres"],
        "estimated_income_lost_inr": round(lost_litres * MILK_PRICE_INR, 2),
        "milk_price_inr_per_litre": MILK_PRICE_INR,
    }
