import sys
import types

# Ensure transformers.onnx dummy module compatibility
if 'transformers.onnx' not in sys.modules:
    dummy_onnx = types.ModuleType('transformers.onnx')
    dummy_onnx_utils = types.ModuleType('transformers.onnx.utils')
    dummy_onnx.OnnxConfig = object
    dummy_onnx.OnnxSeq2SeqConfigWithPast = object
    dummy_onnx_utils.compute_effective_axis_dimension = lambda *args, **kwargs: None
    dummy_onnx.utils = dummy_onnx_utils
    sys.modules['transformers.onnx'] = dummy_onnx
    sys.modules['transformers.onnx.utils'] = dummy_onnx_utils

import hashlib
import asyncio
import torch
import logging
from typing import Optional
from app.utils.language import INDIC_LANGUAGE_TAGS, FALLBACK_LANGUAGE, detect_indic_language
from app.services.cache_service import cache_service
from app.core.config import settings

logger = logging.getLogger(__name__)

class TranslationService:
    """
    Bidirectional IndicTrans2 Translation Service (Indic <-> English)
    Uses AI4Bharat IndicTrans2 architecture to handle 22 Indic Languages + English.
    """
    
    def __init__(
        self, 
        indic_en_model_name: str = "Raghavan/indictrans2-indic-en-dist-200M",
        en_indic_model_name: str = "Raghavan/indictrans2-en-indic-dist-200M"
    ):
        self.indic_en_model_name = indic_en_model_name
        self.en_indic_model_name = en_indic_model_name
        
        self._ip = None
        self._device = None
        
        self._indic_en_tokenizer = None
        self._indic_en_model = None
        
        self._en_indic_tokenizer = None
        self._en_indic_model = None
        
        self._load_lock = asyncio.Lock()

    async def _load_models(self):
        """Lazily load IndicProcessor and IndicTrans2 seq2seq models into device memory."""
        async with self._load_lock:
            if self._indic_en_model is not None and self._en_indic_model is not None:
                return
            
            logger.info("Loading IndicTrans2 Seq2Seq models (Indic <-> English)...")
            
            def _load_sync():
                from transformers import AutoModelForSeq2SeqLM, AlbertTokenizer
                from IndicTransToolkit import IndicProcessor
                
                ip = IndicProcessor(inference=True)
                device = "cuda" if torch.cuda.is_available() else "cpu"
                
                # Load Indic -> English Model
                logger.info(f"Loading Indic->En model ({self.indic_en_model_name})...")
                tok_in_en = AlbertTokenizer.from_pretrained(self.indic_en_model_name)
                mod_in_en = AutoModelForSeq2SeqLM.from_pretrained(self.indic_en_model_name, trust_remote_code=True)
                mod_in_en.config.vocab_size = mod_in_en.get_output_embeddings().weight.shape[0]
                mod_in_en.to(device)
                mod_in_en.eval()
                
                # Load English -> Indic Model
                logger.info(f"Loading En->Indic model ({self.en_indic_model_name})...")
                tok_en_in = AlbertTokenizer.from_pretrained(self.en_indic_model_name)
                mod_en_in = AutoModelForSeq2SeqLM.from_pretrained(self.en_indic_model_name, trust_remote_code=True)
                mod_en_in.config.vocab_size = mod_en_in.get_output_embeddings().weight.shape[0]
                mod_en_in.to(device)
                mod_en_in.eval()
                
                return ip, device, tok_in_en, mod_in_en, tok_en_in, mod_en_in
                
            (
                self._ip, 
                self._device, 
                self._indic_en_tokenizer, 
                self._indic_en_model, 
                self._en_indic_tokenizer, 
                self._en_indic_model
            ) = await asyncio.to_thread(_load_sync)
            
            logger.info(f"IndicTrans2 models successfully loaded on {self._device}!")

    async def translate(self, text: str, src_lang: str, tgt_lang: str) -> str:
        """Translates text between Indic languages and English with Valkey/In-Memory caching."""
        if not text or not text.strip():
            raise ValueError("Input text cannot be empty.")

        if src_lang == tgt_lang:
            return text.strip()

        # Validate language tags
        if src_lang not in INDIC_LANGUAGE_TAGS:
            src_lang = detect_indic_language(text)
            
        if tgt_lang not in INDIC_LANGUAGE_TAGS:
            tgt_lang = FALLBACK_LANGUAGE

        # Check 2-Tier Cache HIT
        text_hash = hashlib.sha256(text.strip().encode("utf-8")).hexdigest()
        cache_key = f"{src_lang}:{tgt_lang}:{text_hash}"
        cached_translation = cache_service.get(namespace="trans", key=cache_key)

        if cached_translation is not None and isinstance(cached_translation, str):
            logger.info(f"Translation Cache HIT [{src_lang}->{tgt_lang}] for key: {cache_key[:20]}...")
            return cached_translation

        # Ensure models are loaded
        if self._indic_en_model is None or self._en_indic_model is None:
            await self._load_models()

        def _translate_sync():
            # Determine translation direction
            if tgt_lang == "eng_Latn":
                tokenizer = self._indic_en_tokenizer
                model = self._indic_en_model
            else:
                tokenizer = self._en_indic_tokenizer
                model = self._en_indic_model
                
            batch = self._ip.preprocess_batch([text.strip()], src_lang=src_lang, tgt_lang=tgt_lang)
            inputs = tokenizer(batch, src_lang=src_lang, return_tensors="pt", padding=True)
            inputs = {k: v.to(self._device) for k, v in inputs.items()}
            inputs.pop("src_lang", None)
            
            with torch.inference_mode():
                outputs = model.generate(**inputs, num_beams=4, max_length=512, use_cache=False)
                
            outputs = tokenizer.batch_decode(outputs, skip_special_tokens=True)
            translations = self._ip.postprocess_batch(outputs, lang=tgt_lang)
            return translations[0]

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
