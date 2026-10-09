from app.db.seed import seed
from app.tools import farm_tools


def setup_module():
    seed()


def test_inventory_flags_low_mineral():
    rows = {r["item"]: r for r in farm_tools.inventory_alerts()}
    assert rows["Mineral mixture"]["status"] == "BELOW SAFE LEVEL"


def test_sick_cows_show_largest_drop():
    worst = farm_tools.cow_milk_drop(7, top_n=3)
    assert {r["cow_id"] for r in worst} == {12, 17, 23}


def test_financial_summary_reports_loss():
    assert farm_tools.financial_summary(7)["estimated_income_lost_inr"] > 0
