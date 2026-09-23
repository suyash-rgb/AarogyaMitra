import logging
from contextlib import asynccontextmanager
from typing import Annotated

from fastapi import FastAPI, Depends, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import text, select

# Import database components
from app.db.base import Base  
from app.db.session import engine, get_session 
from app.api.v1.endpoints.vision import router as vision_router
from app.api.v1.endpoints.translation import router as translation_router
from app.api.v1.endpoints.healthcare_facilities import router as healthcare_facilities_router
from app.api.v1.endpoints.govt_healthcare_facility import router as govt_healthcare_facility_router
from app.api.v1.endpoints.emergency_facility import router as emergency_facility_router
from app.api.v1.endpoints.logs import router as logs_router 
from app.api.v1.endpoints.healthcare_schemes import router as healthcare_schemes_router
from app.api.v1.endpoints.user_intent_classifier import router as user_intent_classifier_router
from app.api.v1.endpoints.voice import router as voice_router
from app.api.v1.endpoints.llm import router as llm_router

# Configure basic logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="ArogyaMitra API Backend"
)

# Enable CORS for frontend clients & Expo simulation
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Device Identification & Isolation Middleware
@app.middleware("http")
async def device_id_middleware(request: Request, call_next):
    device_id = request.headers.get("X-Device-ID", "anonymous-device")
    logger.info(f"[Device-ID: {device_id}] Request: {request.method} {request.url.path}")
    
    response = await call_next(request)
    response.headers["X-Device-ID-Echo"] = device_id
    return response

# Register routers
app.include_router(vision_router, prefix='/api/v1')
app.include_router(translation_router, prefix='/api/v1')
app.include_router(healthcare_facilities_router, prefix='/api/v1')
app.include_router(govt_healthcare_facility_router, prefix='/api/v1')
app.include_router(emergency_facility_router, prefix='/api/v1')
app.include_router(logs_router, prefix='/api/v1')
app.include_router(healthcare_schemes_router, prefix='/api/v1/schemes', tags=["Healthcare Schemes"])
app.include_router(user_intent_classifier_router, prefix="/api/v1/router", tags=["User Intent Router"])
app.include_router(voice_router, prefix="/api/v1")
app.include_router(llm_router, prefix="/api/v1")

# Define session type alias
SessionDep = Annotated[AsyncSession, Depends(get_session)]

# --- Test Endpoints ---
@app.get("/", tags=["Health Check"])
async def root():
    return {
        "message": "Welcome to the ArogyaMitra Servers"
    }

@app.get("/api/v1/session-info", tags=["Session and Identity"])
async def session_info(request: Request):
    device_id = request.headers.get("X-Device-ID", "anonymous-device")
    return {
        "status": "active",
        "device_id": device_id,
        "message": f"Session isolated for device: {device_id}"
    }

@app.get("/db-status", tags=["Health Check"])
async def check_db_connection(session: SessionDep):
    try:
        result = await session.execute(text("SELECT 1"))
        return {
            "status": "Success", 
            "message": "Database connection and session are functional."
        }
    except Exception as e:
        logger.error(f"Endpoint DB check failed: {e}")
        raise HTTPException(status_code=500, detail=f"Database operational check failed: {e}")
