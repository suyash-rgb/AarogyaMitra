import logging
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Dict, Any

from app.db.session import get_session
from app.schemas.user_intent_classifier import (
    IntentRequest, IntentResponse, IntentEnum, ExtractedSlots
)
from app.services.user_intent_classifier_service import intent_classifier_service
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
    db: AsyncSession = Depends(get_session)
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

    # Step 2: Slot Extraction & Intent Classification
    extracted_slots = intent_classifier_service.extract_slots(classification_text)

    # Merge context hints if provided in request
    if user_context:
        if user_context.state and not extracted_slots.state:
            extracted_slots.state = user_context.state
        if user_context.pincode and not extracted_slots.pincode:
            extracted_slots.pincode = user_context.pincode

    intent, confidence, method = intent_classifier_service.classify_intent(classification_text)

    logger.info(f"Query: '{query}' -> Intent: {intent} (Confidence: {confidence}, Method: {method})")

    # Step 3: Execute Target Service API
    response_data: Dict[str, Any] = {}

    try:
        if intent == IntentEnum.GOVT_SCHEMES_DISCOVERY:
            # Query schemes service
            state_query = extracted_slots.state or (user_context.state if user_context else None)
            
            schemes_res = await schemes_service.get_schemes_paginated(
                db=db,
                search=classification_text,
                state=state_query,
                page=1,
                limit=5
            )
            
            # get_schemes_paginated returns a Pydantic model (HealthSchemePaginatedResponse)
            # so we access attributes with dot notation or dict if it's a dict
            items = getattr(schemes_res, "items", []) if not isinstance(schemes_res, dict) else schemes_res.get("items", [])
            total = getattr(schemes_res, "total", 0) if not isinstance(schemes_res, dict) else schemes_res.get("total", 0)
            
            response_data = {
                "message": f"Found matching government health schemes.",
                "schemes": items,
                "total": total
            }

        elif intent == IntentEnum.FACILITY_DISCOVERY:
            # Query healthcare facility service
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
                "message": f"Found nearby healthcare facilities.",
                "facilities": getattr(facility_res, "items", []) if not isinstance(facility_res, dict) else facility_res.get("items", []),
                "total": getattr(facility_res, "total", 0) if not isinstance(facility_res, dict) else facility_res.get("total", 0)
            }

        elif intent == IntentEnum.GREETING_CONVERSATIONAL:
            response_data = {
                "message": "Namaste! I am ArogyaMitra, your AI healthcare assistant. How can I assist you with government health schemes or finding nearest medical facilities today?"
            }

        elif intent == IntentEnum.GENERAL_MEDICAL_QA:
            response_data = {
                "message": "Directing your question to our AI Medical Advice Assistant...",
                "routing_target": "GROQ_MEDICAL_RAG"
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
