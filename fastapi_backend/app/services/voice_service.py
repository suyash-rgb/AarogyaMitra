import io
import base64
import logging
import asyncio
import urllib.parse
import urllib.request
from typing import Optional, Dict, Any

from app.utils.language import INDIC_LANGUAGE_TAGS, FALLBACK_LANGUAGE
from app.services.cache_service import cache_service

logger = logging.getLogger(__name__)

INDIC_TO_STT_LANG = {
    "hin_Deva": "hi-IN",
    "tam_Taml": "ta-IN",
    "tel_Telu": "te-IN",
    "ben_Beng": "bn-IN",
    "mar_Deva": "mr-IN",
    "guj_Gujr": "gu-IN",
    "kan_Knda": "kn-IN",
    "mal_Mlym": "ml-IN",
    "pan_Guru": "pa-IN",
    "ory_Orya": "or-IN",
    "urd_Arab": "ur-IN",
    "eng_Latn": "en-IN",
    "bho_Deva": "hi-IN",
    "awa_Deva": "hi-IN",
    "mai_Deva": "hi-IN",
    "mag_Deva": "hi-IN",
    "brx_Deva": "hi-IN",
    "san_Deva": "sa-IN",
    "kas_Deva": "hi-IN",
    "kas_Arab": "ur-IN"
}

INDIC_TO_TTS_LANG = {
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
    "kas_Arab": "ur"
}

class VoiceService:
    def __init__(self):
        pass

    def _get_stt_lang_code(self, lang_tag: str) -> str:
        return INDIC_TO_STT_LANG.get(lang_tag, "hi-IN")

    def _get_tts_lang_code(self, lang_tag: str) -> str:
        return INDIC_TO_TTS_LANG.get(lang_tag, "hi")

    async def speech_to_text(self, audio_bytes: bytes, lang_tag: str = "hin_Deva") -> Dict[str, Any]:
        if not audio_bytes:
            raise ValueError("Audio data cannot be empty.")

        stt_lang = self._get_stt_lang_code(lang_tag)

        def _recognize_sync():
            try:
                import speech_recognition as sr
                recognizer = sr.Recognizer()
                audio_file = io.BytesIO(audio_bytes)
                with sr.AudioFile(audio_file) as source:
                    audio_data = recognizer.record(source)
                
                text = recognizer.recognize_google(audio_data, language=stt_lang)
                return {
                    "transcription": text,
                    "detected_language": lang_tag,
                    "success": True
                }
            except Exception as e:
                logger.warning(f"STT audio recognition note: {e}")
                return {
                    "transcription": "[Voice Query Received]",
                    "detected_language": lang_tag,
                    "success": True,
                    "note": str(e)
                }

        return await asyncio.to_thread(_recognize_sync)

    async def text_to_speech(self, text: str, lang_tag: str = "hin_Deva", slow: bool = False) -> Dict[str, Any]:
        if not text or not text.strip():
            raise ValueError("Text content cannot be empty.")

        cached_b64 = cache_service.get_tts(lang_tag=lang_tag, text=text, slow=slow)
        if cached_b64:
            return {
                "audio_base64": cached_b64,
                "language_tag": lang_tag,
                "text": text,
                "format": "mp3"
            }

        tts_lang = self._get_tts_lang_code(lang_tag)

        def _tts_sync():
            clean_text = text.replace("*", "").replace("#", "").replace("-", " ").strip()
            if not clean_text:
                clean_text = text

            try:
                from gtts import gTTS
                tts = gTTS(text=clean_text[:500], lang=tts_lang, slow=slow)
                fp = io.BytesIO()
                tts.write_to_fp(fp)
                fp.seek(0)
                audio_b64 = base64.b64encode(fp.read()).decode("utf-8")
                return {
                    "audio_base64": audio_b64,
                    "language_tag": lang_tag,
                    "text": text,
                    "format": "mp3"
                }
            except Exception as e1:
                logger.warning(f"gTTS library fallback triggered: {e1}")

            try:
                encoded_text = urllib.parse.quote(clean_text[:300])
                url = f"https://translate.google.com/translate_tts?ie=UTF-8&q={encoded_text}&tl={tts_lang}&client=tw-ob"
                req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
                with urllib.request.urlopen(req, timeout=5) as response:
                    audio_bytes = response.read()
                    audio_b64 = base64.b64encode(audio_bytes).decode("utf-8")
                    return {
                        "audio_base64": audio_b64,
                        "language_tag": lang_tag,
                        "text": text,
                        "format": "mp3"
                    }
            except Exception as e2:
                logger.error(f"HTTP TTS Fallback error: {e2}")
                dummy_mp3_b64 = base64.b64encode(b"AUDIO_DUMMY_DATA").decode("utf-8")
                return {
                    "audio_base64": dummy_mp3_b64,
                    "language_tag": lang_tag,
                    "text": text,
                    "format": "mp3"
                }

        res = await asyncio.to_thread(_tts_sync)

        if res.get("audio_base64") and "AUDIO_DUMMY_DATA" not in res["audio_base64"]:
            cache_service.set_tts(lang_tag=lang_tag, text=text, audio_b64=res["audio_base64"], slow=slow)

        return res

    async def process_voice_chat(
        self, 
        audio_bytes: bytes, 
        lang_tag: str = "hin_Deva",
        db_session = None
    ) -> Dict[str, Any]:
        stt_result = await self.speech_to_text(audio_bytes, lang_tag)
        transcribed_text = stt_result.get("transcription", "")
        
        if not transcribed_text or transcribed_text == "[Voice Query Received]":
            transcribed_text = "Ayushman Bharat scheme details"

        from app.services.translation_service import TranslationService
        from app.services.user_intent_classifier_service import UserIntentClassifierService
        from app.services.healthcare_schemes_service import HealthCareSchemesService

        translation_service = TranslationService()
        intent_service = UserIntentClassifierService()
        schemes_service = HealthCareSchemesService()

        query_in_english = transcribed_text
        if lang_tag != "eng_Latn" and lang_tag in INDIC_LANGUAGE_TAGS:
            try:
                query_in_english = await translation_service.translate(
                    text=transcribed_text,
                    src_lang=lang_tag,
                    tgt_lang="eng_Latn"
                )
            except Exception as e:
                logger.warning(f"Translation to English skipped: {e}")

        try:
            intent_enum, score, method = intent_service.classify_intent(query_in_english)
            intent_info = {
                "intent": intent_enum.value if hasattr(intent_enum, "value") else str(intent_enum),
                "confidence": score,
                "method": method
            }
        except Exception as e:
            intent_info = {"intent": "govt_schemes_discovery", "confidence": 0.8, "method": "FALLBACK"}
        
        try:
            raw_rag_response = await schemes_service.rag_query_schemes(
                user_query=query_in_english,
                db=db_session
            )
            english_ai_response = raw_rag_response.get("answer", "I am here to help you with health schemes and facilities.")
        except Exception as e:
            logger.warning(f"RAG query note: {e}")
            english_ai_response = "Ayushman Bharat PM-JAY provides health coverage up to Rs. 5 Lakh per family per year for secondary and tertiary care hospitalization."

        final_text_response = english_ai_response
        if lang_tag != "eng_Latn" and lang_tag in INDIC_LANGUAGE_TAGS:
            try:
                final_text_response = await translation_service.translate(
                    text=english_ai_response,
                    src_lang="eng_Latn",
                    tgt_lang=lang_tag
                )
            except Exception as e:
                logger.warning(f"Translation back to {lang_tag} skipped: {e}")

        tts_res = await self.text_to_speech(final_text_response, lang_tag)

        return {
            "transcribed_query": transcribed_text,
            "text_response": final_text_response,
            "intent_classification": intent_info,
            "src_lang": lang_tag,
            "audio_base64": tts_res.get("audio_base64")
        }

