from fastapi import APIRouter, HTTPException, UploadFile, File, Form, Depends, Query
from fastapi.responses import Response
import base64
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Optional

from app.schemas.voice import STTResponse, TTSRequest, TTSResponse, VoiceChatResponse
from app.services.voice_service import VoiceService
from app.services.meta_mms_tts_service import meta_mms_tts_service
from app.services.indic_tts_service import indic_tts_service
from app.services.gtts_service import gtts_service
from app.services.tts_load_balancer import tts_load_balancer
from app.db.session import get_session

router = APIRouter(
    prefix='/voice',
    tags=['Voice Processing and Replying']
)

voice_service = VoiceService()

@router.post('/stt', response_model=STTResponse)
async def speech_to_text_endpoint(
    file: UploadFile = File(...),
    lang_tag: str = Form('hin_Deva'),
    deviceId: str = Query(..., description="Device ID")
):
    try:
        audio_bytes = await file.read()
        res = await voice_service.speech_to_text(audio_bytes=audio_bytes, lang_tag=lang_tag)
        return STTResponse(**res)
    except ValueError as ve:
        raise HTTPException(status_code=400, detail=str(ve))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f'STT processing failed: {str(e)}')

@router.post('/tts', response_model=TTSResponse)
async def text_to_speech_endpoint(request: TTSRequest, deviceId: str = Query(..., description="Device ID")):
    """
    Load-balanced Text-to-Speech Endpoint.
    Uses custom Weighted Round-Robin (WRR) and Load-Aware balancer across:
    - Indic-TTS (Piper ONNX)
    - Meta MMS-TTS (VITS)
    - gTTS Service
    """
    try:
        res = await voice_service.text_to_speech(
            text=request.text, 
            lang_tag=request.language_tag, 
            slow=request.slow
        )
        if "cache_key" in res and res["cache_key"]:
            res["playback_url"] = f"/api/v1/voice/audio/{res['cache_key']}"
        return TTSResponse(**res)
    except ValueError as ve:
        raise HTTPException(status_code=400, detail=str(ve))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f'TTS processing failed: {str(e)}')

@router.get('/tts/lb-status')
async def tts_load_balancer_status():
    """Returns status metrics and active concurrent request counters for the TTS Load Balancer."""
    return tts_load_balancer.get_status()

@router.post('/tts/gtts', response_model=TTSResponse)
async def gtts_endpoint(request: TTSRequest, deviceId: str = Query(..., description="Device ID")):
    """Synthesizes audio specifically using standalone gTTS Service."""
    try:
        res = await gtts_service.text_to_speech(
            text=request.text,
            lang_tag=request.language_tag,
            slow=request.slow
        )
        if "cache_key" in res and res["cache_key"]:
            res["playback_url"] = f"/api/v1/voice/audio/{res['cache_key']}"
        return TTSResponse(**res)
    except ValueError as ve:
        raise HTTPException(status_code=400, detail=str(ve))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f'gTTS processing failed: {str(e)}')

@router.post('/tts/meta-mms', response_model=TTSResponse)
async def meta_mms_tts_endpoint(request: TTSRequest, deviceId: str = Query(..., description="Device ID")):
    """Synthesizes audio using Meta MMS-TTS (VITS Checkpoints) for evaluation across 22 Indic languages."""
    try:
        res = await meta_mms_tts_service.text_to_speech(
            text=request.text, 
            lang_tag=request.language_tag, 
            slow=request.slow
        )
        
        audio_b64 = res.get("audio_base64", "")
        if not audio_b64 or "AUDIO_DUMMY_DATA" in audio_b64:
            raise HTTPException(
                status_code=502, 
                detail="Meta MMS-TTS Engine failed to synthesize audio (returned empty or dummy data)."
            )
            
        if "cache_key" in res and res["cache_key"]:
            res["playback_url"] = f"/api/v1/voice/audio/{res['cache_key']}"
        else:
            raise HTTPException(
                status_code=500, 
                detail="Meta MMS-TTS Engine failed to return a valid cache_key; playback URL cannot be generated."
            )
            
        return TTSResponse(**res)
    except ValueError as ve:
        raise HTTPException(status_code=400, detail=str(ve))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f'Meta MMS-TTS processing failed: {str(e)}')

@router.post('/tts/indic-tts', response_model=TTSResponse)
async def indic_tts_endpoint(request: TTSRequest, deviceId: str = Query(..., description="Device ID")):
    """Synthesizes audio using AI4Bharat Indic-TTS for evaluation across supported Indian languages."""
    try:
        res = await indic_tts_service.text_to_speech(
            text=request.text, 
            lang_tag=request.language_tag, 
            slow=request.slow
        )
        
        audio_b64 = res.get("audio_base64", "")
        if not audio_b64 or "AUDIO_DUMMY_DATA" in audio_b64:
            raise HTTPException(
                status_code=502, 
                detail="Indic-TTS Engine failed to synthesize audio (returned empty or dummy data)."
            )
            
        if "cache_key" in res and res["cache_key"]:
            res["playback_url"] = f"/api/v1/voice/audio/{res['cache_key']}"
        else:
            raise HTTPException(
                status_code=500, 
                detail="Indic-TTS Engine failed to return a valid cache_key; playback URL cannot be generated."
            )
            
        return TTSResponse(**res)
    except ValueError as ve:
        raise HTTPException(status_code=400, detail=str(ve))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f'Indic-TTS processing failed: {str(e)}')

@router.post('/process-chat', response_model=VoiceChatResponse)
async def process_voice_chat_endpoint(
    file: UploadFile = File(...),
    lang_tag: str = Form('hin_Deva'),
    db: AsyncSession = Depends(get_session),
    deviceId: str = Query(..., description="Device ID")
):
    try:
        audio_bytes = await file.read()
        res = await voice_service.process_voice_chat(
            audio_bytes=audio_bytes,
            lang_tag=lang_tag,
            db_session=db
        )
        return VoiceChatResponse(**res)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f'Voice chat pipeline failed: {str(e)}')

@router.get('/audio/{cache_key}')
async def get_audio_playback(cache_key: str):
    """Stream the decoded audio directly to the browser for playback."""
    from app.services.cache_service import cache_service
    
    parts = cache_key.split(":", 1)
    if len(parts) != 2:
        raise HTTPException(status_code=400, detail="Invalid cache key format")
    namespace, key = parts[0], parts[1]
    
    # Look up in cache
    cached_b64 = cache_service.get(namespace=namespace, key=key)
    if not cached_b64:
        raise HTTPException(status_code=404, detail="Audio not found or expired")
    
    try:
        audio_bytes = base64.b64decode(cached_b64)
        media_type = "audio/mp3" if namespace == "gtts" else "audio/wav"
        return Response(content=audio_bytes, media_type=media_type)
    except Exception as e:
        raise HTTPException(status_code=500, detail="Failed to decode audio")
