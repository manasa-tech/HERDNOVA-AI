"""Farm Manager: plans which specialists to run, runs them in parallel, lets them share
findings in a second round, then synthesises one action plan."""
import asyncio
import json

from app.agents.base import ask_llm, parse_json
from app.agents.specialists import ALL_SPECIALISTS

PLANNER_SYSTEM = (
    "You are the Farm Manager of a livestock advisory team. Given a farmer's question, choose "
    "which specialists are needed from: " + ", ".join(ALL_SPECIALISTS) + ". "
    'Respond ONLY with JSON: {"agents": ["..."], "reason": "..."}'
)

SYNTH_SYSTEM = """You are the Farm Manager. You receive the farmer's question and the findings of
several specialist agents. Merge them into ONE prioritised action plan. Resolve conflicts
explicitly, rank likely causes, and give a rough financial impact.
Write every text field in {language}. Respond ONLY with JSON:
{"summary": "...", "ranked_causes": ["..."],
 "action_plan": [{"step": 1, "action": "...", "owner": "agent name", "urgency": "today|this week|monitor"}],
 "financial_impact": "...", "expected_recovery": "...",
 "disclaimer": "This supports decisions and does not replace a veterinarian."}"""


class FarmManager:
    async def handle(self, question: str, language: str = "English") -> dict:
        selected = await self._plan(question)

        # Round 1: independent investigation, in parallel
        round1 = await asyncio.gather(*(ALL_SPECIALISTS[n].investigate(question) for n in selected))

        # Round 2: collaboration. Each agent sees its peers' round-1 findings and may revise.
        round2 = await asyncio.gather(*(
            ALL_SPECIALISTS[n].investigate(question, peer_findings=[r for r in round1 if r["agent"] != ALL_SPECIALISTS[n].name])
            for n in selected
        ))

        plan = await self._synthesise(question, list(round2), language)
        return {
            "question": question,
            "agents_consulted": selected,
            "plan": plan,
            "agent_reports": list(round2),
        }

    async def _plan(self, question: str) -> list[str]:
        reply = parse_json(await ask_llm(PLANNER_SYSTEM, question, max_tokens=300))
        chosen = [a for a in reply.get("agents", []) if a in ALL_SPECIALISTS]
        return chosen or list(ALL_SPECIALISTS)

    async def _synthesise(self, question: str, reports: list[dict], language: str) -> dict:
        user = json.dumps({"question": question, "specialist_reports": reports}, default=str)
        reply = await ask_llm(SYNTH_SYSTEM.replace("{language}", language), user, max_tokens=1500)
        return parse_json(reply)
