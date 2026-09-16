from pydantic import BaseModel, Field
from typing import Optional, Dict, Any, List
from enum import Enum

class IntentEnum(str, Enum):
    GOVT_SCHEMES_DISCOVERY = "GOVT_SCHEMES_DISCOVERY"
    FACILITY_DISCOVERY = "FACILITY_DISCOVERY"
    GENERAL_MEDICAL_QA = "GENERAL_MEDICAL_QA"
    GREETING_CONVERSATIONAL = "GREETING_CONVERSATIONAL"

class UserContext(BaseModel):
    state: Optional[str] = None
    district: Optional[str] = None
    pincode: Optional[str] = None
    language: Optional[str] = "en"

class IntentRequest(BaseModel):
    query: str
    user_context: Optional[UserContext] = None

class ExtractedSlots(BaseModel):
    specialty: Optional[str] = None
    pincode: Optional[str] = None
    state: Optional[str] = None
    district: Optional[str] = None
    disease: Optional[str] = None

class IntentResponse(BaseModel):
    intent: IntentEnum
    confidence: float
    method: str
    translated_query: Optional[str] = None
    extracted_slots: ExtractedSlots
    response_data: Optional[Dict[str, Any]] = None
