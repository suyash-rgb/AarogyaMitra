import os
import re
import time
import json
import logging
from datetime import datetime
from typing import Optional, Dict, Any, List

from app.services.telemetry_service import telemetry_service

logger = logging.getLogger(__name__)

class LLMService:
    _instance: Optional['LLMService'] = None

    DEFAULT_SYSTEM_PROMPT = (
        "You are AarogyaMitra, an empathetic, highly knowledgeable AI healthcare assistant for rural India. "
        "Provide accurate medical advice, guidance, and first-aid steps in clear bullet points."
    )

    def __init__(self, model_path: Optional[str] = None):
        if model_path is None:
            backend_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
            model_path = os.path.join(backend_dir, "models", "Qwen3.5-2B.Q4_K_M.gguf")
        
        self.model_path = model_path
        self._model = None

    def _initialize_model(self):
        if self._model is not None:
            return

        if not os.path.exists(self.model_path):
            logger.error(f"Fine-tuned GGUF model not found at path: {self.model_path}")
            raise FileNotFoundError(f"Model file missing at: {self.model_path}")

        try:
            from llama_cpp import Llama
            logger.info(f"Loading fine-tuned model from {self.model_path}...")
            start_time = time.time()
            self._model = Llama(
                model_path=self.model_path,
                n_ctx=2048,
                n_threads=min(os.cpu_count() or 4, 6),
                verbose=False
            )
            logger.info(f"Model loaded successfully in {time.time() - start_time:.2f}s")
        except Exception as e:
            logger.error(f"Failed to load GGUF model via llama_cpp: {e}")
            raise RuntimeError(f"Model loading error: {e}")

    @classmethod
    def get_instance(cls, model_path: Optional[str] = None) -> 'LLMService':
        if cls._instance is None:
            cls._instance = LLMService(model_path=model_path)
        return cls._instance

    def _clean_response(self, text: str) -> str:
        cleaned = re.sub(r'<think>.*?</think>', '', text, flags=re.DOTALL).strip()
        cleaned = re.sub(r'</?think>', '', cleaned).strip()
        return cleaned

    def generate_response(
        self,
        prompt: str,
        system_prompt: Optional[str] = None,
        target_intent: Optional[str] = None,
        max_tokens: int = 512,
        temperature: float = 0.7,
        top_p: float = 0.9,
        repeat_penalty: float = 1.15,
        stop: Optional[List[str]] = None,
        trace_id: Optional[str] = None
    ) -> Dict[str, Any]:
        if self._model is None:
            self._initialize_model()

        sys_prompt = system_prompt or self.DEFAULT_SYSTEM_PROMPT
        formatted_prompt = (
            f"<|im_start|>system\n{sys_prompt}<|im_end|>\n"
            f"<|im_start|>user\n{prompt}<|im_end|>\n"
            f"<|im_start|>assistant\n"
        )

        stop_tokens = stop or ["<|im_end|>", "<|endoftext|>"]
        meta_info = {
            "model_name": os.path.basename(self.model_path),
            "target_intent": target_intent,
            "prompt_length": len(prompt)
        }

        with telemetry_service.span("qwen_llm_generation", trace_id=trace_id, meta=meta_info) as span:
            logger.info(f"Generating response from fine-tuned LLM service... (repeat_penalty={repeat_penalty})")
            start_perf = time.perf_counter()
            
            raw_text_parts = []
            ttft_ms = None
            token_count = 0

            try:
                stream = self._model(
                    prompt=formatted_prompt,
                    max_tokens=max_tokens,
                    temperature=temperature,
                    top_p=top_p,
                    repeat_penalty=repeat_penalty,
                    stop=stop_tokens,
                    echo=False,
                    stream=True
                )

                for chunk in stream:
                    if ttft_ms is None:
                        ttft_ms = (time.perf_counter() - start_perf) * 1000
                    
                    if chunk and "choices" in chunk and len(chunk["choices"]) > 0:
                        delta = chunk["choices"][0].get("text", "")
                        if delta:
                            raw_text_parts.append(delta)
                            token_count += 1
                
                raw_text = "".join(raw_text_parts)

            except Exception as stream_e:
                logger.warning(f"Streaming generation failed, falling back to non-streaming mode: {stream_e}")
                output = self._model(
                    prompt=formatted_prompt,
                    max_tokens=max_tokens,
                    temperature=temperature,
                    top_p=top_p,
                    repeat_penalty=repeat_penalty,
                    stop=stop_tokens,
                    echo=False
                )
                raw_text = ""
                if output and "choices" in output and len(output["choices"]) > 0:
                    raw_text = output["choices"][0].get("text", "").strip()

            duration_sec = time.perf_counter() - start_perf
            cleaned_text = self._clean_response(raw_text)
            tokens_per_sec = round(token_count / duration_sec, 2) if duration_sec > 0 else 0.0

            if ttft_ms is not None:
                span.set_ttft(ttft_ms)

            span.set_metric("generated_tokens", token_count)
            span.set_metric("tokens_per_sec", tokens_per_sec)
            span.set_metric("raw_length", len(raw_text))
            span.set_metric("clean_length", len(cleaned_text))

            result_data = {
                "response": cleaned_text,
                "raw_response": raw_text,
                "execution_time_sec": round(duration_sec, 3),
                "ttft_ms": round(ttft_ms, 2) if ttft_ms else None,
                "usage": {"completion_tokens": token_count},
                "model_name": os.path.basename(self.model_path),
                "target_intent": target_intent
            }

            try:
                log_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), "logs")
                os.makedirs(log_dir, exist_ok=True)
                
                jsonl_log_path = os.path.join(log_dir, "llm_evaluations.jsonl")
                log_entry = {
                    "timestamp": datetime.utcnow().isoformat() + "Z",
                    "trace_id": span.trace_id,
                    "prompt": prompt,
                    "system_prompt": sys_prompt,
                    "target_intent": target_intent,
                    "max_tokens": max_tokens,
                    "temperature": temperature,
                    "top_p": top_p,
                    "repeat_penalty": repeat_penalty,
                    "model_name": result_data["model_name"],
                    "execution_time_sec": result_data["execution_time_sec"],
                    "ttft_ms": result_data["ttft_ms"],
                    "usage": result_data["usage"],
                    "response": result_data["response"],
                    "raw_response": result_data["raw_response"]
                }
                with open(jsonl_log_path, "a", encoding="utf-8") as f:
                    f.write(json.dumps(log_entry) + "\n")
            except Exception as log_e:
                logger.error(f"Failed to log LLM evaluation query: {log_e}")

            return result_data

def get_llm_service() -> LLMService:
    return LLMService.get_instance()
