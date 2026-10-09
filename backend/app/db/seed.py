"""Creates a synthetic farm that reproduces the 'milk drop' scenario from the project idea.

Run from backend/:  python -m app.db.seed
"""
import random
from datetime import date, timedelta

from app.db.database import get_conn, init_db

SICK_COWS = [12, 17, 23]       # early mastitis indicators
LATE_LACTATION = [2, 9]        # minor natural decline


def seed(days: int = 30) -> None:
    init_db()
    random.seed(42)
    today = date.today()
    conn = get_conn()

    for table in ["expenses", "inventory", "feed_logs", "health_events", "milk_yield", "cows"]:
        conn.execute(f"DELETE FROM {table}")

    cows = []
    for cow_id in range(1, 31):
        if cow_id in LATE_LACTATION:
            stage, dim = "late", random.randint(230, 260)
        elif cow_id in SICK_COWS:
            stage, dim = "mid", random.randint(90, 120)
        else:
            stage, dim = random.choice(["early", "mid", "mid"]), random.randint(30, 200)
        pregnant = 1 if stage == "late" else 0
        calving = (today + timedelta(days=random.randint(20, 120))).isoformat() if pregnant else None
        cows.append((cow_id, f"C{cow_id:02d}", "Holstein Friesian", stage, dim, pregnant, calving))
    conn.executemany("INSERT INTO cows VALUES (?,?,?,?,?,?,?)", cows)

    # Last 2*days of yield so the 'previous period' baseline exists for comparisons.
    for d in range(2 * days, -1, -1):
        day = (today - timedelta(days=d)).isoformat()
        for cow_id in range(1, 31):
            litres = random.uniform(12, 16)
            if cow_id in LATE_LACTATION and d <= 14:
                litres *= 0.9
            if cow_id in SICK_COWS and d <= 6:
                litres *= 0.7
            conn.execute("INSERT INTO milk_yield (cow_id, date, litres) VALUES (?,?,?)",
                         (cow_id, day, round(litres, 2)))

    conn.execute("INSERT INTO feed_logs (date, feed_type, quantity_kg, protein_pct, notes) VALUES (?,?,?,?,?)",
                 ((today - timedelta(days=30)).isoformat(), "Standard dairy mix", 900, 16.5, "Regular ration"))
    conn.execute("INSERT INTO feed_logs (date, feed_type, quantity_kg, protein_pct, notes) VALUES (?,?,?,?,?)",
                 ((today - timedelta(days=7)).isoformat(), "Economy mix", 900, 14.2,
                  "Switched to economy mix to cut costs"))

    conn.execute("INSERT INTO health_events (cow_id, date, event_type, notes) VALUES (?,?,?,?)",
                 (1, (today - timedelta(days=60)).isoformat(), "vaccination", "FMD booster"))
    for cow_id in SICK_COWS:
        conn.execute("INSERT INTO health_events (cow_id, date, event_type, notes) VALUES (?,?,?,?)",
                     (cow_id, (today - timedelta(days=5)).isoformat(), "mastitis_indicator",
                      "Udder firmness and reduced milk letdown noted"))

    conn.executemany("INSERT INTO inventory VALUES (?,?,?,?,?)", [
        ("Dairy concentrate", "feed", 820, "kg", 300),
        ("Green fodder (silage)", "feed", 1400, "kg", 500),
        ("Mineral mixture", "supplement", 4, "kg", 10),
        ("Mastitis treatment (intramammary)", "medicine", 6, "tubes", 4),
    ])

    conn.executemany("INSERT INTO expenses (date, category, amount_inr, description) VALUES (?,?,?,?)", [
        ((today - timedelta(days=20)).isoformat(), "feed", 14500, "Concentrate purchase"),
        ((today - timedelta(days=12)).isoformat(), "vet", 1200, "Routine vet visit"),
        ((today - timedelta(days=4)).isoformat(), "medicine", 650, "Mastitis treatment tubes"),
        ((today - timedelta(days=2)).isoformat(), "feed", 3800, "Economy mix purchase"),
    ])

    conn.commit()
    conn.close()
    print(f"Seeded synthetic farm: 30 cows, {2 * days} days of yield data.")


if __name__ == "__main__":
    seed()
