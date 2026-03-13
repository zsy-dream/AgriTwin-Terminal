from __future__ import annotations

from datetime import datetime

from sqlalchemy import DateTime, Float, ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column

from app.models.base import Base


class Greenhouse(Base):
    __tablename__ = "greenhouses"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    crop: Mapped[str] = mapped_column(String(100), nullable=False)
    location: Mapped[str] = mapped_column(String(200), nullable=True)


class SensorReading(Base):
    __tablename__ = "sensor_readings"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    greenhouse_id: Mapped[int] = mapped_column(ForeignKey("greenhouses.id"), nullable=False)

    ts: Mapped[datetime] = mapped_column(DateTime(timezone=False), nullable=False)

    air_temp_c: Mapped[float] = mapped_column(Float, nullable=False)
    air_humidity_pct: Mapped[float] = mapped_column(Float, nullable=False)

    soil_moisture_pct: Mapped[float] = mapped_column(Float, nullable=False)
    soil_ph: Mapped[float] = mapped_column(Float, nullable=False)
    soil_ec: Mapped[float] = mapped_column(Float, nullable=False)


class ControlAction(Base):
    __tablename__ = "control_actions"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    greenhouse_id: Mapped[int] = mapped_column(ForeignKey("greenhouses.id"), nullable=False)

    ts: Mapped[datetime] = mapped_column(DateTime(timezone=False), nullable=False)
    action_type: Mapped[str] = mapped_column(String(50), nullable=False)
    reason: Mapped[str] = mapped_column(String(500), nullable=False)
    duration_sec: Mapped[int] = mapped_column(Integer, nullable=False)
    expected_effect: Mapped[str] = mapped_column(String(300), nullable=False)
