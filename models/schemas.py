from pydantic import BaseModel, Field, field_validator
from typing import Optional
from enum import Enum


class TravelStyle(str, Enum):
    ADVENTURE = "adventure"
    CULTURAL = "cultural"
    RELIGIOUS = "religious"
    NATURE = "nature"
    FOODIE = "foodie"
    MIXED = "mixed"


class TravelRequest(BaseModel):
    destination: str = Field(..., description="City or region in Pakistan e.g. Hunza, Lahore, Skardu")
    origin_city: str = Field(default="Islamabad", description="Departure city")
    start_date: str = Field(..., description="YYYY-MM-DD")
    end_date: str = Field(..., description="YYYY-MM-DD")
    budget_pkr: int = Field(..., ge=10000, description="Total budget in PKR")
    travelers: int = Field(default=1, ge=1, le=20)
    travel_style: TravelStyle = TravelStyle.MIXED
    interests: list[str] = Field(default_factory=list)
    special_requirements: Optional[str] = None


class AgentResult(BaseModel):
    agent_name: str
    pattern: str
    status: str
    output: str
    processing_time_ms: Optional[int] = None


class TravelResponse(BaseModel):
    request_id: str
    destination: str
    agent_results: list[AgentResult]
    final_itinerary: str
    budget_summary: str
    best_season_tip: str
    emergency_contacts: str
