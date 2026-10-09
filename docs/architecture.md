# Architecture

## Request flow
1. Farmer question arrives at `POST /api/query`.
2. **Planner** (Farm Manager) picks which specialists are needed.
3. **Round 1**: selected specialists run in parallel, each calling its data tools in
   `app/tools/farm_tools.py`, and return structured findings.
4. **Round 2 (collaboration)**: each specialist sees its peers' round-1 findings and may revise.
5. **Synthesis**: the Farm Manager merges everything into ranked causes, prioritised steps,
   a financial impact estimate and a disclaimer, written in the farmer's language.
6. The frontend shows the plan and one card per agent.

## Extending
- New agent: add a `SpecialistAgent` in `specialists.py` and register it in `ALL_SPECIALISTS`.
- New data source: add a query in `farm_tools.py` and reference it in the agent's `fetch`.
- Retrieval (RAG): add a vector store and inject guideline snippets into a specialist's `fetch`.
