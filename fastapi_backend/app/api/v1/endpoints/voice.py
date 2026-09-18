from fastapi import APIRouter, HTTPException, UploadFile, File, Form, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Optional

from app.schemas.voice import STTResponse, TTSRequest, TTSResponse, VoiceChatResponse
from app.services.voice_service import VoiceService
from app.db.session import get_session

router = APIRouter(
    prefix='/voice',
    tags=['Voice Processing and Replying']
)

voice_service = VoiceService()

@router.post('/stt', response_model=STTResponse)
async def speech_to_text_endpoint(
    file: UploadFile = File(...),
    lang_tag: str = Form('hin_Deva')
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
async def text_to_speech_endpoint(request: TTSRequest):
    try:
        res = await voice_service.text_to_speech(
            text=request.text, 
            lang_tag=request.language_tag, 
            slow=request.slow
        )
        return TTSResponse(**res)
    except ValueError as ve:
        raise HTTPException(status_code=400, detail=str(ve))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f'TTS processing failed: {str(e)}')

@router.post('/process-chat', response_model=VoiceChatResponse)
async def process_voice_chat_endpoint(
    file: UploadFile = File(...),
    lang_tag: str = Form('hin_Deva'),
    db: AsyncSession = Depends(get_session)
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
