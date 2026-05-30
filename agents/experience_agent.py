"""
AGENT 3: Experiences & Culture Agent
PATTERN: Prompt Chaining

3 chained LLM calls: interests → categorise → curate → day schedule.
Output of each step feeds the next.
"""
import time
from models.schemas import AgentResult, TravelRequest
from tools.groq_client import chat
from tools.pakistan_data import ATTRACTIONS, FOOD_GUIDE

STEP1_SYSTEM = """You are a Pakistan travel experiences categorisation expert.
Your job is to map traveler interests to specific experience categories available in Pakistan.
Output ONLY a JSON list. No extra text. Example: ["Mughal architecture", "Sufi shrines", "street food"]"""

STEP2_SYSTEM = """You are a Pakistan local experiences curator with deep on-the-ground knowledge.
You know hidden gems, local tips, best times to visit, and how to experience Pakistan authentically.
Be specific — use real place names, actual costs in PKR, practical logistics."""

STEP3_SYSTEM = """You are a master Pakistan itinerary designer.
You create day-by-day plans that flow logically, respect travel distances within the destination,
balance activity with rest, and integrate local meal recommendations at each stage.
Format: Day N | Time Block | Activity | Practical Note"""


async def run(request: TravelRequest) -> AgentResult:
    start = time.time()
    dest = request.destination
    known_attractions = ATTRACTIONS.get(dest.lower().split()[0], [])
    food_info = FOOD_GUIDE.get(dest.lower().split()[0], {})

    # STEP 1 — Map interests to Pakistan-specific experience categories
    categories_raw = chat(
        system=STEP1_SYSTEM,
        messages=[{"role": "user", "content": (
            f"Traveler interests: {request.interests or ['general sightseeing']}\n"
            f"Destination: {dest}, Pakistan\n"
            f"Travel style: {request.travel_style}\n"
            f"Map to 4-5 specific experience categories available at this destination. JSON list only."
        )}],
        model="llama-3.1-8b-instant",  # faster model for simple categorisation
        max_tokens=200, temperature=0.4,
    )

    # STEP 2 — Curate 3 specific activities per category
    activities = chat(
        system=STEP2_SYSTEM,
        messages=[{"role": "user", "content": (
            f"Destination: {dest}, Pakistan | Dates: {request.start_date} to {request.end_date}\n"
            f"Travelers: {request.travelers} | Budget for experiences (~20%): PKR {int(request.budget_pkr*0.20):,}\n"
            f"Experience categories: {categories_raw}\n"
            f"Known attractions in database: {known_attractions[:5]}\n"
            f"Local food highlights: {food_info.get('must_try', [])[:4]}\n\n"
            f"Curate 3 specific activities per category with:\n"
            f"- Exact name and location\n- Why it fits this traveler\n"
            f"- Approximate cost in PKR\n- Best time of day to visit\n- Local insider tip"
        )}],
        max_tokens=1500,
    )

    # STEP 3 — Build day-by-day schedule
    trip_days = max(1, (int(request.end_date.replace("-","")) - int(request.start_date.replace("-",""))))
    trip_days = min(trip_days, 14)

    schedule = chat(
        system=STEP3_SYSTEM,
        messages=[{"role": "user", "content": (
            f"Create a {trip_days}-day experience itinerary for {dest}, Pakistan.\n"
            f"Dates: {request.start_date} to {request.end_date}\n"
            f"Travelers: {request.travelers} | Style: {request.travel_style}\n"
            f"Special requirements: {request.special_requirements or 'none'}\n\n"
            f"Curated activities:\n{activities}\n\n"
            f"Rules:\n"
            f"- Start Day 1 after arrival (no intense activities first day if long journey)\n"
            f"- Group nearby attractions to minimise travel time\n"
            f"- Include halal meal recommendations at each time block\n"
            f"- Note Jummah (Friday prayer) timing — avoid activities 12-2pm Friday\n"
            f"- Include one 'hidden gem' per day that most tourists miss\n"
            f"- End each day with a local evening activity or food recommendation"
        )}],
        max_tokens=2000,
    )

    full_output = (
        f"STEP 1 — Experience Categories:\n{categories_raw}\n\n"
        f"STEP 2 — Curated Activities:\n{activities}\n\n"
        f"STEP 3 — Day-by-Day Schedule:\n{schedule}"
    )

    return AgentResult(
        agent_name="Experiences & Culture Agent", pattern="Prompt Chaining",
        status="success", output=full_output,
        processing_time_ms=int((time.time()-start)*1000)
    )
