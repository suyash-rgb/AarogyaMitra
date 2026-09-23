import re
import logging

logger = logging.getLogger(__name__)

INDIC_LANGUAGE_TAGS = {
    'asm_Beng', 'awa_Deva', 'ben_Beng', 'bho_Deva', 'brx_Deva', 'doi_Deva',
    'eng_Latn', 'gom_Deva', 'gon_Deva', 'guj_Gujr', 'hin_Deva', 'hne_Deva',
    'kan_Knda', 'kas_Arab', 'kas_Deva', 'kha_Latn', 'lus_Latn', 'mag_Deva',
    'mai_Deva', 'mal_Mlym', 'mar_Deva', 'mni_Beng', 'mni_Mtei', 'npi_Deva',
    'ory_Orya', 'pan_Guru', 'san_Deva', 'sat_Olck', 'snd_Arab', 'snd_Deva',
    'tam_Taml', 'tel_Telu', 'urd_Arab', 'unr_Deva'
}

FALLBACK_LANGUAGE = 'eng_Latn'

SCRIPT_MAP = [
    (re.compile(r'[ऀ-ॿ]'), 'hin_Deva'),  # Devanagari (Hindi, Marathi, Sanskrit, etc.)
    (re.compile(r'[ঀ-৿]'), 'ben_Beng'),  # Bengali / Assamese
    (re.compile(r'[஀-௿]'), 'tam_Taml'),  # Tamil
    (re.compile(r'[ఀ-౿]'), 'tel_Telu'),  # Telugu
    (re.compile(r'[ಀ-೿]'), 'kan_Knda'),  # Kannada
    (re.compile(r'[ഀ-ൿ]'), 'mal_Mlym'),  # Malayalam
    (re.compile(r'[઀-૿]'), 'guj_Gujr'),  # Gujarati
    (re.compile(r'[਀-੿]'), 'pan_Guru'),  # Gurmukhi / Punjabi
    (re.compile(r'[଀-୿]'), 'ory_Orya'),  # Odia
    (re.compile(r'[؀-ۿݐ-ݿ]'), 'urd_Arab'), # Perso-Arabic / Urdu
    (re.compile(r'[᱐-᱿]'), 'sat_Olck'),  # Ol Chiki / Santali
    (re.compile(r'[ꯀ-꯿]'), 'mni_Mtei'),  # Meitei / Manipuri
]

def detect_indic_language(text: str, fallback: str = FALLBACK_LANGUAGE) -> str:
    """
    IndicLID (Language Identification) module.
    Detects Indic scripts using unicode character range matching, returning standard FLORES-200 language tags.
    Defaults to eng_Latn for Latin script or fallback.
    """
    if not text or not text.strip():
        return fallback

    counts = {}
    for pattern, tag in SCRIPT_MAP:
        matches = len(pattern.findall(text))
        if matches > 0:
            counts[tag] = matches

    if counts:
        best_tag = max(counts, key=counts.get)
        logger.info(f"IndicLID detected language '{best_tag}' for query snippet: '{text[:30]}...'")
        return best_tag

    return fallback
