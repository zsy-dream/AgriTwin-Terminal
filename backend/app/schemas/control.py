from __future__ import annotations

from datetime import datetime

from pydantic import BaseModel, Field


class IrrigateRequest(BaseModel):
    greenhouse_id: int
    mode: str = Field(default="auto", description="auto | manual")
    duration_sec: int = Field(ge=5, le=1800)
    reason: str = Field(min_length=2, max_length=500)


class ControlActionResponse(BaseModel):
    action_id: int
    greenhouse_id: int
    ts: datetime
    action_type: str
    duration_sec: int
    expected_effect: str
