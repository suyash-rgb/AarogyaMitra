from pydantic import BaseModel, Field
from typing import Optional, Dict, Any

class STTResponse(BaseModel):
    transcription: str = Field(..., description='Transcribed text from speech input')
    detected_language: str = Field('hin_Deva', description='Detected or specified Indic language tag')
    confidence: Optional[float] = Field(None, description='Confidence score of ASR transcription')
    success: bool = True

class TTSRequest(BaseModel):
    text: str = Field(..., description='Text content to synthesize into speech')
    language_tag: str = Field('hin_Deva', description='Target Indic language tag (e.g., hin_Deva, tam_Taml, eng_Latn)')
    slow: bool = Field(False, description='Set to True for slower speaking pace')

class TTSResponse(BaseModel):
    audio_base64: str = Field(..., description='Base64 encoded MP3 audio binary')
    language_tag: str = Field(..., description='Indic language tag used for synthesis')
    text: str = Field(..., description='Original text synthesized')
    format: str = 'mp3'
    playback_url: Optional[str] = Field(None, description='URL to directly play the generated audio in browser')

class VoiceChatResponse(BaseModel):
    transcribed_query: str = Field(..., description='Transcribed text of user audio query')
    text_response: str = Field(..., description='Generated AI response text in target language')
    intent_classification: Optional[Dict[str, Any]] = Field(None, description='Detected user intent and routing metadata')
    src_lang: str = Field('hin_Deva', description='Original Indic language tag')
    audio_base64: Optional[str] = Field(None, description='Synthesized MP3 audio of the AI response in base64')
