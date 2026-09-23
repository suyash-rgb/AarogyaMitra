import time
import logging
from fastapi import APIRouter, HTTPException, status
from app.schemas.llm import LLMQueryRequest, LLMQueryResponse
from app.services.llm_service import get_llm_service
from app.services.translation_service import translation_service
from app.utils.language import detect_indic_language

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/llm", tags=["LLM Inference Service"])

@router.post("/query", response_model=LLMQueryResponse)
async def query_llm(request: LLMQueryRequest):
    """
    Orchestrated Translate-Inference-Translate Pipeline:
    1. IndicLID: Detect language of input prompt (or use request.src_lang).
    2. IndicTrans2: Translate input query from Indic Language -> English.
    3. AarogyaMitra Qwen 3.5 2B: Execute clinical reasoning in English with repeat_penalty=1.15.
    4. IndicTrans2: Translate English clinical triage response back to detected Indic language.
    5. Patient receives clinical advice in their native language.
    """
    start_total_time = time.time()
    raw_prompt = request.prompt.strip()
    
    if not raw_prompt:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Prompt text cannot be empty."
        )

    try:
        # Step 1: IndicLID (Language Identification)
        detected_lang = request.src_lang or detect_indic_language(raw_prompt)
        logger.info(f"Pipeline Step 1 (IndicLID): Detected language '{detected_lang}'")

        # Step 2: IndicTrans2 (Indic -> English)
        if detected_lang != "eng_Latn":
            logger.info(f"Pipeline Step 2 (IndicTrans2): Translating prompt '{detected_lang}' -> 'eng_Latn'")
            english_prompt = await translation_service.translate(
                text=raw_prompt,
                src_lang=detected_lang,
                tgt_lang="eng_Latn"
            )
        else:
            english_prompt = raw_prompt

        logger.info(f"English reasoning prompt: '{english_prompt}'")

        # Step 3: AarogyaMitra Qwen 3.5 2B (Clinical Reasoning in English)
        logger.info("Pipeline Step 3 (Qwen 3.5 2B): Executing clinical reasoning in English...")
        llm_service = get_llm_service()
        llm_result = llm_service.generate_response(
            prompt=english_prompt,
            system_prompt=request.system_prompt,
            target_intent=request.target_intent,
            max_tokens=request.max_tokens or 512,
            temperature=request.temperature or 0.7,
            top_p=request.top_p or 0.9,
            repeat_penalty=request.repeat_penalty or 1.15
        )

        english_response = llm_result["response"]

        # Step 4: IndicTrans2 (English -> Detected Indic Language)
        if detected_lang != "eng_Latn":
            logger.info(f"Pipeline Step 4 (IndicTrans2): Translating response 'eng_Latn' -> '{detected_lang}'")
            final_response = await translation_service.translate(
                text=english_response,
                src_lang="eng_Latn",
                tgt_lang=detected_lang
            )
        else:
            final_response = english_response

        total_elapsed = round(time.time() - start_total_time, 3)
        logger.info(f"Pipeline Completed in {total_elapsed}s for language '{detected_lang}'")

        return LLMQueryResponse(
            response=final_response,
            detected_language=detected_lang,
            translated_prompt=english_prompt if detected_lang != "eng_Latn" else None,
            english_response=english_response if detected_lang != "eng_Latn" else None,
            execution_time_sec=total_elapsed,
            usage=llm_result.get("usage"),
            model_name=llm_result["model_name"]
        )

    except FileNotFoundError as fnf:
        logger.error(f"Model file not found: {fnf}")
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail=f"Fine-tuned model file unavailable: {fnf}"
        )
    except Exception as e:
        logger.error(f"Error during Orchestrated LLM Pipeline: {e}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"LLM Orchestrated Pipeline error: {str(e)}"
        )
