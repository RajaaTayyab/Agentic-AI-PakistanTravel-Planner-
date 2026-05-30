"""
AGENT 4: Safety & Advisory Agent  
PATTERN: Reflection

Draft advisory → self-critique for gaps → improved final advisory.
Critical for Pakistan travel — visa, cultural, altitude, and area-specific safety.
"""
import time
from models.schemas import AgentResult, TravelRequest
from tools.groq_client import chat
from tools.pakistan_data import SAFETY_INFO, SEASON_GUIDE

DRAFT_SYSTEM = """You are Pakistan's leading travel safety and advisory expert with 20+ years experience.
You provide honest, thorough, and practical safety guidance for travelers to Pakistan.
Pakistan is far safer than international media portrays — your advisory should be accurate, not alarmist."""

CRITIC_SYSTEM = """You are a strict reviewer of Pakistan travel advisories. 
Identify SPECIFIC gaps and errors. Be harsh — a traveler's safety depends on completeness.
List missing items as bullet points. Focus on what's missing, not what's good."""

FINAL_SYSTEM = """You are producing a polished, production-ready Pakistan travel advisory.
Address every critique point. Be specific, actionable, and reassuring where appropriate.
Structure your advisory with clear sections. Include exact numbers (emergency contacts, costs in PKR)."""


async def run(request: TravelRequest) -> AgentResult:
    start = time.time()
    dest = request.destination
    is_northern = any(x in dest.lower() for x in ["hunza", "skardu", "gilgit", "chitral", "swat", "naran", "kaghan", "fairy"])

    emergency = SAFETY_INFO["emergency_numbers"]
    cultural = SAFETY_INFO["cultural_norms"]

    # Determine travel season for season-specific warnings
    month = int(request.start_date.split("-")[1])
    if month in [3,4,5]: season = "spring"
    elif month in [6,7,8]: season = "summer"
    elif month in [9,10,11]: season = "autumn"
    else: season = "winter"
    season_info = SEASON_GUIDE.get(season, {})

    context = (
        f"Destination: {dest}, Pakistan | Season: {season} ({season_info.get('months','')})\n"
        f"Northern areas: {is_northern} | Travelers: {request.travelers}\n"
        f"Special requirements: {request.special_requirements or 'none'}\n"
        f"Emergency numbers from database: {emergency}\n"
        f"Cultural norms: {cultural[:4]}\n"
        f"Season notes: {season_info}"
    )

    # STEP 1 — Draft advisory
    draft = chat(
        system=DRAFT_SYSTEM,
        messages=[{"role": "user", "content": (
            f"Write a comprehensive travel safety advisory for {dest}, Pakistan.\n"
            f"Context:\n{context}\n\n"
            f"Cover: visa/entry, cultural norms, health/altitude, area-specific safety, "
            f"emergency contacts, currency/ATMs, connectivity, weather/seasonal warnings, "
            f"transport safety, accommodation safety tips."
        )}],
        max_tokens=1200,
    )

    # STEP 2 — Self-critique
    critique = chat(
        system=CRITIC_SYSTEM,
        messages=[{"role": "user", "content": (
            f"Review this travel advisory for {dest}, Pakistan:\n\n{draft}\n\n"
            f"Check for: missing emergency numbers, vague cultural advice, missing altitude warnings "
            f"(if northern), missing KKH/road warnings, missing Ramadan/Friday guidance, "
            f"missing SIM card advice, missing ATM/cash warnings for remote areas, "
            f"any outdated or inaccurate information about Pakistan. List ALL gaps."
        )}],
        model="llama-3.1-8b-instant",
        max_tokens=600,
    )

    # STEP 3 — Improved final advisory
    final = chat(
        system=FINAL_SYSTEM,
        messages=[{"role": "user", "content": (
            f"Original draft:\n{draft}\n\nCritique:\n{critique}\n\n"
            f"Produce an improved, complete advisory for {dest}, Pakistan that:\n"
            f"1. Addresses every critique point\n"
            f"2. Includes exact emergency numbers: Police 15, Rescue 1122, Ambulance 115\n"
            f"3. Gives specific PKR amounts where relevant (SIM: PKR 500, water: PKR 50-100)\n"
            f"4. Is honest about safety — Pakistan's northern areas are genuinely safe for tourists\n"
            f"5. Sections: Entry & Visa | Cultural Etiquette | Health & Altitude | "
            f"Safety & Areas | Emergency Contacts | Connectivity | Currency & ATMs"
        )}],
        max_tokens=1500,
    )

    full_output = f"DRAFT:\n{draft}\n\nCRITIQUE:\n{critique}\n\nFINAL ADVISORY:\n{final}"

    return AgentResult(
        agent_name="Safety & Advisory Agent", pattern="Reflection",
        status="success", output=full_output,
        processing_time_ms=int((time.time()-start)*1000)
    )
