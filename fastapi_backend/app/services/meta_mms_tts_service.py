import io
import wave
import base64
import hashlib
import asyncio
import logging
import torch
import numpy as np
from typing import Dict, Any, Optional

from app.services.cache_service import cache_service
from app.core.config import settings

logger = logging.getLogger(__name__)

# Mapping from ArogyaMitra 22 Indic language tags to Meta MMS-TTS language codes
INDIC_TO_MMS_LANG = {
    "hin_Deva": "hin",
    "mar_Deva": "mar",
    "tam_Taml": "tam",
    "tel_Telu": "tel",
    "ben_Beng": "ben",
    "guj_Gujr": "guj",
    "kan_Knda": "kan",
    "mal_Mlym": "mal",
    "pan_Guru": "pan",
    "ory_Orya": "ory",
    "urd_Arab": "urd",
    "san_Deva": "san",
    "asm_Beng": "asm",
    "nep_Deva": "nep",
    "snd_Arab": "snd",
    "snd_Deva": "snd",
    "sat_Olck": "sat",
    "doi_Deva": "doi",
    "mni_Mtei": "mni",
    "kok_Deva": "kok",
    "kas_Deva": "kas",
    "kas_Arab": "kas",
    "bho_Deva": "hin",
    "awa_Deva": "hin",
    "mai_Deva": "hin",
    "mag_Deva": "hin",
    "brx_Deva": "hin",
    "eng_Latn": "eng"
}

class MetaMMSTTSService:
    def __init__(self):
        self._models = {}
        self._tokenizers = {}
        self._lock = asyncio.Lock()

    def _get_mms_lang_code(self, lang_tag: str) -> str:
        return INDIC_TO_MMS_LANG.get(lang_tag, "hin")

    async def _load_model(self, mms_lang: str):
        async with self._lock:
            if mms_lang in self._models:
                return

            model_id = f"facebook/mms-tts-{mms_lang}"
            logger.info(f"Loading Meta MMS-TTS Model ({model_id})...")

            def _load_sync():
                from transformers import VitsModel, AutoTokenizer
                tokenizer = AutoTokenizer.from_pretrained(model_id)
                model = VitsModel.from_pretrained(model_id)
                device = "cuda" if torch.cuda.is_available() else "cpu"
                model.to(device)
                model.eval()
                return tokenizer, model

            try:
                tokenizer, model = await asyncio.to_thread(_load_sync)
                self._tokenizers[mms_lang] = tokenizer
                self._models[mms_lang] = model
                logger.info(f"Meta MMS-TTS Model ({model_id}) loaded successfully!")
            except Exception as e:
                logger.error(f"Failed to load Meta MMS-TTS model ({model_id}): {e}")
                raise e

    async def text_to_speech(self, text: str, lang_tag: str = "hin_Deva", slow: bool = False) -> Dict[str, Any]:
        if not text or not text.strip():
            raise ValueError("Text content cannot be empty.")

        mms_lang = self._get_mms_lang_code(lang_tag)
        text_hash = hashlib.sha256(text.strip().encode("utf-8")).hexdigest()
        cache_key = f"{lang_tag}:{mms_lang}:{text_hash}"

        # 2-Tier Cache Check
        cached_b64 = cache_service.get(namespace="mms_tts", key=cache_key)
        if cached_b64 and isinstance(cached_b64, str):
            logger.info(f"Meta MMS-TTS Cache HIT for key: {cache_key[:25]}...")
            return {
                "audio_base64": cached_b64,
                "language_tag": lang_tag,
                "text": text,
                "format": "wav",
                "engine": f"facebook/mms-tts-{mms_lang}",
                "cache_key": f"mms_tts:{cache_key}"
            }

        # Cache MISS: Synthesize Speech using VITS
        try:
            await self._load_model(mms_lang)
            tokenizer = self._tokenizers[mms_lang]
            model = self._models[mms_lang]

            def _synthesize_sync():
                inputs = tokenizer(text, return_tensors="pt")
                device = next(model.parameters()).device
                inputs = {k: v.to(device) for k, v in inputs.items()}

                with torch.no_grad():
                    output = model(**inputs).waveform

                audio_data = output.squeeze().cpu().numpy()
                sample_rate = model.config.sampling_rate

                # Convert float32 array (-1.0 to 1.0) to int16 PCM WAV
                audio_int16 = (audio_data * 32767).astype(np.int16)
                
                buffer = io.BytesIO()
                with wave.open(buffer, "wb") as wav_file:
                    wav_file.setnchannels(1)  # Mono
                    wav_file.setsampwidth(2)  # 16-bit PCM
                    wav_file.setframerate(sample_rate)
                    wav_file.writeframes(audio_int16.tobytes())

                buffer.seek(0)
                return base64.b64encode(buffer.read()).decode("utf-8")

            audio_b64 = await asyncio.to_thread(_synthesize_sync)

            # Store in 2-Tier Cache
            cache_service.set(
                namespace="mms_tts",
                key=cache_key,
                value=audio_b64,
                ttl=settings.VALKEY_TTS_TTL_SECONDS
            )

            return {
                "audio_base64": audio_b64,
                "language_tag": lang_tag,
                "text": text,
                "format": "wav",
                "engine": f"facebook/mms-tts-{mms_lang}",
                "cache_key": f"mms_tts:{cache_key}"
            }
        except Exception as e:
            logger.error(f"Meta MMS-TTS synthesis error for {lang_tag}: {e}")
            # Fallback to gTTS bridge if HuggingFace checkpoint is downloading or fails
            from gtts import gTTS
            def _gtts_fallback():
                tts_lang = lang_tag.split("_")[0][:2]
                tts = gTTS(text=text[:300], lang=tts_lang, slow=slow)
                fp = io.BytesIO()
                tts.write_to_fp(fp)
                fp.seek(0)
                return base64.b64encode(fp.read()).decode("utf-8")

            fallback_b64 = await asyncio.to_thread(_gtts_fallback)
            cache_service.set(
                namespace="mms_tts",
                key=cache_key,
                value=fallback_b64,
                ttl=settings.VALKEY_TTS_TTL_SECONDS
            )
            return {
                "audio_base64": fallback_b64,
                "language_tag": lang_tag,
                "text": text,
                "format": "mp3",
                "engine": f"gtts_fallback_{mms_lang}",
                "cache_key": f"mms_tts:{cache_key}"
            }

meta_mms_tts_service = MetaMMSTTSService()
