from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from datetime import date, datetime, timedelta, timezone
from ..database import get_db
from ..services import ai_service
from ..models.emotion import EmotionAnalysis
from ..models.diary import Diary
from ..schemas.emotion import EmotionAnalysisResponse
from ..utils.jwt import verify_token

router = APIRouter(prefix="/api/ai", tags=["AI情绪分析"])


@router.get("/analysis/{diary_id}", response_model=EmotionAnalysisResponse)
def get_analysis(diary_id: int, payload: dict = Depends(verify_token), db: Session = Depends(get_db)):
    analysis = db.query(EmotionAnalysis).filter(
        EmotionAnalysis.diary_id == diary_id,
        EmotionAnalysis.user_id == payload["user_id"],
    ).first()
    if not analysis:
        raise HTTPException(status_code=404, detail="分析结果不存在或尚未完成")
    return analysis


@router.get("/today-analysis", response_model=dict)
def get_today_analysis(payload: dict = Depends(verify_token), db: Session = Depends(get_db)):
    today = date.today()
    today_str = str(today)
    
    diary = db.query(Diary).filter(
        Diary.user_id == payload["user_id"],
        Diary.date == today_str,
    ).order_by(Diary.id.desc()).first()
    
    if not diary:
        return {"message": "今日暂无日记", "analysis": None}
    
    analysis = db.query(EmotionAnalysis).filter(
        EmotionAnalysis.diary_id == diary.id,
        EmotionAnalysis.user_id == payload["user_id"],
    ).first()
    
    if not analysis:
        # 时间判断：日记创建超过60秒仍无分析 → 视为失败
        if diary.created_at and (datetime.now(timezone.utc) - diary.created_at.replace(tzinfo=timezone.utc)) > timedelta(seconds=60):
            return {"message": "AI暂不可用", "analysis": None, "ai_status": "unavailable"}
        return {"message": "AI分析正在生成中", "analysis": None, "ai_status": "pending"}
    
    if analysis.emotion_label == "unavailable":
        return {
            "message": "AI暂不可用",
            "analysis": EmotionAnalysisResponse.model_validate(analysis).model_dump(),
            "diary_title": diary.title,
            "ai_status": "unavailable",
        }
    
    return {
        "message": "success",
        "analysis": EmotionAnalysisResponse.model_validate(analysis).model_dump(),
        "diary_title": diary.title,
        "ai_status": "completed",
    }
