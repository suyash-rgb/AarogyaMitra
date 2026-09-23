from pydantic import BaseModel, Field
from typing import Optional, Dict, Any

class LLMQueryRequest(BaseModel):
    prompt: str = Field(..., description="The user query or prompt for the LLM")
    src_lang: Optional[str] = Field(None, description="Optional source language tag (e.g. hin_Deva, ben_Beng). Auto-detected via IndicLID if null.")
    system_prompt: Optional[str] = Field(None, description="Optional custom system prompt")
    target_intent: Optional[str] = Field(None, description="The classified intent of the user query")
    max_tokens: Optional[int] = Field(512, description="Maximum response tokens")
    temperature: Optional[float] = Field(0.7, description="Sampling temperature")
    top_p: Optional[float] = Field(0.9, description="Top-p nucleus sampling parameter")
    repeat_penalty: Optional[float] = Field(1.15, description="Penalty for token repetition")

class LLMQueryResponse(BaseModel):
    response: str = Field(..., description="The generated response text in the patient native language")
    detected_language: str = Field(..., description="Language tag identified by IndicLID or specified by user")
    translated_prompt: Optional[str] = Field(None, description="English translation of the prompt used for LLM reasoning")
    english_response: Optional[str] = Field(None, description="Raw clinical reasoning output from Qwen 3.5 2B in English")
    execution_time_sec: float = Field(..., description="Total processing time in seconds")
    usage: Optional[Dict[str, Any]] = Field(None, description="Token usage stats")
    model_name: str = Field(..., description="Name of the model file used")
