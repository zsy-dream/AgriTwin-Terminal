from fastapi import APIRouter

from app.api.v1.endpoints import auth, control, dashboard, export, operations, websocket

api_router = APIRouter()

api_router.include_router(auth.router, prefix="/auth", tags=["auth"])
api_router.include_router(dashboard.router, prefix="/dashboard", tags=["dashboard"])
api_router.include_router(control.router, prefix="/control", tags=["control"])
api_router.include_router(operations.router, prefix="/operations", tags=["operations"])
api_router.include_router(websocket.router, prefix="/ws", tags=["websocket"])
api_router.include_router(export.router, prefix="/export", tags=["export"])
