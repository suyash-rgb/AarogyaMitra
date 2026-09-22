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

    def _find_model_file(self, lang_code: str) -> Optional[str]:
        lang_dir = os.path.join(self.models_dir, lang_code)
        if not os.path.isdir(lang_dir):
            return None
        for file in os.listdir(lang_dir):
            if file.endswith(".onnx") and not file.endswith(".onnx.json"):
                return os.path.join(lang_dir, file)
        return None

    def is_language_supported(self, lang_tag: str) -> bool:
        indic_lang = self._get_indic_lang_code(lang_tag)
        model_path = self._find_model_file(indic_lang)
        return model_path is not None and PiperVoice is not None

    def _get_indic_lang_code(self, lang_tag: str) -> str:
        return INDIC_TTS_LANG_MAP.get(lang_tag, "hi")

    def _load_voice(self, lang_code: str):
        if lang_code in self.voices:
            return self.voices[lang_code]
        
        model_path = self._find_model_file(lang_code)
        if model_path and os.path.exists(model_path) and PiperVoice is not None:
            logger.info(f"Loading Piper ONNX model for {lang_code} from {model_path}...")
            try:
                self.voices[lang_code] = PiperVoice.load(model_path)
                return self.voices[lang_code]
            except Exception as e:
                logger.error(f"Failed to load Piper voice for {lang_code}: {e}")
                return None
        else:
            logger.warning(f"ONNX model for {lang_code} not found at {model_path} or PiperVoice not installed.")
        
        return None

indic_tts_service = IndicTTSService()
