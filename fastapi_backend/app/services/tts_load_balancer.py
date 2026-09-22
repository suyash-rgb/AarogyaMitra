import asyncio
import logging
from typing import Dict, Any, List, Optional

from app.services.indic_tts_service import indic_tts_service
from app.services.meta_mms_tts_service import meta_mms_tts_service
from app.services.gtts_service import gtts_service
from app.services.cache_service import cache_service

logger = logging.getLogger(__name__)

class TTSLoadBalancer:
    """
    Weighted Round-Robin (WRR) and Dynamic Load-Aware TTS Service Load Balancer.
    Delegates requests between:
      1. Indic-TTS Service (AI4Bharat / Piper ONNX - Highest priority / most natural)
      2. Meta MMS-TTS Service (Facebook VITS - High language coverage)
      3. gTTS Service (Google TTS - High availability fallback)
    """

    def __init__(self, max_concurrent_indic: int = 3):
        self.max_concurrent_indic = max_concurrent_indic
        self._active_counts = {
            "indic_tts": 0,
            "meta_mms": 0,
            "gtts": 0
        }
        self._lock = asyncio.Lock()
        
        # Engine Weights for Weighted Round-Robin
        self.weights = {
            "indic_tts": 5,
            "meta_mms": 3,
            "gtts": 2
        }
        
        # Current state for smooth Weighted Round Robin
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
        """Returns current load balancer status and active request metrics."""
        return {
            "max_concurrent_indic": self.max_concurrent_indic,
            "active_requests": dict(self._active_counts),
            "weights": self.weights,
            "total_requests_processed": self._request_counter
        }

    async def _select_candidate_engines(self, lang_tag: str) -> List[str]:
        """
        Determines the priority-ordered list of candidate engines based on:
        1. Language support
        2. Current concurrent load on Indic-TTS
        3. Weighted Round Robin balancing for overflow/secondary traffic
        """
        async with self._lock:
            self._request_counter += 1
            current_count = self._request_counter

        indic_supported = self._is_engine_supported("indic_tts", lang_tag)
        meta_supported = self._is_engine_supported("meta_mms", lang_tag)
        gtts_supported = self._is_engine_supported("gtts", lang_tag)

        indic_busy = self._active_counts["indic_tts"] >= self.max_concurrent_indic

        candidates = []

        # Rule 1: Indic-TTS gets top priority if supported and not overloaded
        if indic_supported and not indic_busy:
            candidates.append("indic_tts")

        # Prepare secondary candidates (meta_mms vs gtts)
        secondary = []
        if meta_supported:
            secondary.append("meta_mms")
        if gtts_supported:
            secondary.append("gtts")

        # If Indic-TTS is busy or unsupported, or for general WRR distribution
        if secondary:
            # Weighted Round-Robin ordering between secondary engines
            # Meta weight: 3, gTTS weight: 2 -> 3:2 ratio
            if len(secondary) > 1:
                # Interleaved selection based on request counter
                if (current_count % 5) in [1, 2, 3]:
                    wrr_ordered = ["meta_mms", "gtts"]
                else:
                    wrr_ordered = ["gtts", "meta_mms"]
            else:
                wrr_ordered = secondary

            for eng in wrr_ordered:
                if eng not in candidates:
                    candidates.append(eng)

        # If Indic-TTS is supported but was busy, add it as a late fallback option
        if indic_supported and "indic_tts" not in candidates:
            candidates.append("indic_tts")

        return candidates

    async def text_to_speech(self, text: str, lang_tag: str = "hin_Deva", slow: bool = False) -> Dict[str, Any]:
        """
        Synthesize speech with load balancing, load shedding, and automatic failover cascade.
        """
        if not text or not text.strip():
            raise ValueError("Text content cannot be empty.")

        # Step 1: Check candidate engines
        candidates = await self._select_candidate_engines(lang_tag)
        if not candidates:
            logger.error(f"No TTS engines supported for language tag: {lang_tag}")
            # Fallback to gTTS as absolute safety net
            candidates = ["gtts"]

        logger.info(f"[TTS Load Balancer] Request for '{lang_tag}'. Candidate order: {candidates}. Active counts: {self._active_counts}")

        # Step 2: Cascade through candidate engines until success
        last_exception = None
        for engine_name in candidates:
            service = self.services[engine_name]
            
            # Increment active request counter
            async with self._lock:
                self._active_counts[engine_name] += 1
            
            try:
                logger.info(f"[TTS Load Balancer] Invoking engine '{engine_name}'...")
                res = await service.text_to_speech(text=text, lang_tag=lang_tag, slow=slow)
                
                audio_b64 = res.get("audio_base64", "")
                if audio_b64 and "AUDIO_DUMMY_DATA" not in audio_b64:
                    res["lb_engine_used"] = engine_name
                    return res
                else:
                    logger.warning(f"[TTS Load Balancer] Engine '{engine_name}' returned empty or dummy audio; cascading to next engine...")
            except Exception as e:
                logger.warning(f"[TTS Load Balancer] Engine '{engine_name}' failed with error: {e}. Cascading...")
                last_exception = e
            finally:
                async with self._lock:
                    self._active_counts[engine_name] = max(0, self._active_counts[engine_name] - 1)

        # If all candidates fail, attempt final gTTS call
        try:
            logger.error("[TTS Load Balancer] All primary candidates failed. Attempting final emergency gTTS synthesis.")
            res = await gtts_service.text_to_speech(text=text, lang_tag=lang_tag, slow=slow)
            res["lb_engine_used"] = "emergency_gtts"
            return res
        except Exception as final_err:
            raise RuntimeError(f"All load-balanced TTS engines failed. Last error: {last_exception or final_err}")

tts_load_balancer = TTSLoadBalancer()
