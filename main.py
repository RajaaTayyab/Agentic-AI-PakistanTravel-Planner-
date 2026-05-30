"""
Pakistan AI Travel Planner — FastAPI Backend
Run: uvicorn main:app --reload --port 8000
"""
import os
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from models.schemas import TravelRequest, TravelResponse
from orchestrator.travel_orchestrator import orchestrate
from dotenv import load_dotenv

load_dotenv()

app = FastAPI(
    title="Pakistan AI Travel Planner",
    description="Multi-agent AI concierge for Pakistan tourism — powered by Groq + LLaMA 3.3",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/health")
def health():
    return {"status": "ok", "model": "llama-3.3-70b-versatile", "provider": "Groq"}


@app.post("/plan", response_model=TravelResponse)
async def plan_trip(request: TravelRequest):
    """
    Main endpoint — triggers all 4 specialist agents in parallel
    and returns unified Pakistan travel plan with individual agent outputs.
    """
    try:
        return await orchestrate(request)
    except EnvironmentError as e:
        raise HTTPException(status_code=500, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Planning error: {str(e)}")


@app.get("/destinations")
def get_destinations():
    return {
        "popular": ["Hunza", "Lahore", "Skardu", "Islamabad", "Swat", "Murree", "Chitral", "Naran", "Karachi"],
        "northern_gems": ["Fairy Meadows", "Deosai", "Attabad Lake", "Khunjerab Pass", "Rakaposhi Base Camp"],
        "cultural": ["Lahore Walled City", "Taxila", "Mohenjo-Daro", "Multan", "Peshawar"],
    }


# Serve frontend — MUST be after all API routes
if os.path.exists("frontend"):
    app.mount("/", StaticFiles(directory="frontend", html=True), name="frontend")
