import os
import sys
from pathlib import Path

# Set HF Cache variables FIRST before any HuggingFace / Transformers imports
backend_dir = Path(__file__).resolve().parent.parent.parent
hf_dir = backend_dir / "models" / "huggingface"
models_dir = backend_dir / "models" / "ctranslate2_nllb_int8"

os.environ["HF_HOME"] = str(hf_dir)
os.environ["HF_HUB_CACHE"] = str(hf_dir / "hub")
os.environ["TRANSFORMERS_CACHE"] = str(hf_dir / "transformers")

import time
import hashlib
import asyncio
import logging
from typing import Optional

from app.utils.language import INDIC_LANGUAGE_TAGS, FALLBACK_LANGUAGE, detect_indic_language
from app.services.cache_service import cache_service
from app.services.transliteration_service import transliteration_service
from app.core.config import settings

logger = logging.getLogger(__name__)

class TranslationService:
    """
    High-Speed CTranslate2 NLLB-200 INT8 Translation Service (Indic <-> English).
    Replaces PyTorch FP32 CPU model with C++ INT8 quantized engine (~0.3s latency).
    Supports all 22 scheduled Indic languages + English.
    """

    def __init__(self, model_repo: str = "facebook/nllb-200-distilled-600M"):
        self.model_repo = model_repo
        self._translator = None
        self._tokenizer = None
        self._load_lock = asyncio.Lock()

    async def _load_models(self):
        """Lazily load CTranslate2 Translator and HuggingFace AutoTokenizer."""
        async with self._load_lock:
            if self._translator is not None and self._tokenizer is not None:
                return

            logger.info("Initializing CTranslate2 INT8 NLLB-200 Engine...")

            def _load_sync():
                import ctranslate2
                from transformers import AutoTokenizer

                if not (models_dir / "model.bin").exists():
                    logger.info(f"Converting {self.model_repo} to CTranslate2 INT8 model at {models_dir}...")
                    os.makedirs(models_dir, exist_ok=True)
                    converter = ctranslate2.converters.TransformersConverter(self.model_repo)
                    converter.convert(str(models_dir), quantization="int8", force=True)
                    logger.info("CTranslate2 INT8 Conversion Successful!")

                translator = ctranslate2.Translator(str(models_dir), device="cpu", compute_type="int8")
                tokenizer = AutoTokenizer.from_pretrained(self.model_repo)
                return translator, tokenizer

            self._translator, self._tokenizer = await asyncio.to_thread(_load_sync)
            logger.info("CTranslate2 NLLB Engine successfully loaded into memory!")

    async def translate(self, text: str, src_lang: str, tgt_lang: str) -> str:
        """Translates text between Indic languages and English with 2-Tier Caching & Hinglish Transliteration."""
        if not text or not text.strip():
            raise ValueError("Input text cannot be empty.")

        text_clean = text.strip()

        # Step 2: Handle Romanized Hinglish/Banglish Transliteration if required
        text_clean, src_lang = transliteration_service.transliterate_to_native(text_clean, src_lang)

        if src_lang == tgt_lang or (src_lang == "eng_Latn" and tgt_lang == "eng_Latn"):
            return text_clean

        # Validate language tags
        if src_lang not in INDIC_LANGUAGE_TAGS:
            src_lang = detect_indic_language(text_clean)

        if tgt_lang not in INDIC_LANGUAGE_TAGS:
            tgt_lang = FALLBACK_LANGUAGE

        # Check 2-Tier Cache HIT
        text_hash = hashlib.sha256(text_clean.encode("utf-8")).hexdigest()
        cache_key = f"{src_lang}:{tgt_lang}:{text_hash}"
        cached_translation = cache_service.get(namespace="trans", key=cache_key)

        if cached_translation is not None and isinstance(cached_translation, str):
            logger.info(f"Translation Cache HIT [{src_lang}->{tgt_lang}] for key: {cache_key[:20]}...")
            return cached_translation

        # Ensure CTranslate2 model is loaded
        if self._translator is None or self._tokenizer is None:
            await self._load_models()

        def _translate_sync():
            t0 = time.time()
            self._tokenizer.src_lang = src_lang
            tokens = self._tokenizer.convert_ids_to_tokens(self._tokenizer.encode(text_clean))
            results = self._translator.translate_batch([tokens], target_prefix=[[tgt_lang]])
            output_tokens = results[0].hypotheses[0][1:]
            translated = self._tokenizer.decode(self._tokenizer.convert_tokens_to_ids(output_tokens))
            t_dur = round(time.time() - t0, 3)
            logger.info(f"CTranslate2 NLLB Translated [{src_lang}->{tgt_lang}] in {t_dur}s")
            return translated

        translated_text = await asyncio.to_thread(_translate_sync)

        # Store in Cache
        cache_service.set(
            namespace="trans",
            key=cache_key,
            value=translated_text,
            ttl=settings.VALKEY_TRANS_TTL_SECONDS
        )

        return translated_text

translation_service = TranslationService()
