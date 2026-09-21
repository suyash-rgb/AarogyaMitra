import hashlib
import asyncio
import torch
import logging
from app.utils.language import INDIC_LANGUAGE_TAGS, FALLBACK_LANGUAGE
from app.services.cache_service import cache_service
from app.core.config import settings

logger = logging.getLogger(__name__)

class TranslationService:
    
    def __init__(self, model_name="ai4bharat/indictrans2-en-indic-dist-200M"):
        self.model_name = model_name
        self._model = None
        self._tokenizer = None
        self._ip = None
        self._device = None
        self._load_lock = asyncio.Lock()

    async def _load_models(self):
        """Lazily load the tokenizer and model into memory in a background thread."""
        async with self._load_lock:
            if self._model is not None:
                return
            
            logger.info(f"Loading Translation Model ({self.model_name})... This may take a moment.")
            
            def _load_sync():
                from transformers import AutoModelForSeq2SeqLM, AutoTokenizer
                from IndicTransToolkit import IndicProcessor
                
                tokenizer = AutoTokenizer.from_pretrained(self.model_name, trust_remote_code=True)
                model = AutoModelForSeq2SeqLM.from_pretrained(self.model_name, trust_remote_code=True)
                ip = IndicProcessor(inference=True)
                
                device = "cuda" if torch.cuda.is_available() else "cpu"
                model.to(device)
                model.eval()
                
                return tokenizer, model, ip, device
                
            self._tokenizer, self._model, self._ip, self._device = await asyncio.to_thread(_load_sync)
            logger.info(f"Translation Model successfully loaded on {self._device}!")

    async def translate(self, text: str, src_lang: str, tgt_lang: str) -> str:
        """Translates a single string of text with 2-Tier Valkey + In-Memory caching."""
        
        if not text or not text.strip():
            raise ValueError("Input text cannot be empty.")
            
        if src_lang in INDIC_LANGUAGE_TAGS:
            if tgt_lang not in INDIC_LANGUAGE_TAGS:
                logger.warning(f"Unsupported target language tag: '{tgt_lang}'. Falling back to English.")
                tgt_lang = FALLBACK_LANGUAGE
        else:
            raise ValueError(f"Unsupported source language tag: '{src_lang}'")
            
        # Check 2-Tier Cache HIT
        text_hash = hashlib.sha256(text.strip().encode("utf-8")).hexdigest()
        cache_key = f"{src_lang}:{tgt_lang}:{text_hash}"
        cached_translation = cache_service.get(namespace="trans", key=cache_key)

        if cached_translation is not None and isinstance(cached_translation, str):
            logger.info(f"Translation Cache HIT [{src_lang}->{tgt_lang}] for key: {cache_key[:20]}...")
            return cached_translation

        # Cache MISS: Ensure the model is loaded before translating
        if self._model is None:
            await self._load_models()
            
        def _translate_sync():
            # 1. Preprocess
            batch = self._ip.preprocess_batch([text], src_lang=src_lang, tgt_lang=tgt_lang)
            inputs = self._tokenizer(batch, src_lang=src_lang, return_tensors="pt", padding=True)
            inputs = {k: v.to(self._device) for k, v in inputs.items()}
            
            inputs.pop("src_lang", None)
            
            # 2. Generate
            with torch.inference_mode():
                outputs = self._model.generate(**inputs, num_beams=5, max_length=256, use_cache=False)
                
            # 3. Postprocess
            outputs = self._tokenizer.batch_decode(outputs, skip_special_tokens=True)
            translations = self._ip.postprocess_batch(outputs, lang=tgt_lang)
            return translations[0]
            
        translated_text = await asyncio.to_thread(_translate_sync)

        # Store in 2-Tier Cache
        cache_service.set(
            namespace="trans",
            key=cache_key,
            value=translated_text,
            ttl=settings.VALKEY_TRANS_TTL_SECONDS
        )

        return translated_text

translation_service = TranslationService()
