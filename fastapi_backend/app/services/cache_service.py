# app/services/cache_service.py
import hashlib
import logging
from typing import Optional
from cachetools import TTLCache
from app.core.config import settings

logger = logging.getLogger(__name__)

class CacheService:
    def __init__(self):
        # Fallback local memory cache (up to 1,000 items, TTL from settings)
        self.memory_cache = TTLCache(maxsize=1000, ttl=settings.VALKEY_TTS_TTL_SECONDS)
        self._valkey_client = None
        self._init_valkey()

    def _init_valkey(self):
        try:
            import valkey
            self._valkey_client = valkey.Valkey(
                host=settings.VALKEY_HOST,
                port=settings.VALKEY_PORT,
                db=settings.VALKEY_DB,
                decode_responses=True,
                socket_timeout=2.0,
                socket_connect_timeout=2.0
            )
            self._valkey_client.ping()
            logger.info("Valkey cache client initialized successfully.")
        except Exception as e:
            logger.warning(f"Valkey initialization note ({e}). Using in-memory TTLCache fallback.")
            self._valkey_client = None

    def _generate_key(self, prefix: str, lang_tag: str, text: str, slow: bool) -> str:
        clean_text = text.replace("*", "").replace("#", "").replace("-", " ").strip()
        raw = f"{lang_tag}:{slow}:{clean_text}"
        hashed = hashlib.sha256(raw.encode("utf-8")).hexdigest()
        return f"{prefix}:{hashed}"

    def get_tts(self, lang_tag: str, text: str, slow: bool = False) -> Optional[str]:
        cache_key = self._generate_key("tts", lang_tag, text, slow)

        if self._valkey_client is not None:
            try:
                cached_b64 = self._valkey_client.get(cache_key)
                if cached_b64:
                    logger.info(f"TTS Cache HIT (Valkey) for key: {cache_key[:20]}...")
                    return cached_b64
            except Exception as e:
                logger.warning(f"Valkey GET error ({e}). Attempting memory cache fallback.")

        cached_b64 = self.memory_cache.get(cache_key)
        if cached_b64:
            logger.info(f"TTS Cache HIT (In-Memory) for key: {cache_key[:20]}...")
            return cached_b64

        logger.info(f"TTS Cache MISS for key: {cache_key[:20]}...")
        return None

    def set_tts(self, lang_tag: str, text: str, audio_b64: str, slow: bool = False, ttl: Optional[int] = None) -> None:
        if not audio_b64:
            return

        cache_key = self._generate_key("tts", lang_tag, text, slow)
        effective_ttl = ttl or settings.VALKEY_TTS_TTL_SECONDS

        self.memory_cache[cache_key] = audio_b64

        if self._valkey_client is not None:
            try:
                self._valkey_client.setex(name=cache_key, time=effective_ttl, value=audio_b64)
                logger.info(f"TTS Cache SET (Valkey & Memory) for key: {cache_key[:20]}...")
            except Exception as e:
                logger.warning(f"Valkey SET error ({e}).")
        else:
            logger.info(f"TTS Cache SET (Memory) for key: {cache_key[:20]}...")

cache_service = CacheService()

