from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import date, datetime


class DiaryCreate(BaseModel):
    title: Optional[str] = None
    content: Optional[str] = None
    mood_tag: Optional[str] = None
    weather: Optional[str] = None
    date: date


class DiaryUpdate(BaseModel):
    title: Optional[str] = None
    content: Optional[str] = None
    mood_tag: Optional[str] = None
    weather: Optional[str] = None
    date: Optional[date] = None


class DiaryResponse(BaseModel):
    id: int
    user_id: int
    title: Optional[str] = None
    content: Optional[str] = None
    mood_tag: Optional[str] = None
    weather: Optional[str] = None
    date: date
    is_public: int
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True


class DiaryListResponse(BaseModel):
    total: int
    page: int
    page_size: int
    items: List[DiaryResponse]


class BatchDelete(BaseModel):
    ids: List[int]


class BatchMoodUpdate(BaseModel):
    ids: List[int]
    mood_tag: str


class BatchExport(BaseModel):
    ids: List[int]
    format: str = "markdown"  # markdown or json
