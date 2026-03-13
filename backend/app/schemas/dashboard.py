from __future__ import annotations

from datetime import datetime
from typing import List

from pydantic import BaseModel, Field


class GreenhouseInfo(BaseModel):
    id: int
    name: str
    crop: str
    risk_score: float = Field(ge=0, le=100)
    curve_adherence_pct: float = Field(ge=0, le=100)


class LatestReading(BaseModel):
    ts: datetime
    air_temp_c: float
    air_humidity_pct: float
    soil_moisture_pct: float
    soil_ph: float
    soil_ec: float


class DashboardSummary(BaseModel):
    ts: datetime
    total_greenhouses: int
    top_risk: List[GreenhouseInfo]
    latest_by_greenhouse: dict[int, LatestReading]
