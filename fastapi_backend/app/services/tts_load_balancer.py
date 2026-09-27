import asyncio
import logging
from typing import Dict, Any, List, Optional

from app.services.indic_tts_service import indic_tts_service
from app.services.meta_mms_tts_service import meta_mms_tts_service
from app.services.gtts_service import gtts_service
from app.services.cache_service import cache_service
from app.services.telemetry_service import telemetry_service

logger = logging.getLogger(__name__)

class TTSLoadBalancer:
    def __init__(self, max_concurrent_indic: int = 3):
        self.max_concurrent_indic = max_concurrent_indic
        self._active_counts = {
            "indic_tts": 0,
            "meta_mms": 0,
            "gtts": 0
        }
        self._lock = asyncio.Lock()
        
        self.weights = {
            "indic_tts": 5,
            "meta_mms": 3,
            "gtts": 2
        }
        
        self._current_rr_index = 0
        self._request_counter = 0

        self.services = {
            "indic_tts": indic_tts_service,
            "meta_mms": meta_mms_tts_service,
            "gtts": gtts_service
        }

    def _is_engine_supported(self, engine_name: str, lang_tag: str) -> bool:
        service = self.services.get(engine_name)
        if not service:
            return False
        if hasattr(service, "is_language_supported"):
            return service.is_language_supported(lang_tag)
        return True

    def get_status(self) -> Dict[str, Any]:
        return {
            "max_concurrent_indic": self.max_concurrent_indic,
            "active_requests": dict(self._active_counts),
            "weights": self.weights,
            "total_requests_processed": self._request_counter
        }

    async def _select_candidate_engines(self, lang_tag: str) -> List[str]:
        async with self._lock:
            self._request_counter += 1
            current_count = self._request_counter

        indic_supported = self._is_engine_supported("indic_tts", lang_tag)
        meta_supported = self._is_engine_supported("meta_mms", lang_tag)
        gtts_supported = self._is_engine_supported("gtts", lang_tag)

        indic_busy = self._active_counts["indic_tts"] >= self.max_concurrent_indic

        candidates = []

        if indic_supported and not indic_busy:
            candidates.append("indic_tts")

        secondary = []
        if meta_supported:
            secondary.append("meta_mms")
        if gtts_supported:
            secondary.append("gtts")

        if secondary:
            if len(secondary) > 1:
                if (current_count % 5) in [1, 2, 3]:
                    wrr_ordered = ["meta_mms", "gtts"]
                else:
                    wrr_ordered = ["gtts", "meta_mms"]
            else:
                wrr_ordered = secondary

            for eng in wrr_ordered:
                if eng not in candidates:
                    candidates.append(eng)

        if indic_supported and "indic_tts" not in candidates:
            candidates.append("indic_tts")

        return candidates

    async def text_to_speech(
        self,
        text: str,
        lang_tag: str = "hin_Deva",
        slow: bool = False,
        trace_id: Optional[str] = None
    ) -> Dict[str, Any]:
        if not text or not text.strip():
            raise ValueError("Text content cannot be empty.")

        meta = {"lang_tag": lang_tag, "text_len": len(text), "slow": slow}

        with telemetry_service.span("tts_speech_synthesis", trace_id=trace_id, meta=meta) as span:
            candidates = await self._select_candidate_engines(lang_tag)
            if not candidates:
                logger.error(f"No TTS engines supported for language tag: {lang_tag}")
                candidates = ["gtts"]

            logger.info(f"[TTS Load Balancer] Request for '{lang_tag}'. Candidate order: {candidates}. Active counts: {self._active_counts}")

            last_exception = None
            for engine_name in candidates:
                service = self.services[engine_name]
                
                async with self._lock:
                    self._active_counts[engine_name] += 1
                
                try:
                    logger.info(f"[TTS Load Balancer] Invoking engine '{engine_name}'...")
                    res = await service.text_to_speech(text=text, lang_tag=lang_tag, slow=slow)
                    
                    audio_b64 = res.get("audio_base64", "")
                    if audio_b64 and "AUDIO_DUMMY_DATA" not in audio_b64:
                        res["lb_engine_used"] = engine_name
                        span.set_metric("engine_used", engine_name)
                        span.set_metric("audio_bytes_len", len(audio_b64))
                        return res
                    else:
                        logger.warning(f"[TTS Load Balancer] Engine '{engine_name}' returned empty or dummy audio; cascading to next engine...")
                except Exception as e:
                    logger.warning(f"[TTS Load Balancer] Engine '{engine_name}' failed with error: {e}. Cascading...")
                    last_exception = e
                finally:
                    async with self._lock:
                        self._active_counts[engine_name] = max(0, self._active_counts[engine_name] - 1)

            try:
                logger.error("[TTS Load Balancer] All primary candidates failed. Attempting final emergency gTTS synthesis.")
                res = await gtts_service.text_to_speech(text=text, lang_tag=lang_tag, slow=slow)
                res["lb_engine_used"] = "emergency_gtts"
                span.set_metric("engine_used", "emergency_gtts")
                return res
            except Exception as final_err:
                span.record_error(final_err)
                raise RuntimeError(f"All load-balanced TTS engines failed. Last error: {last_exception or final_err}")

tts_load_balancer = TTSLoadBalancer()
