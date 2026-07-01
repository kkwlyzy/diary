from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from datetime import date
from ..database import get_db
from ..services import statistics_service
from ..utils.jwt import verify_token

router = APIRouter(prefix="/api/statistics", tags=["统计"])


@router.get("/calendar")
def get_calendar(
    year: int = Query(...),
    month: int = Query(..., ge=1, le=12),
    payload: dict = Depends(verify_token),
    db: Session = Depends(get_db),
):
    return statistics_service.get_calendar_data(db, payload["user_id"], year, month)


@router.get("/mood-trend")
def get_mood_trend(
    start_date: date = Query(...),
    end_date: date = Query(...),
    payload: dict = Depends(verify_token),
    db: Session = Depends(get_db),
):
    return statistics_service.get_mood_trend(db, payload["user_id"], start_date, end_date)


@router.get("/mood-distribution")
def get_mood_distribution(
    start_date: date = Query(...),
    end_date: date = Query(...),
    payload: dict = Depends(verify_token),
    db: Session = Depends(get_db),
):
    return statistics_service.get_mood_distribution(db, payload["user_id"], start_date, end_date)


@router.get("/summary")
def get_summary(
    start_date: date = Query(...),
    end_date: date = Query(...),
    payload: dict = Depends(verify_token),
    db: Session = Depends(get_db),
):
    return statistics_service.get_summary(db, payload["user_id"], start_date, end_date)
