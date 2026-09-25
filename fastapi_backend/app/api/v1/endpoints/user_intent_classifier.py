from fastapi import Query
import logging
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Dict, Any

from app.db.session import get_session
from app.schemas.user_intent_classifier import (
    IntentRequest, IntentResponse, IntentEnum, ExtractedSlots
)
from app.services.laya_service import laya_service
from app.services.healthcare_schemes_service import HealthCareSchemesService
from app.services.govt_healthcare_facility_service import GovtHealthcareFacilityService
from app.services.translation_service import TranslationService

logger = logging.getLogger(__name__)

router = APIRouter()

# Instantiate services
schemes_service = HealthCareSchemesService
facility_service = GovtHealthcareFacilityService()
translation_service = TranslationService()

@router.post("/classify", response_model=IntentResponse)
async def classify_and_route_user_intent(
    req: IntentRequest,
    db: AsyncSession = Depends(get_session),
    deviceId: str = Query(..., description="Device ID")
):
    query = req.query.strip()
    if not query:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Query string cannot be empty"
        )

    user_context = req.user_context
    src_lang = user_context.language if user_context and user_context.language else "en"
    translated_query = None

    # Step 1: Translation Pre-processing (if non-English)
    if src_lang.lower() not in ["en", "english"]:
        try:
            logger.info(f"Translating user query from '{src_lang}' to 'en'")
            translated_query = await translation_service.translate(query, src_lang=src_lang, tgt_lang="en")
            classification_text = translated_query
        except Exception as e:
            logger.warning(f"Translation failed: {e}. Defaulting to original text for classification.")
            classification_text = query
    else:
        classification_text = query

    # Step 2: Slot Extraction & Laya AI Intent Classification
    extracted_slots = laya_service.extract_slots(classification_text)

    # Merge context hints if provided in request
    if user_context:
        if user_context.state and not extracted_slots.state:
            extracted_slots.state = user_context.state
        if user_context.pincode and not extracted_slots.pincode:
            extracted_slots.pincode = user_context.pincode

    intent, confidence, method = laya_service.classify_intent(classification_text)

    logger.info(f"Query: '{query}' -> Intent: {intent} (Confidence: {confidence}, Method: {method})")

    # Step 3: Execute Target Service API / Orchestration Handler
    response_data: Dict[str, Any] = {}

    try:
        if intent in [IntentEnum.EMERGENCY_CRITICAL]:
            response_data = {
                "message": "EMERGENCY ALERT: For immediate medical emergencies, please call national emergency ambulance service 108 right away.",
                "emergency_contacts": [
                    {"title": "National Ambulance Service", "number": "108"},
                    {"title": "Health Information Helpline", "number": "104"}
                ],
                "routing_target": "H1_EMERGENCY_RED_FLAG_DISPATCHER"
            }

        elif intent in [IntentEnum.GOVT_SCHEME_ELIGIBILITY, IntentEnum.GOVT_SCHEMES_DISCOVERY]:
            state_query = extracted_slots.state or (user_context.state if user_context else None)
            
            schemes_res = await schemes_service.get_schemes_paginated(
                db=db,
                search=classification_text,
                state=state_query,
                page=1,
                limit=5
            )
            
            items = getattr(schemes_res, "items", []) if not isinstance(schemes_res, dict) else schemes_res.get("items", [])
            total = getattr(schemes_res, "total", 0) if not isinstance(schemes_res, dict) else schemes_res.get("total", 0)
            
            response_data = {
                "message": "Found matching government health schemes.",
                "schemes": items,
                "total": total,
                "routing_target": "H2_POSTGRES_SCHEMES_DB"
            }

        elif intent in [IntentEnum.FACILITY_LOCATOR, IntentEnum.FACILITY_DISCOVERY]:
            state_val = extracted_slots.state or (user_context.state if user_context else None)
            pin_val = extracted_slots.pincode or (user_context.pincode if user_context else None)
            
            q_parts = [classification_text]
            if extracted_slots.specialty:
                q_parts.append(extracted_slots.specialty)
            combined_query = " ".join(q_parts)

            facility_res = await facility_service.search_facilities(
                session=db,
                query_str=combined_query,
                state_name=state_val,
                pincode=pin_val,
                limit=5
            )
            response_data = {
                "message": "Found nearby healthcare facilities.",
                "facilities": getattr(facility_res, "items", []) if not isinstance(facility_res, dict) else facility_res.get("items", []),
                "total": getattr(facility_res, "total", 0) if not isinstance(facility_res, dict) else facility_res.get("total", 0),
                "routing_target": "H2_POSTGRES_SPATIAL_FACILITY_DB"
            }

        elif intent in [IntentEnum.MEDICINE_GENERIC_SEARCH]:
            response_data = {
                "message": "Searching generic medicine index and Jan Aushadhi Kendra availability...",
                "routing_target": "H4_IN_MEMORY_GENERIC_MEDICINE_INDEX"
            }

        elif intent in [IntentEnum.SYMPTOM_TRIAGE_REMEDY, IntentEnum.GENERAL_MEDICAL_QA]:
            response_data = {
                "message": "Directing your question to ICMR RAG & AI Medical Advice Assistant...",
                "routing_target": "H3_ICMR_RAG_QWEN"
            }

        elif intent in [IntentEnum.OUT_OF_SCOPE_GENERAL, IntentEnum.GREETING_CONVERSATIONAL]:
            response_data = {
                "message": "Namaste! I am ArogyaMitra, your AI healthcare assistant for rural India. How can I help you today with finding hospitals, government schemes, medicine information, or symptom guidance?",
                "routing_target": "H5_DIRECT_LIGHT_ENGINE"
            }

    except Exception as e:
        logger.error(f"Error executing target service for intent {intent}: {e}", exc_info=True)
        response_data = {
            "error": "Failed to execute target domain search.",
            "details": str(e)
        }

    return IntentResponse(
        intent=intent,
        confidence=confidence,
        method=method,
        translated_query=translated_query,
        extracted_slots=extracted_slots,
        response_data=response_data
    )
