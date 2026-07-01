from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class EmotionAnalysisResponse(BaseModel):
    id: int
    diary_id: int
    emotion_label: Optional[str] = None
    emotion_score: Optional[float] = None
    analysis_detail: Optional[str] = None
    suggestion: Optional[str] = None
    model_used: Optional[str] = None
    prompt: Optional[str] = None
    raw_response: Optional[str] = None
    ai_text: Optional[str] = None
    created_at: Optional[datetime] = None

    class Config:
        from_attributes = True


class DiaryWithEmotionResponse(BaseModel):
    diary: dict
    emotion: Optional[EmotionAnalysisResponse] = None
