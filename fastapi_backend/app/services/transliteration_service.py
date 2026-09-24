import logging
from typing import Optional
from indic_transliteration import sanscript
from indic_transliteration.sanscript import transliterate

logger = logging.getLogger(__name__)

# Map of IndicLID / NLLB script codes to sanscript scheme constants
SCRIPT_SCHEME_MAP = {
    "hin_Deva": sanscript.DEVANAGARI,
    "mar_Deva": sanscript.DEVANAGARI,
    "san_Deva": sanscript.DEVANAGARI,
    "doi_Deva": sanscript.DEVANAGARI,
    "mai_Deva": sanscript.DEVANAGARI,
    "brx_Deva": sanscript.DEVANAGARI,
    "npi_Deva": sanscript.DEVANAGARI,
    "ben_Beng": sanscript.BENGALI,
    "asm_Beng": sanscript.BENGALI,
    "mni_Beng": sanscript.BENGALI,
    "guj_Gujr": sanscript.GUJARATI,
    "tam_Taml": sanscript.TAMIL,
    "tel_Telu": sanscript.TELUGU,
    "kan_Knda": sanscript.KANNADA,
    "mal_Mlym": sanscript.MALAYALAM,
    "pan_Guru": sanscript.GURMUKHI,
    "ory_Orya": sanscript.ORIYA,
}

class TransliterationService:
    """
    Lightweight 3ms Transliteration Service (Romanized Latin -> Native Orthographic Indic Script).
    Solves Hinglish, Banglish, and Manglish inputs using indic-transliteration (Sanscript).
    """

    @staticmethod
    def transliterate_to_native(text: str, detected_lang: str) -> tuple[str, str]:
        """
        If detected_lang is Romanized (e.g., 'hin_Latn', 'mar_Latn', 'ben_Latn'),
        transliterates Romanized text to Native Orthographic Script ('hin_Deva', etc.).
        Returns (transliterated_text, native_lang_code).
        """
        if not text or not text.strip():
            return text, detected_lang

        # If not Latin script or is pure English, return as-is
        if not detected_lang.endswith("_Latn") or detected_lang == "eng_Latn":
            return text, detected_lang

        # Infer native language tag (e.g., 'hin_Latn' -> 'hin_Deva', 'ben_Latn' -> 'ben_Beng')
        lang_prefix = detected_lang.split("_")[0]
        
        # Default native script mappings
        native_lang_map = {
            "hin": "hin_Deva",
            "mar": "mar_Deva",
            "ben": "ben_Beng",
            "guj": "guj_Gujr",
            "tam": "tam_Taml",
            "tel": "tel_Telu",
            "kan": "kan_Knda",
            "mal": "mal_Mlym",
            "pan": "pan_Guru",
            "ory": "ory_Orya",
            "asm": "asm_Beng",
            "san": "san_Deva",
            "mai": "mai_Deva",
            "doi": "doi_Deva",
            "npi": "npi_Deva",
            "urd": "urd_Arab",
        }

        target_native_lang = native_lang_map.get(lang_prefix, "hin_Deva")
        target_scheme = SCRIPT_SCHEME_MAP.get(target_native_lang, sanscript.DEVANAGARI)

        try:
            native_text = transliterate(text.strip(), sanscript.ITRANS, target_scheme)
            logger.info(f"Transliterated [{detected_lang} -> {target_native_lang}]: '{text}' -> '{native_text}'")
            return native_text, target_native_lang
        except Exception as e:
            logger.warning(f"Transliteration failed for {detected_lang}, falling back to original: {e}")
            return text, target_native_lang

transliteration_service = TransliterationService()
