import logging
from fastapi import APIRouter, HTTPException, status
from app.schemas.llm import LLMQueryRequest, LLMQueryResponse
from app.services.llm_service import get_llm_service

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/llm", tags=["LLM Inference Service"])

@router.post("/query", response_model=LLMQueryResponse)
async def query_llm(request: LLMQueryRequest):
    """
    Execute inference against the fine-tuned GGUF model (Qwen 3.5 2B Q4_K_M).
    """
    try:
        service = get_llm_service()
        result = service.generate_response(
            prompt=request.prompt,
            system_prompt=request.system_prompt,
            target_intent=request.target_intent,
            max_tokens=request.max_tokens or 512,
            temperature=request.temperature or 0.7,
            top_p=request.top_p or 0.9,
            repeat_penalty=request.repeat_penalty or 1.15
        )
        return LLMQueryResponse(
            response=result["response"],
            execution_time_sec=result["execution_time_sec"],
            usage=result.get("usage"),
            model_name=result["model_name"]
        )
    except FileNotFoundError as fnf:
        logger.error(f"Model file not found: {fnf}")
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail=f"Fine-tuned model file unavailable: {fnf}"
        )
    except Exception as e:
        logger.error(f"Error during LLM inference: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"LLM inference error: {str(e)}"
        )
