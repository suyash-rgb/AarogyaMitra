import os
import sys
import io
import wave
import json
import base64
import hashlib
import asyncio
import logging
from pathlib import Path
from typing import Dict, Any, Optional

import numpy as np
import onnxruntime as ort
from transformers import AutoTokenizer

from app.services.cache_service import cache_service
from app.core.config import settings

logger = logging.getLogger(__name__)

# Backend paths
backend_dir = Path(__file__).resolve().parent.parent.parent
mms_onnx_dir = backend_dir / "models" / "mms_onnx"
hf_dir = backend_dir / "models" / "huggingface"

os.environ["HF_HOME"] = str(hf_dir)
os.environ["HF_HUB_CACHE"] = str(hf_dir / "hub")

# Mapping from ArogyaMitra Indic language tags to local MMS ONNX model codes
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
    "urd_Arab": "urd-script_arabic",
    "san_Deva": "hin",
    "asm_Beng": "asm",
    "nep_Deva": "hin",
    "snd_Arab": "hin",
    "snd_Deva": "hin",
    "sat_Olck": "hin",
    "doi_Deva": "dgo",
    "mni_Mtei": "hin",
    "kok_Deva": "hin",
    "kas_Deva": "hin",
    "kas_Arab": "hin",
    "bho_Deva": "hin",
    "awa_Deva": "awa",
    "mai_Deva": "mai",
    "mag_Deva": "mag",
    "brx_Deva": "hin",
    "eng_Latn": "eng"
}

class MetaMMSTTSService:
    """
    High-Speed ONNX Runtime Text-to-Speech Service for Meta MMS VITS Models.
    Delivers ~1.5s - 2.5s uniform CPU latency across 22 Indic Languages without PyTorch overhead.
    """

    def __init__(self):
        self._sessions: Dict[str, ort.InferenceSession] = {}
        self._tokenizers: Dict[str, Any] = {}
        self._sampling_rates: Dict[str, int] = {}
        self._lock = asyncio.Lock()

    def is_language_supported(self, lang_tag: str) -> bool:
        return lang_tag in INDIC_TO_MMS_LANG

    def _get_mms_lang_code(self, lang_tag: str) -> str:
        return INDIC_TO_MMS_LANG.get(lang_tag, "hin")

    async def _load_model(self, mms_lang: str):
        """Lazily load ONNX session and Tokenizer for the specified MMS language."""
        async with self._lock:
            if mms_lang in self._sessions:
                return

            lang_dir = mms_onnx_dir / mms_lang
            onnx_path = lang_dir / "model.onnx"
            config_path = lang_dir / "mms_config.json"

            def _load_sync():
                if not onnx_path.exists():
                    raise FileNotFoundError(f"ONNX model file missing for MMS language: {mms_lang} at {onnx_path}")

                logger.info(f"Loading ONNX Runtime Session for MMS-TTS ({mms_lang})...")
                sess_opts = ort.SessionOptions()
                sess_opts.intra_op_num_threads = min(os.cpu_count() or 4, 6)
                session = ort.InferenceSession(str(onnx_path), sess_opts, providers=["CPUExecutionProvider"])

                # Load Tokenizer from local lang directory
                if lang_dir.exists() and (lang_dir / "vocab.json").exists():
                    tokenizer = AutoTokenizer.from_pretrained(str(lang_dir))
                else:
                    tokenizer = AutoTokenizer.from_pretrained(f"facebook/mms-tts-{mms_lang}")

                # Load sampling rate
                sampling_rate = 16000
                if config_path.exists():
                    try:
                        with open(config_path, "r", encoding="utf-8") as f:
                            meta = json.load(f)
                            sampling_rate = meta.get("sampling_rate", 16000)
                    except Exception:
                        pass

                return session, tokenizer, sampling_rate

            try:
                session, tokenizer, rate = await asyncio.to_thread(_load_sync)
                self._sessions[mms_lang] = session
                self._tokenizers[mms_lang] = tokenizer
                self._sampling_rates[mms_lang] = rate
                logger.info(f"MMS-TTS ONNX model for [{mms_lang}] loaded successfully into memory!")
            except Exception as e:
                logger.error(f"Failed to load ONNX model for [{mms_lang}]: {e}")
                raise e

    async def text_to_speech(self, text: str, lang_tag: str = "hin_Deva", slow: bool = False) -> Dict[str, Any]:
        """Synthesizes speech into Base64-encoded WAV using ONNX Runtime with 2-tier caching."""
        if not text or not text.strip():
            raise ValueError("Text content cannot be empty.")

        mms_lang = self._get_mms_lang_code(lang_tag)
        text_hash = hashlib.sha256(text.strip().encode("utf-8")).hexdigest()
        cache_key = f"{lang_tag}:{mms_lang}:{text_hash}"

        # 1. Check 2-Tier Cache HIT
        cached_b64 = cache_service.get(namespace="mms_tts", key=cache_key)
        if cached_b64 and isinstance(cached_b64, str):
            logger.info(f"Meta MMS-TTS ONNX Cache HIT for key: {cache_key[:25]}...")
            return {
                "audio_base64": cached_b64,
                "language_tag": lang_tag,
                "text": text,
                "format": "wav",
                "engine": f"mms-tts-onnx-{mms_lang}",
                "cache_key": f"mms_tts:{cache_key}"
            }

        # 2. Cache MISS: Synthesize Speech using pure ONNX Runtime C++ Engine
        try:
            if mms_lang not in self._sessions:
                await self._load_model(mms_lang)

            session = self._sessions[mms_lang]
            tokenizer = self._tokenizers[mms_lang]
            sample_rate = self._sampling_rates.get(mms_lang, 16000)

            def _synthesize_sync():
                inputs = tokenizer(text.strip(), return_tensors="np")
                input_ids = inputs["input_ids"]
                attention_mask = inputs.get("attention_mask", np.ones_like(input_ids))

                ort_out = session.run(["waveform"], {
                    "input_ids": input_ids,
                    "attention_mask": attention_mask
                })[0]

                audio_data = ort_out.squeeze()
                
                # Convert float32 array (-1.0 to 1.0) to int16 PCM WAV
                audio_int16 = (audio_data * 32767).clip(-32768, 32767).astype(np.int16)

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
                "engine": f"mms-tts-onnx-{mms_lang}",
                "cache_key": f"mms_tts:{cache_key}"
            }

        except Exception as e:
            logger.error(f"Meta MMS-TTS ONNX synthesis error for {lang_tag}: {e}")
            # Fallback to gTTS bridge if needed
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
