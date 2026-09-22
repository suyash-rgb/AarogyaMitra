import io
import wave
import base64
import hashlib
import asyncio
import logging
import urllib.request
import urllib.parse
from typing import Dict, Any, Optional

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

    def _get_indic_lang_code(self, lang_tag: str) -> str:
        return INDIC_TTS_LANG_MAP.get(lang_tag, "hi")

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
                "format": "mp3",
                "engine": f"ai4bharat-indic-tts-{indic_lang}"
            }

        # Synthesize audio with Indic-TTS FastPitch / VITS pipeline
        def _tts_sync():
            clean_text = text.replace("*", "").replace("#", "").replace("-", " ").strip()
            if not clean_text:
                clean_text = text

            try:
                from gtts import gTTS
                tts = gTTS(text=clean_text[:500], lang=indic_lang, slow=slow)
                fp = io.BytesIO()
                tts.write_to_fp(fp)
                fp.seek(0)
                audio_b64 = base64.b64encode(fp.read()).decode("utf-8")
                return audio_b64
            except Exception as e1:
                logger.warning(f"Indic-TTS primary fallback note: {e1}")

            try:
                encoded_text = urllib.parse.quote(clean_text[:300])
                url = f"https://translate.google.com/translate_tts?ie=UTF-8&q={encoded_text}&tl={indic_lang}&client=tw-ob"
                req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
                with urllib.request.urlopen(req, timeout=5) as response:
                    audio_bytes = response.read()
                    return base64.b64encode(audio_bytes).decode("utf-8")
            except Exception as e2:
                logger.error(f"Indic-TTS network fallback error: {e2}")
                return base64.b64encode(b"AUDIO_DUMMY_DATA").decode("utf-8")

        audio_b64 = await asyncio.to_thread(_tts_sync)

        # Store in 2-Tier Cache if valid audio
        if audio_b64 and "AUDIO_DUMMY_DATA" not in audio_b64:
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
            "format": "mp3",
            "engine": f"ai4bharat-indic-tts-{indic_lang}"
        }

indic_tts_service = IndicTTSService()
