"""更真实的Dashboard服务 - 模拟真实农业生产场景"""
from __future__ import annotations

from datetime import datetime, timedelta
from random import Random
from typing import Dict, List, Optional

from sqlalchemy.ext.asyncio import AsyncSession

from app.schemas.dashboard import DashboardSummary, GreenhouseInfo, LatestReading


class GreenhouseSimulator:
    """单个大棚的物理模拟器"""
    
    def __init__(self, gh_id: int, name: str, crop: str, seed: int):
        self.id = gh_id
        self.name = name
        self.crop = crop
        self._rnd = Random(seed + gh_id)
        
        # 大棚物理参数
        self.area_m2 = self._rnd.uniform(200, 1000)  # 面积平方米
        self.volume_m3 = self.area_m2 * self._rnd.uniform(3, 5)  # 体积
        
        # 当前环境状态
        self.air_temp = 22.0
        self.air_humidity = 70.0
        self.soil_moisture = 35.0
        self.soil_temp = 20.0
        self.soil_ph = 6.5
        self.soil_ec = 1.5
        self.co2_ppm = 400.0
        self.light_lux = 0.0
        
        # 作物生长参数
        self.plant_date = datetime.utcnow() - timedelta(days=self._rnd.randint(10, 60))
        self.growth_days = (datetime.utcnow() - self.plant_date).days
        self.expected_harvest_days = self._rnd.randint(30, 120)
        self.growth_stage = self._calculate_growth_stage()
        
        # 设备状态
        self.irrigation_active = False
        self.ventilation_open = 0  # 0-100%
        self.shading_active = False
        self.heating_active = False
        self.lights_active = False
        
        # 灌溉历史
        self.last_irrigation: Optional[datetime] = None
        self.total_irrigation_minutes_today = 0
        
        # 告警状态
        self.active_alerts: List[dict] = []
        self.alert_history: List[dict] = []
    
    def _calculate_growth_stage(self) -> str:
        """根据种植天数计算生长阶段"""
        progress = self.growth_days / self.expected_harvest_days
        if progress < 0.2:
            return "幼苗期"
        elif progress < 0.4:
            return "生长期"
        elif progress < 0.7:
            return "开花期" if self.crop in ["藏红花", "名贵兰花", "番茄", "黄瓜"] else "旺盛生长期"
        elif progress < 0.9:
            return "结果期" if self.crop in ["番茄", "黄瓜", "辣椒"] else "成熟期"
        else:
            return "采收期"
    
    def update(self, dt: timedelta = timedelta(minutes=5)):
        """更新大棚物理状态 - 模拟真实的物理变化"""
        minutes = dt.total_seconds() / 60
        hour = datetime.utcnow().hour + datetime.utcnow().minute / 60
        
        # 光照模拟 - 根据时间变化
        if 6 <= hour < 18:
            # 白天 - 正弦曲线模拟光照强度
            day_progress = (hour - 6) / 12
            max_lux = 50000 + self._rnd.uniform(-10000, 10000)
            self.light_lux = max_lux * max(0, (3.14159 * day_progress) % 3.14159)
        else:
            self.light_lux = 0
        
        # 外部温度模拟 - 日变化
        base_outdoor_temp = 15 + 10 * (3.14159 * (hour - 6) / 12 % 3.14159)
        
        # 空气温度变化
        if self.heating_active:
            self.air_temp += 0.5 * minutes / 60
        elif self.ventilation_open > 0:
            # 通风导致温度趋向外部温度
            ventilation_effect = self.ventilation_open / 100 * 0.3
            self.air_temp += (base_outdoor_temp - self.air_temp) * ventilation_effect * minutes / 60
        
        # 光照加热效应
        self.air_temp += self.light_lux / 50000 * 0.1 * minutes / 60
        
        # 自然散热
        self.air_temp -= (self.air_temp - base_outdoor_temp) * 0.05 * minutes / 60
        
        # 随机波动
        self.air_temp += self._rnd.uniform(-0.1, 0.1)
        self.air_temp = max(5, min(40, self.air_temp))
        
        # 湿度变化
        if self.irrigation_active:
            # 灌溉增加湿度
            self.air_humidity += 2 * minutes / 60
            self.soil_moisture += 3 * minutes / 60
        
        if self.ventilation_open > 30:
            # 强通风降低湿度
            self.air_humidity -= 1 * minutes / 60
        
        # 蒸发
        self.soil_moisture -= self.light_lux / 50000 * 0.5 * minutes / 60
        
        # 湿度自然趋向
        target_humidity = 60 + self.light_lux / 50000 * 20
        self.air_humidity += (target_humidity - self.air_humidity) * 0.1 * minutes / 60
        self.air_humidity += self._rnd.uniform(-1, 1)
        self.air_humidity = max(20, min(95, self.air_humidity))
        
        # 土壤湿度自然下降
        self.soil_moisture -= 0.3 * minutes / 60
        self.soil_moisture = max(10, min(60, self.soil_moisture))
        
        # CO2变化
        if self.ventilation_open > 50:
            self.co2_ppm = 400 + self._rnd.uniform(-50, 50)
        else:
            self.co2_ppm += self._rnd.uniform(-20, 30)
            self.co2_ppm = max(300, min(2000, self.co2_ppm))
        
        # 自动灌溉触发逻辑（模拟系统自动控制）
        if self.soil_moisture < 25 and not self.irrigation_active:
            if self.total_irrigation_minutes_today < 30:  # 每天最多30分钟
                self.irrigation_active = True
                self.last_irrigation = datetime.utcnow()
        
        # 灌溉自动停止
        if self.irrigation_active:
            if self.soil_moisture > 40 or (datetime.utcnow() - self.last_irrigation).seconds > 300:
                self.irrigation_active = False
                self.total_irrigation_minutes_today += 5
        
        # 自动通风逻辑
        if self.air_temp > 28:
            self.ventilation_open = min(100, self.ventilation_open + 10)
        elif self.air_temp < 20:
            self.ventilation_open = max(0, self.ventilation_open - 10)
        
        # 更新生长天数
        self.growth_days = (datetime.utcnow() - self.plant_date).days
        self.growth_stage = self._calculate_growth_stage()
        
        # 检查告警条件
        self._check_alerts()
    
    def _check_alerts(self):
        """检查并生成告警"""
        now = datetime.utcnow()
        
        # 清除已解决的告警
        self.active_alerts = [a for a in self.active_alerts if not a.get("resolved")]
        
        # 高温告警
        if self.air_temp > 32 and not any(a["type"] == "high_temp" for a in self.active_alerts):
            self.active_alerts.append({
                "id": f"{self.id}_{now.timestamp()}",
                "type": "high_temp",
                "level": "warning" if self.air_temp < 35 else "critical",
                "message": f"温度过高: {self.air_temp:.1f}°C",
                "ts": now,
                "resolved": False
            })
        
        # 低温告警
        if self.air_temp < 10 and not any(a["type"] == "low_temp" for a in self.active_alerts):
            self.active_alerts.append({
                "id": f"{self.id}_{now.timestamp()}",
                "type": "low_temp", 
                "level": "warning" if self.air_temp > 5 else "critical",
                "message": f"温度过低: {self.air_temp:.1f}°C",
                "ts": now,
                "resolved": False
            })
        
        # 干旱告警
        if self.soil_moisture < 15 and not any(a["type"] == "drought" for a in self.active_alerts):
            self.active_alerts.append({
                "id": f"{self.id}_{now.timestamp()}",
                "type": "drought",
                "level": "critical",
                "message": f"土壤严重干旱: {self.soil_moisture:.1f}%",
                "ts": now,
                "resolved": False
            })
        
        # 高湿告警
        if self.air_humidity > 85 and not any(a["type"] == "high_humidity" for a in self.active_alerts):
            self.active_alerts.append({
                "id": f"{self.id}_{now.timestamp()}",
                "type": "high_humidity",
                "level": "warning",
                "message": f"湿度过高: {self.air_humidity:.1f}%",
                "ts": now,
                "resolved": False
            })
        
        # 解决已恢复的告警
        for alert in self.active_alerts:
            if alert["type"] == "high_temp" and self.air_temp < 30:
                alert["resolved"] = True
                alert["resolved_ts"] = now
            elif alert["type"] == "low_temp" and self.air_temp > 12:
                alert["resolved"] = True
                alert["resolved_ts"] = now
            elif alert["type"] == "drought" and self.soil_moisture > 25:
                alert["resolved"] = True
                alert["resolved_ts"] = now
            elif alert["type"] == "high_humidity" and self.air_humidity < 75:
                alert["resolved"] = True
                alert["resolved_ts"] = now
    
    def get_reading(self) -> LatestReading:
        """获取当前读数"""
        return LatestReading(
            ts=datetime.utcnow(),
            air_temp_c=round(self.air_temp, 2),
            air_humidity_pct=round(self.air_humidity, 1),
            soil_moisture_pct=round(self.soil_moisture, 1),
            soil_ph=round(self.soil_ph, 2),
            soil_ec=round(self.soil_ec, 2),
        )
    
    def irrigate(self, seconds: int) -> dict:
        """执行灌溉"""
        self.irrigation_active = True
        self.last_irrigation = datetime.utcnow()
        self.total_irrigation_minutes_today += seconds / 60
        
        # 立即增加土壤湿度
        self.soil_moisture = min(60, self.soil_moisture + seconds / 60)
        
        return {
            "success": True,
            "message": f"已启动灌溉 {seconds}秒",
            "irrigation_time": seconds,
            "estimated_water_ml": seconds * 500,  # 假设500ml/分钟
            "soil_moisture_after": round(self.soil_moisture, 1)
        }


class DashboardService:
    """增强的Dashboard服务"""
    
    def __init__(self, seed: int = 42) -> None:
        self._rnd = Random(seed)
        self._simulators: Dict[int, GreenhouseSimulator] = {}
        self._init_greenhouses()
    
    def _init_greenhouses(self):
        """初始化大棚模拟器"""
        configs = [
            {"id": 1, "name": "1号智能棚", "crop": "藏红花"},
            {"id": 2, "name": "2号智能棚", "crop": "人参"},
            {"id": 3, "name": "3号智能棚", "crop": "名贵兰花"},
            {"id": 4, "name": "4号智能棚", "crop": "番茄"},
        ]
        
        for config in configs:
            self._simulators[config["id"]] = GreenhouseSimulator(
                gh_id=config["id"],
                name=config["name"],
                crop=config["crop"],
                seed=self._rnd.randint(1, 10000)
            )
    
    async def get_summary(self, db: AsyncSession) -> DashboardSummary:
        """获取汇总数据"""
        now = datetime.utcnow()
        
        # 更新所有模拟器
        for sim in self._simulators.values():
            sim.update()
        
        latest_by_greenhouse: dict[int, LatestReading] = {}
        top_risk: list[GreenhouseInfo] = []
        
        for gh_id, sim in self._simulators.items():
            reading = sim.get_reading()
            latest_by_greenhouse[gh_id] = reading
            
            # 计算风险分数
            risk = 0.0
            
            # 温度风险
            if reading.air_temp_c > 30:
                risk += min(30, (reading.air_temp_c - 30) * 5)
            elif reading.air_temp_c < 12:
                risk += min(30, (12 - reading.air_temp_c) * 3)
            
            # 湿度风险
            if reading.air_humidity_pct > 80:
                risk += min(25, (reading.air_humidity_pct - 80) * 2)
            elif reading.air_humidity_pct < 30:
                risk += 10
            
            # 土壤水分风险
            if reading.soil_moisture_pct < 20:
                risk += min(40, (20 - reading.soil_moisture_pct) * 4)
            elif reading.soil_moisture_pct > 50:
                risk += min(15, (reading.soil_moisture_pct - 50))
            
            # 告警加成
            for alert in sim.active_alerts:
                if alert["level"] == "critical":
                    risk += 20
                elif alert["level"] == "warning":
                    risk += 10
            
            risk = max(0.0, min(100.0, risk + self._rnd.uniform(-2, 2)))
            
            # 曲线吻合度 - 基于生长阶段
            stage_adherence = {
                "幼苗期": 92, "生长期": 88, "开花期": 85,
                "旺盛生长期": 90, "结果期": 82, "成熟期": 85, "采收期": 95
            }
            adherence = stage_adherence.get(sim.growth_stage, 85) - risk * 0.3
            adherence = max(0.0, min(100.0, adherence + self._rnd.uniform(-2, 2)))
            
            top_risk.append(
                GreenhouseInfo(
                    id=gh_id,
                    name=sim.name,
                    crop=sim.crop,
                    risk_score=round(risk, 1),
                    curve_adherence_pct=round(adherence, 1),
                    growth_stage=sim.growth_stage,
                    growth_days=sim.growth_days,
                    expected_harvest_days=sim.expected_harvest_days,
                    active_alerts_count=len(sim.active_alerts)
                )
            )
        
        top_risk.sort(key=lambda x: x.risk_score, reverse=True)
        
        return DashboardSummary(
            ts=now,
            total_greenhouses=len(self._simulators),
            top_risk=top_risk,
            latest_by_greenhouse=latest_by_greenhouse,
        )
    
    async def get_timeseries(self, db: AsyncSession, greenhouse_id: int) -> dict:
        """获取历史数据 - 包含更真实的变化模式"""
        now = datetime.utcnow()
        points = []
        
        sim = self._simulators.get(greenhouse_id)
        if not sim:
            return {"greenhouse_id": greenhouse_id, "points": []}
        
        # 获取当前值作为基准
        base_temp = sim.air_temp
        base_hum = sim.air_humidity
        base_soil = sim.soil_moisture
        
        for i in range(24):
            ts = now - timedelta(hours=(23 - i))
            hour = ts.hour + ts.minute / 60
            
            # 温度日变化曲线
            daily_temp_var = 8 * ((hour - 14) / 12) ** 2  # 下午2点最高
            temp = base_temp - daily_temp_var + self._rnd.uniform(-0.5, 0.5)
            
            # 湿度日变化（与温度相反）
            daily_hum_var = -10 * ((hour - 6) / 12) ** 2  # 早上6点湿度最高
            hum = base_hum - daily_hum_var + self._rnd.uniform(-3, 3)
            
            # 土壤湿度变化（更平缓）
            soil_trend = -0.5 * i  # 逐渐干燥
            soil = base_soil + soil_trend + self._rnd.uniform(-2, 2)
            
            points.append({
                "ts": ts.isoformat() + "Z",
                "air_temp_c": round(max(5, min(40, temp)), 2),
                "air_humidity_pct": round(max(20, min(95, hum)), 1),
                "soil_moisture_pct": round(max(10, min(60, soil)), 1),
                "soil_ph": round(sim.soil_ph + self._rnd.uniform(-0.1, 0.1), 2),
                "soil_ec": round(sim.soil_ec + self._rnd.uniform(-0.1, 0.1), 2),
            })
        
        return {"greenhouse_id": greenhouse_id, "points": points}
    
    async def get_greenhouse_detail(self, db: AsyncSession, greenhouse_id: int) -> dict:
        """获取大棚详细信息"""
        sim = self._simulators.get(greenhouse_id)
        if not sim:
            return None
        
        return {
            "id": sim.id,
            "name": sim.name,
            "crop": sim.crop,
            "area_m2": round(sim.area_m2, 1),
            "plant_date": sim.plant_date.isoformat(),
            "growth_days": sim.growth_days,
            "growth_stage": sim.growth_stage,
            "expected_harvest_days": sim.expected_harvest_days,
            "harvest_progress_pct": round(sim.growth_days / sim.expected_harvest_days * 100, 1),
            "current_reading": sim.get_reading().dict(),
            "equipment_status": {
                "irrigation_active": sim.irrigation_active,
                "ventilation_open_pct": sim.ventilation_open,
                "shading_active": sim.shading_active,
                "heating_active": sim.heating_active,
                "lights_active": sim.lights_active,
            },
            "irrigation_today_minutes": round(sim.total_irrigation_minutes_today, 1),
            "last_irrigation": sim.last_irrigation.isoformat() if sim.last_irrigation else None,
            "active_alerts": sim.active_alerts,
        }
    
    async def irrigate(self, db: AsyncSession, greenhouse_id: int, seconds: int) -> dict:
        """执行灌溉操作"""
        sim = self._simulators.get(greenhouse_id)
        if not sim:
            return {"success": False, "message": "大棚不存在"}
        
        # 限制单次灌溉时间
        seconds = min(seconds, 600)  # 最多10分钟
        
        result = sim.irrigate(seconds)
        
        return {
            **result,
            "greenhouse_id": greenhouse_id,
            "greenhouse_name": sim.name,
            "timestamp": datetime.utcnow().isoformat()
        }
    
    async def get_all_alerts(self, db: AsyncSession) -> List[dict]:
        """获取所有大棚的告警"""
        all_alerts = []
        for sim in self._simulators.values():
            for alert in sim.active_alerts:
                all_alerts.append({
                    **alert,
                    "greenhouse_id": sim.id,
                    "greenhouse_name": sim.name,
                    "crop": sim.crop
                })
        
        # 按时间排序
        all_alerts.sort(key=lambda x: x["ts"], reverse=True)
        return all_alerts
    
    async def acknowledge_alert(self, db: AsyncSession, alert_id: str) -> dict:
        """确认告警"""
        for sim in self._simulators.values():
            for alert in sim.active_alerts:
                if alert["id"] == alert_id:
                    alert["acknowledged"] = True
                    alert["acknowledged_ts"] = datetime.utcnow()
                    return {"success": True, "message": "告警已确认"}
        
        return {"success": False, "message": "告警不存在或已解决"}
