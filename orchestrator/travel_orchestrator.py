"""
ORCHESTRATOR: Travel Concierge Orchestrator
PATTERN: Multi-Agent Fan-Out + Synthesise

All 4 specialist agents run in parallel via asyncio.gather.
Results are collected and synthesised into a unified Pakistan travel plan.
"""
import asyncio, uuid, time
from models.schemas import TravelRequest, TravelResponse, AgentResult
from agents import flight_agent, hotel_agent, experience_agent, safety_agent
from tools.groq_client import chat
from tools.pakistan_data import SAFETY_INFO, SEASON_GUIDE


SYNTHESISER_SYSTEM = """You are Pakistan's premier AI travel concierge.
You receive outputs from four specialist agents and synthesise them into one
cohesive, personalised Pakistan travel plan. Your output is the final product
the traveler will read and use.

Be practical, warm, and specific. Use PKR for all costs.
Reference real Pakistani places, transport, food, and cultural context throughout."""


async def _run_agent_safe(agent_module, request: TravelRequest, name: str) -> AgentResult:
    """Wraps agent run in try/except so one failure doesn't kill the others."""
    try:
        return await agent_module.run(request)
    except Exception as e:
        return AgentResult(
            agent_name=name, pattern="unknown",
            status="error", output=f"Agent error: {str(e)}",
            processing_time_ms=0
        )


async def orchestrate(request: TravelRequest) -> TravelResponse:
    request_id = str(uuid.uuid4())[:8]
    total_start = time.time()

    # ─── MULTI-AGENT FAN-OUT ───────────────────────────────────────────
    # All 4 agents fire simultaneously — not sequentially.
    # asyncio.gather runs coroutines concurrently (parallel I/O).
    results = await asyncio.gather(
        _run_agent_safe(flight_agent, request, "Flight & Transport Agent"),
        _run_agent_safe(hotel_agent, request, "Accommodation Agent"),
        _run_agent_safe(experience_agent, request, "Experiences & Culture Agent"),
        _run_agent_safe(safety_agent, request, "Safety & Advisory Agent"),
    )
    agent_results: list[AgentResult] = list(results)
    # ──────────────────────────────────────────────────────────────────

    # Build synthesiser context from successful agents only
    successful = [r for r in agent_results if r.status == "success"]
    agent_context = "\n\n".join(
        f"=== {r.agent_name} ({r.pattern} pattern) ===\n{r.output[-2000:]}"  # truncate for token limit
        for r in successful
    )

    # Determine season tip
    month = int(request.start_date.split("-")[1])
    season = "spring" if month in [3,4,5] else "summer" if month in [6,7,8] else "autumn" if month in [9,10,11] else "winter"
    season_info = SEASON_GUIDE.get(season, {})
    season_tip = f"{season.title()} ({season_info.get('months','')}) — {season_info.get('note', season_info.get('best_for', ''))}"

    # ─── SYNTHESISER ──────────────────────────────────────────────────
    final_itinerary = chat(
        system=SYNTHESISER_SYSTEM,
        messages=[{"role": "user", "content": (
            f"Create the final Pakistan travel plan:\n"
            f"Destination: {request.destination} | From: {request.origin_city}\n"
            f"Dates: {request.start_date} → {request.end_date}\n"
            f"Budget: PKR {request.budget_pkr:,} | Travelers: {request.travelers}\n"
            f"Style: {request.travel_style} | Season: {season_tip}\n"
            f"Special requirements: {request.special_requirements or 'none'}\n\n"
            f"Agent outputs:\n{agent_context}\n\n"
            f"Produce a COMPLETE, PRACTICAL Pakistan travel plan:\n"
            f"1. TRIP OVERVIEW — 2-3 sentence summary of this Pakistan journey\n"
            f"2. DAY-BY-DAY ITINERARY — integrate transport arrival, accommodation check-in, "
            f"   daily experiences with timing, meals, and local tips\n"
            f"3. TOP 3 SAFETY TIPS specific to {request.destination}\n"
            f"4. FOOD HIGHLIGHTS — 3 must-eat dishes and where to eat them\n"
            f"5. PACKING LIST — 5 items specific to {request.destination} and {season}"
        )}],
        max_tokens=2500,
    )

    # Budget summary
    budget_summary = chat(
        messages=[{"role": "user", "content": (
            f"From this Pakistan travel plan, extract a budget breakdown table.\n"
            f"Total budget: PKR {request.budget_pkr:,} for {request.travelers} traveler(s).\n"
            f"Format as a clean table with columns: Category | Estimated PKR | % of Budget\n"
            f"Categories: Transport | Accommodation | Experiences & Entrance Fees | Food | Miscellaneous\n"
            f"End with: Total | PKR X,XXX | 100%\n\n"
            f"Travel plan reference:\n{final_itinerary[:1500]}"
        )}],
        max_tokens=400, temperature=0.3,
    )

    emergency = SAFETY_INFO["emergency_numbers"]
    emergency_str = (
        f"Police: {emergency['police']} | Rescue: {emergency['rescue_punjab']} | "
        f"Ambulance: {emergency['ambulance']} | Tourist Helpline: {emergency['tourist_helpline_ptdc']}"
    )

    return TravelResponse(
        request_id=request_id,
        destination=request.destination,
        agent_results=agent_results,
        final_itinerary=final_itinerary,
        budget_summary=budget_summary,
        best_season_tip=season_tip,
        emergency_contacts=emergency_str,
    )
