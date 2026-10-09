"""Specialist agents. Each reads only its own data and returns structured findings."""
import json
from dataclasses import dataclass
from typing import Callable, Optional

from app.agents.base import ask_llm, parse_json
from app.tools import farm_tools as t

OUTPUT_FORMAT = """Respond with ONLY a JSON object, no preamble, using this shape:
{"findings": "<2-4 sentences>", "severity": "low|medium|high",
 "confidence": <0.0-1.0>, "recommended_actions": ["..."], "cows_flagged": [<cow ids>]}"""


@dataclass
class SpecialistAgent:
    name: str
    role_prompt: str
    fetch: Callable[[], dict]

    async def investigate(self, question: str, peer_findings: Optional[list[dict]] = None) -> dict:
        data = self.fetch()
        system = (
            f"You are the {self.name} on a livestock advisory team. {self.role_prompt} "
            "Base your reasoning only on the data provided. Do not invent numbers. " + OUTPUT_FORMAT
        )
        user = f"Farmer's question: {question}\n\nYour farm data:\n{json.dumps(data, default=str)}"
        if peer_findings:
            user += (
                "\n\nOther agents reported these findings. Revise your view if they change your "
                f"conclusion, and note any cross-links:\n{json.dumps(peer_findings, default=str)}"
            )
        result = parse_json(await ask_llm(system, user))
        result["agent"] = self.name
        return result


HEALTH = SpecialistAgent(
    name="Health Agent",
    role_prompt="You assess disease signs, vaccinations and treatments in the herd.",
    fetch=lambda: {
        "recent_health_events": t.recent_health_events(14),
        "cows_with_largest_milk_drop": t.cow_milk_drop(7),
    },
)

NUTRITION = SpecialistAgent(
    name="Nutrition Agent",
    role_prompt="You assess feed type, quantity, protein levels and recent ration changes.",
    fetch=lambda: {
        "feed_changes": t.feed_changes(30),
        "cows_with_largest_milk_drop": t.cow_milk_drop(7),
    },
)

BREEDING = SpecialistAgent(
    name="Breeding Agent",
    role_prompt="You assess lactation stage, pregnancy and calving dates, and whether they explain yield changes.",
    fetch=lambda: {"breeding_status": t.breeding_status()},
)

INVENTORY = SpecialistAgent(
    name="Inventory Agent",
    role_prompt="You check stock of feed, medicines and supplements against safe levels.",
    fetch=lambda: {"inventory": t.inventory_alerts()},
)

FINANCE = SpecialistAgent(
    name="Finance Agent",
    role_prompt="You estimate income lost, the cost of the fixes, and whether treatment is worth it.",
    fetch=lambda: {"financials": t.financial_summary(7)},
)

ALL_SPECIALISTS = {a.name: a for a in [HEALTH, NUTRITION, BREEDING, INVENTORY, FINANCE]}
