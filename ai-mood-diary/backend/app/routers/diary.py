import sys
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import Optional
from datetime import date
from ..database import get_db
from ..schemas.diary import (
    DiaryCreate, DiaryUpdate, DiaryResponse, DiaryListResponse,
    BatchDelete, BatchMoodUpdate, BatchExport,
)
from ..schemas.emotion import EmotionAnalysisResponse
from ..services import diary_service, ai_service
from ..models.emotion import EmotionAnalysis
from ..utils.jwt import verify_token

router = APIRouter(prefix="/api/diaries", tags=["日记"])


def run_ai_analysis(diary_id, user_id, content, title):
    log_path = r"e:\keshe\ai_analysis_log.txt"
    with open(log_path, "a", encoding="utf-8") as f:
        f.write(f"\n=== {diary_id} - 开始分析 ===\n")
        f.write(f"user_id: {user_id}\n")
        f.write(f"content: {content[:100]}...\n")
        f.write(f"title: {title}\n")
    try:
        ai_service.analyze_emotion(diary_id, user_id, content, title)
        with open(log_path, "a", encoding="utf-8") as f:
            f.write(f"=== {diary_id} - 分析完成 ===\n")
    except Exception as e:
        with open(log_path, "a", encoding="utf-8") as f:
            f.write(f"=== {diary_id} - 分析失败 ===\n")
            f.write(f"错误: {e}\n")
            import traceback
            f.write(traceback.format_exc())


@router.post("", response_model=DiaryResponse)
def create_diary(
    data: DiaryCreate,
    payload: dict = Depends(verify_token),
    db: Session = Depends(get_db),
):
    user_id = payload["user_id"]
    diary = diary_service.create_diary(db, user_id, data)
    run_ai_analysis(diary.id, user_id, diary.content, diary.title)
    return diary


@router.get("", response_model=DiaryListResponse)
def list_diaries(
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    mood_tag: Optional[str] = None,
    start_date: Optional[date] = None,
    end_date: Optional[date] = None,
    payload: dict = Depends(verify_token),
    db: Session = Depends(get_db),
):
    return diary_service.list_diaries(db, payload["user_id"], page, page_size, mood_tag, start_date, end_date)


@router.get("/{diary_id}", response_model=dict)
def get_diary(diary_id: int, payload: dict = Depends(verify_token), db: Session = Depends(get_db)):
    user_id = payload["user_id"]
    try:
        diary = diary_service.get_diary(db, diary_id, user_id)
        emotion = db.query(EmotionAnalysis).filter(EmotionAnalysis.diary_id == diary_id).first()
        return {
            "diary": DiaryResponse.model_validate(diary).model_dump(),
            "emotion": EmotionAnalysisResponse.model_validate(emotion).model_dump() if emotion else None,
        }
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.put("/{diary_id}", response_model=DiaryResponse)
def update_diary(diary_id: int, data: DiaryUpdate, payload: dict = Depends(verify_token), db: Session = Depends(get_db)):
    try:
        return diary_service.update_diary(db, diary_id, payload["user_id"], data)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.delete("/{diary_id}")
def delete_diary(diary_id: int, payload: dict = Depends(verify_token), db: Session = Depends(get_db)):
    try:
        diary_service.delete_diary(db, diary_id, payload["user_id"])
        return {"message": "删除成功"}
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))


@router.post("/batch-delete")
def batch_delete(data: BatchDelete, payload: dict = Depends(verify_token), db: Session = Depends(get_db)):
    diary_service.batch_delete(db, data.ids, payload["user_id"])
    return {"message": "批量删除成功"}


@router.post("/batch-mood")
def batch_update_mood(data: BatchMoodUpdate, payload: dict = Depends(verify_token), db: Session = Depends(get_db)):
    diary_service.batch_update_mood(db, data.ids, payload["user_id"], data.mood_tag)
    return {"message": "批量修改情绪标签成功"}


@router.post("/batch-export")
def batch_export(data: BatchExport, payload: dict = Depends(verify_token), db: Session = Depends(get_db)):
    result = diary_service.batch_export(db, data.ids, payload["user_id"], data.format)
    return {"data": result, "format": data.format}
