"""
AGENT 1: Flight & Transport Agent
PATTERN: Tool Use

The LLM is given a tool schema, decides when to call it,
we execute the mock function and feed results back for a final answer.
"""
import time, json, re
from models.schemas import AgentResult, TravelRequest
from tools.groq_client import chat
from tools.pakistan_data import TRANSPORT_OPTIONS

SYSTEM_PROMPT = """You are Pakistan's expert transport planning agent specialising in routes
across Pakistan — covering PIA/AirBlue/AirSial flights, Daewoo/NATCO buses,
Pakistan Railways, and private vehicles on the Karakoram Highway (KKH).

You have access to this tool:
TOOL: search_pakistan_transport({"origin": "city", "destination": "city", "travelers": N, "budget_pkr": N})

When you need transport data, output EXACTLY:
TOOL_CALL: search_pakistan_transport({"origin": "...", "destination": "...", "travelers": N, "budget_pkr": N})

After receiving tool results, provide:
1. Recommended option with reasons
2. Alternative options ranked by cost vs comfort  
3. Booking tips (where to book, advance booking advice)
4. KKH road conditions / weather warnings if relevant
5. Total estimated transport cost breakdown in PKR
6. Local transport tips within the destination (Careem, rickshaw, local wagons)"""


def _execute_tool(call_json: dict, request: TravelRequest) -> str:
    origin = call_json.get("origin", request.origin_city).lower().replace(" ", "_")
    dest = call_json.get("destination", request.destination).lower().replace(" ", "_")
    travelers = call_json.get("travelers", request.travelers)
    budget = call_json.get("budget_pkr", int(request.budget_pkr * 0.25))

    key = f"{origin}_to_{dest}"
    options = TRANSPORT_OPTIONS.get(key, TRANSPORT_OPTIONS.get(f"{dest}_to_{origin}", {}))

    if not options:
        return json.dumps({
            "status": "no_direct_data",
            "advice": f"Check Sastaticket.pk or NATCO website for {origin} to {dest}.",
            "general_tip": "Most northern routes depart Rawalpindi Pirwadhai Mor. Book 3-5 days ahead in peak season (Jun-Oct).",
        })

    affordable = {k: v for k, v in options.items()
                  if isinstance(v, dict) and v.get("price_pkr", 0) * travelers <= budget}

    return json.dumps({
        "route": f"{origin} → {dest}", "travelers": travelers,
        "all_options": options, "within_budget": affordable,
        "booking_links": {"daewoo": "daewoo.com.pk", "pia": "piac.com.pk", "airblue": "airblue.com"},
    })


async def run(request: TravelRequest) -> AgentResult:
    start = time.time()
    messages = [{
        "role": "user",
        "content": (
            f"Plan transport for this Pakistan trip:\n"
            f"From: {request.origin_city} → To: {request.destination}\n"
            f"Travelers: {request.travelers} | Dates: {request.start_date} to {request.end_date}\n"
            f"Total budget: PKR {request.budget_pkr:,} | Transport budget (~25%): PKR {int(request.budget_pkr*0.25):,}\n"
            f"Style: {request.travel_style}\n\nUse your tool to search options then give full recommendation."
        )
    }]

    response_text = chat(messages=messages, system=SYSTEM_PROMPT, max_tokens=800)

    match = re.search(r"TOOL_CALL:\s*search_pakistan_transport\((\{.*?\})\)", response_text, re.DOTALL)
    if match:
        try:
            call_json = json.loads(match.group(1))
        except Exception:
            call_json = {}
        tool_result = _execute_tool(call_json, request)
        messages += [
            {"role": "assistant", "content": response_text},
            {"role": "user", "content": f"Tool result:\n{tool_result}\n\nNow give complete transport recommendation."}
        ]
        final_text = chat(messages=messages, system=SYSTEM_PROMPT, max_tokens=1500)
    else:
        final_text = response_text

    return AgentResult(
        agent_name="Flight & Transport Agent", pattern="Tool Use",
        status="success", output=final_text,
        processing_time_ms=int((time.time()-start)*1000)
    )
