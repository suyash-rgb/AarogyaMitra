import io
import wave
import base64
import hashlib
import asyncio
import logging
import os
from typing import Dict, Any, Optional

try:
    from piper import PiperVoice
except ImportError:
    PiperVoice = None

from app.services.cache_service import cache_service
from app.core.config import settings

logger = logging.getLogger(__name__)

# AI4Bharat Indic-TTS Language Mapping for 13 supported Indian languages
INDIC_TTS_LANG_MAP = {
    "hin_Deva": "hi",
    "mar_Deva": "mr",
    "tam_Taml": "ta",
    "tel_Telu": "te",
    "ben_Beng": "bn",
    "guj_Gujr": "gu",
    "kan_Knda": "kn",
    "mal_Mlym": "ml",
    "pan_Guru": "pa",
    "ory_Orya": "or",
    "urd_Arab": "ur",
    "asm_Beng": "as",
    "san_Deva": "sa",
    "bho_Deva": "hi",
    "awa_Deva": "hi",
    "mai_Deva": "hi",
    "mag_Deva": "hi",
    "brx_Deva": "hi",
    "kas_Deva": "hi",
    "kas_Arab": "ur",
    "eng_Latn": "en"
}

class IndicTTSService:
    def __init__(self):
        self._load_lock = asyncio.Lock()
        self.voices = {}
        # Path: fastapi_backend/models/indic_tts
        self.models_dir = os.path.join(os.path.dirname(__file__), "..", "..", "models", "indic_tts")

    def _get_indic_lang_code(self, lang_tag: str) -> str:
        return INDIC_TTS_LANG_MAP.get(lang_tag, "hi")

    def _load_voice(self, lang_code: str):
        if lang_code in self.voices:
            return self.voices[lang_code]
        
        # Currently we only have Hindi downloaded
        if lang_code == "hi":
            model_path = os.path.join(self.models_dir, "hi", "hi_IN-pratham-medium.onnx")
            if os.path.exists(model_path) and PiperVoice is not None:
                logger.info(f"Loading Piper ONNX model for {lang_code} from {model_path}...")
                self.voices[lang_code] = PiperVoice.load(model_path)
                return self.voices[lang_code]
            else:
                logger.warning(f"ONNX model for {lang_code} not found or PiperVoice not installed.")
        
        return None

    async def text_to_speech(self, text: str, lang_tag: str = "hin_Deva", slow: bool = False) -> Dict[str, Any]:
        if not text or not text.strip():
            raise ValueError("Text content cannot be empty.")

        indic_lang = self._get_indic_lang_code(lang_tag)
        text_hash = hashlib.sha256(text.strip().encode("utf-8")).hexdigest()
        cache_key = f"{lang_tag}:{indic_lang}:{text_hash}"

        # 2-Tier Cache Check
        cached_b64 = cache_service.get(namespace="indic_tts", key=cache_key)
        if cached_b64 and isinstance(cached_b64, str):
            logger.info(f"AI4Bharat Indic-TTS Cache HIT for key: {cache_key[:25]}...")
            return {
                "audio_base64": cached_b64,
                "language_tag": lang_tag,
                "text": text,
                "format": "wav",
                "engine": f"ai4bharat-indic-tts-onnx-{indic_lang}",
                "cache_key": f"indic_tts:{cache_key}"
            }

        # Synthesize audio with Piper ONNX pipeline
        def _tts_sync():
            clean_text = text.replace("*", "").replace("#", "").replace("-", " ").strip()
            if not clean_text:
                clean_text = text

            voice = self._load_voice(indic_lang)
            if not voice:
                logger.error(f"Voice model for {indic_lang} not loaded or missing. PiperVoice is {PiperVoice}, models_dir is {self.models_dir}"); open("indic_tts_debug.log", "a").write(f"[DEBUG] Voice missing. PiperVoice: {PiperVoice}, models_dir: {self.models_dir}\n")
                return None

            try:
                # Piper synthesizes raw WAV audio
                wav_io = io.BytesIO()
                with wave.open(wav_io, 'wb') as wav_file:
                    voice.synthesize_wav(clean_text, wav_file)
                wav_io.seek(0)
                return base64.b64encode(wav_io.read()).decode("utf-8")
            except Exception as e:
                logger.error(f"Piper ONNX synthesis error: {e}"); open("indic_tts_debug.log", "a").write(f"[DEBUG] Synthesis error: {e}\n")
                return None

        audio_b64 = await asyncio.to_thread(_tts_sync)

        if not audio_b64:
            # Fallback to gTTS if Indic-TTS ONNX model is missing or fails
            from gtts import gTTS
            def _gtts_fallback():
                tts_lang = lang_tag.split("_")[0][:2]
                tts = gTTS(text=text[:300], lang=tts_lang, slow=slow)
                fp = io.BytesIO()
                tts.write_to_fp(fp)
                fp.seek(0)
                return base64.b64encode(fp.read()).decode("utf-8")

            try:
                fallback_b64 = await asyncio.to_thread(_gtts_fallback)
                cache_service.set(
                    namespace="indic_tts",
                    key=cache_key,
                    value=fallback_b64,
                    ttl=settings.VALKEY_TTS_TTL_SECONDS
                )
                return {
                    "audio_base64": fallback_b64,
                    "language_tag": lang_tag,
                    "text": text,
                    "format": "mp3",
                    "engine": f"gtts_fallback_{indic_lang}",
                    "cache_key": f"indic_tts:{cache_key}"
                }
            except Exception as e2:
                logger.error(f"Indic-TTS gTTS fallback error: {e2}")
                return {
                    "audio_base64": base64.b64encode(b"AUDIO_DUMMY_DATA").decode("utf-8"),
                    "language_tag": lang_tag,
                    "text": text,
                    "format": "wav",
                    "engine": "fallback",
                    "error": "Model missing and fallback failed",
                    "cache_key": None
                }

        # Store in 2-Tier Cache if valid audio
        cache_service.set(
            namespace="indic_tts",
            key=cache_key,
            value=audio_b64,
            ttl=settings.VALKEY_TTS_TTL_SECONDS
        )

        return {
            "audio_base64": audio_b64,
            "language_tag": lang_tag,
            "text": text,
            "format": "wav",
            "engine": f"ai4bharat-indic-tts-onnx-{indic_lang}",
                "cache_key": f"indic_tts:{cache_key}"
        }

indic_tts_service = IndicTTSService()
