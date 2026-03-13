from __future__ import annotations

from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel, Field


class StageInfo(BaseModel):
    id: int
    name: str
    order: int
    status: str = Field(default="pending")  # pending, active, completed
    target_temp_min: float
    target_temp_max: float
    target_humidity_min: float
    target_humidity_max: float
    target_soil_moisture_min: float
    target_soil_moisture_max: float


class GreenhouseStage(BaseModel):
    greenhouse_id: int
    current_stage: StageInfo
    all_stages: List[StageInfo]
    days_in_stage: int
    estimated_days_remaining: int


class Alert(BaseModel):
    id: str
    greenhouse_id: int
    level: str = Field(default="warning")  # info, warning, critical
    title: str
    message: str
    ts: datetime
    resolved: bool = False
    auto_action: Optional[str] = None


class SOPTask(BaseModel):
    id: str
    greenhouse_id: int
    title: str
    description: str
    scheduled_time: str
    status: str = Field(default="pending")  # pending, in_progress, completed
    priority: str = Field(default="normal")  # low, normal, high
    assignee: Optional[str] = None


class TaskCompleteRequest(BaseModel):
    task_id: str
    notes: Optional[str] = None
