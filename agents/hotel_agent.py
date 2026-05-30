"""
AGENT 2: Accommodation Agent
PATTERN: ReAct (Reason + Act)

The LLM explicitly writes Thought → Action → Observation loops
before arriving at a Final Answer. Makes reasoning fully transparent.
"""
import time, re
from models.schemas import AgentResult, TravelRequest
from tools.groq_client import chat
from tools.pakistan_data import ACCOMMODATIONS

SYSTEM_PROMPT = """You are Pakistan's expert accommodation specialist. You know every type of stay
in Pakistan — from five-star Serena hotels to traditional Hunzai wooden guesthouses,
heritage havelis in Lahore's Walled City, mountain camping sites, and PTDC motels.

You follow the ReAct pattern STRICTLY. For each search decision write:

Thought: <your reasoning — what type of accommodation fits this traveler and why>
Action: search_accommodations(<destination>, <budget_tier: luxury|mid_range|budget>, <travelers>)
Observation: <what the search returned>

After minimum 2 Action/Observation cycles write:
Final Answer: <structured hotel recommendations with prices, pros/cons, booking advice>

NEVER give a Final Answer without completing at least 2 Thought/Action/Observation cycles.
Always include: price in PKR per night, total for stay, pros/cons, booking method."""


def _search_accommodations(destination: str, tier: str, travelers: int) -> str:
    dest_key = destination.lower().split()[0]  # "hunza valley" → "hunza"
    all_hotels = ACCOMMODATIONS.get(dest_key, {})

    if not all_hotels:
        return f"No database entry for {destination}. Recommend searching booking.com or ptdc.org.pk for options."

    hotels = all_hotels.get(tier, all_hotels.get("mid_range", []))
    if not hotels:
        hotels = [h for tier_list in all_hotels.values() for h in tier_list]

    result = []
    for h in hotels:
        h_copy = dict(h)
        h_copy["total_pkr_3nights"] = h["price_pkr_per_night"] * 3 * max(1, travelers // 2)
        result.append(h_copy)
    return str(result)


async def run(request: TravelRequest) -> AgentResult:
    start = time.time()
    budget_per_night = int((request.budget_pkr * 0.35) / max(1, (
        (int(request.end_date.split("-")[2]) - int(request.start_date.split("-")[2])) or 3
    )))
    tier = "luxury" if budget_per_night > 15000 else "mid_range" if budget_per_night > 4000 else "budget"

    messages = [{
        "role": "user",
        "content": (
            f"Find best accommodation in {request.destination} for this Pakistan trip:\n"
            f"Travelers: {request.travelers} | Dates: {request.start_date} to {request.end_date}\n"
            f"Accommodation budget (~35% of total): PKR {int(request.budget_pkr*0.35):,}\n"
            f"Est. per night: PKR {budget_per_night:,} | Likely tier: {tier}\n"
            f"Travel style: {request.travel_style} | Interests: {', '.join(request.interests) or 'general'}\n"
            f"Special requirements: {request.special_requirements or 'none'}\n\n"
            f"Use the ReAct loop — minimum 2 searches before Final Answer."
        )
    }]

    full_trace = ""
    for _ in range(6):
        response = chat(messages=messages, system=SYSTEM_PROMPT, max_tokens=1000)
        full_trace += response + "\n\n"

        if "Final Answer:" in response:
            break

        # Parse and execute action
        action_match = re.search(r"Action:\s*search_accommodations\(([^)]+)\)", response)
        if action_match:
            args = [a.strip().strip("'\"") for a in action_match.group(1).split(",")]
            dest = args[0] if args else request.destination
            t = args[1] if len(args) > 1 else tier
            n = int(args[2]) if len(args) > 2 and args[2].isdigit() else request.travelers
            observation = _search_accommodations(dest, t, n)
            messages += [
                {"role": "assistant", "content": response},
                {"role": "user", "content": f"Observation: {observation}"}
            ]
        else:
            messages += [{"role": "assistant", "content": response}]
            break

    return AgentResult(
        agent_name="Accommodation Agent", pattern="ReAct",
        status="success", output=full_trace,
        processing_time_ms=int((time.time()-start)*1000)
    )
