# app/services/cache_service.py
import json
import hashlib
import logging
from typing import Optional, Any
from cachetools import TTLCache
from app.core.config import settings

logger = logging.getLogger(__name__)

class CacheService:
    def __init__(self):
        # Fallback local memory cache (up to 5,000 items)
        self.memory_cache = TTLCache(maxsize=5000, ttl=86400)
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

    def _format_key(self, namespace: str, key: str) -> str:
        return f"{namespace}:{key}"

    def get(self, namespace: str, key: str) -> Optional[Any]:
        full_key = self._format_key(namespace, key)

        raw_val = None
        if self._valkey_client is not None:
            try:
                raw_val = self._valkey_client.get(full_key)
                if raw_val is not None:
                    logger.info(f"Cache HIT (Valkey) [{namespace}] key: {key[:30]}...")
            except Exception as e:
                logger.warning(f"Valkey GET error ({e}). Attempting memory cache fallback.")

        if raw_val is None:
            raw_val = self.memory_cache.get(full_key)
            if raw_val is not None:
                logger.info(f"Cache HIT (In-Memory) [{namespace}] key: {key[:30]}...")

        if raw_val is None:
            return None

        if isinstance(raw_val, str):
            try:
                return json.loads(raw_val)
            except (json.JSONDecodeError, TypeError):
                return raw_val

        return raw_val

    def set(self, namespace: str, key: str, value: Any, ttl: Optional[int] = None) -> None:
        if value is None:
            return

        full_key = self._format_key(namespace, key)
        effective_ttl = ttl or 86400

        if isinstance(value, (dict, list, bool, int, float)):
            serialized = json.dumps(value)
        else:
            serialized = str(value)

        self.memory_cache[full_key] = serialized

        if self._valkey_client is not None:
            try:
                self._valkey_client.setex(name=full_key, time=effective_ttl, value=serialized)
                logger.info(f"Cache SET (Valkey and Memory) [{namespace}] key: {key[:30]}...")
            except Exception as e:
                logger.warning(f"Valkey SET error ({e}).")
        else:
            logger.info(f"Cache SET (Memory) [{namespace}] key: {key[:30]}...")

    # Backward compatibility for TTS Voice Service
    def _generate_key(self, prefix: str, lang_tag: str, text: str, slow: bool) -> str:
        clean_text = text.replace("*", "").replace("#", "").replace("-", " ").strip()
        raw = f"{lang_tag}:{slow}:{clean_text}"
        hashed = hashlib.sha256(raw.encode("utf-8")).hexdigest()
        return hashed

    def get_tts(self, lang_tag: str, text: str, slow: bool = False) -> Optional[str]:
        key = self._generate_key("tts", lang_tag, text, slow)
        val = self.get("tts", key)
        return val if isinstance(val, str) else None

    def set_tts(self, lang_tag: str, text: str, audio_b64: str, slow: bool = False, ttl: Optional[int] = None) -> None:
        if not audio_b64:
            return
        key = self._generate_key("tts", lang_tag, text, slow)
        effective_ttl = ttl or settings.VALKEY_TTS_TTL_SECONDS
        self.set("tts", key, audio_b64, ttl=effective_ttl)

cache_service = CacheService()
