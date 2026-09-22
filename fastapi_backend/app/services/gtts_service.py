import io
import base64
import hashlib
import asyncio
import logging
import urllib.parse
import urllib.request
from typing import Dict, Any, Optional

from app.services.cache_service import cache_service
from app.core.config import settings

logger = logging.getLogger(__name__)

INDIC_TO_GTTS_LANG = {
    "hin_Deva": "hi",
    "tam_Taml": "ta",
    "tel_Telu": "te",
    "ben_Beng": "bn",
    "mar_Deva": "mr",
    "guj_Gujr": "gu",
    "kan_Knda": "kn",
    "mal_Mlym": "ml",
    "pan_Guru": "pa",
    "ory_Orya": "or",
    "urd_Arab": "ur",
    "eng_Latn": "en",
    "bho_Deva": "hi",
    "awa_Deva": "hi",
    "mai_Deva": "hi",
    "mag_Deva": "hi",
    "brx_Deva": "hi",
    "san_Deva": "hi",
    "kas_Deva": "hi",
    "kas_Arab": "ur",
    "nep_Deva": "ne",
    "asm_Beng": "bn"
}

class GTTSService:
    def __init__(self):
        pass

    def get_gtts_lang_code(self, lang_tag: str) -> str:
        return INDIC_TO_GTTS_LANG.get(lang_tag, "hi")

    def is_language_supported(self, lang_tag: str) -> bool:
        return lang_tag in INDIC_TO_GTTS_LANG or lang_tag.split("_")[0][:2] in ["hi", "en", "bn", "ta", "te", "mr", "gu", "kn", "ml", "pa", "or", "ur", "ne"]

    async def text_to_speech(self, text: str, lang_tag: str = "hin_Deva", slow: bool = False) -> Dict[str, Any]:
        if not text or not text.strip():
            raise ValueError("Text content cannot be empty.")

        gtts_lang = self.get_gtts_lang_code(lang_tag)
        text_hash = hashlib.sha256(text.strip().encode("utf-8")).hexdigest()
        cache_key = f"{lang_tag}:{gtts_lang}:{text_hash}"

        cached_b64 = cache_service.get(namespace="gtts", key=cache_key)
        if cached_b64 and isinstance(cached_b64, str):
            logger.info(f"gTTS Cache HIT for key: {cache_key[:25]}...")
            return {
                "audio_base64": cached_b64,
                "language_tag": lang_tag,
                "text": text,
                "format": "mp3",
                "engine": f"gtts-{gtts_lang}",
                "cache_key": f"gtts:{cache_key}"
            }

        def _tts_sync():
            clean_text = text.replace("*", "").replace("#", "").replace("-", " ").strip()
            if not clean_text:
                clean_text = text

            try:
                from gtts import gTTS
                tts = gTTS(text=clean_text[:500], lang=gtts_lang, slow=slow)
                fp = io.BytesIO()
                tts.write_to_fp(fp)
                fp.seek(0)
                return base64.b64encode(fp.read()).decode("utf-8")
            except Exception as e1:
                logger.warning(f"gTTS library call failed: {e1}")

            try:
                encoded_text = urllib.parse.quote(clean_text[:300])
                url = f"https://translate.google.com/translate_tts?ie=UTF-8&q={encoded_text}&tl={gtts_lang}&client=tw-ob"
                req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
                with urllib.request.urlopen(req, timeout=5) as response:
                    audio_bytes = response.read()
                    return base64.b64encode(audio_bytes).decode("utf-8")
            except Exception as e2:
                logger.error(f"HTTP gTTS fallback error: {e2}")
                return None

        audio_b64 = await asyncio.to_thread(_tts_sync)

        if audio_b64:
            cache_service.set(
                namespace="gtts",
                key=cache_key,
                value=audio_b64,
                ttl=settings.VALKEY_TTS_TTL_SECONDS
            )
            return {
                "audio_base64": audio_b64,
                "language_tag": lang_tag,
                "text": text,
                "format": "mp3",
                "engine": f"gtts-{gtts_lang}",
                "cache_key": f"gtts:{cache_key}"
            }
        else:
            dummy_mp3_b64 = base64.b64encode(b"AUDIO_DUMMY_DATA").decode("utf-8")
            return {
                "audio_base64": dummy_mp3_b64,
                "language_tag": lang_tag,
                "text": text,
                "format": "mp3",
                "engine": "gtts-failed",
                "cache_key": None
            }

gtts_service = GTTSService()
