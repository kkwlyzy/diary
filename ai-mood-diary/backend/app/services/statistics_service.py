from sqlalchemy.orm import Session
from sqlalchemy import func
from datetime import date
from ..models.diary import Diary
from ..models.emotion import EmotionAnalysis


def get_calendar_data(db: Session, user_id: int, year: int, month: int):
    """获取某月日历数据：有日记的日期及其情绪标签"""
    start = date(year, month, 1)
    if month == 12:
        end = date(year + 1, 1, 1)
    else:
        end = date(year, month + 1, 1)

    results = (
        db.query(Diary.date, Diary.mood_tag, func.count(Diary.id).label("count"))
        .filter(
            Diary.user_id == user_id,
            Diary.date >= start,
            Diary.date < end,
        )
        .group_by(Diary.date, Diary.mood_tag)
        .all()
    )
    return [{"date": str(r.date), "mood_tag": r.mood_tag, "count": r.count} for r in results]


def get_mood_trend(db: Session, user_id: int, start_date: date, end_date: date):
    """获取心情趋势数据"""
    results = (
        db.query(Diary.date, Diary.mood_tag, func.count(Diary.id).label("count"))
        .filter(
            Diary.user_id == user_id,
            Diary.date >= start_date,
            Diary.date <= end_date,
            Diary.mood_tag.isnot(None),
        )
        .group_by(Diary.date, Diary.mood_tag)
        .order_by(Diary.date.asc())
        .all()
    )
    return [{"date": str(r.date), "mood_tag": r.mood_tag, "count": r.count} for r in results]


def get_mood_distribution(db: Session, user_id: int, start_date: date, end_date: date):
    """获取情绪标签分布"""
    results = (
        db.query(Diary.mood_tag, func.count(Diary.id).label("count"))
        .filter(
            Diary.user_id == user_id,
            Diary.date >= start_date,
            Diary.date <= end_date,
            Diary.mood_tag.isnot(None),
        )
        .group_by(Diary.mood_tag)
        .all()
    )
    return [{"mood_tag": r.mood_tag, "count": r.count} for r in results]


def get_summary(db: Session, user_id: int, start_date: date, end_date: date):
    """获取时间段汇总统计"""
    total = (
        db.query(func.count(Diary.id))
        .filter(Diary.user_id == user_id, Diary.date >= start_date, Diary.date <= end_date)
        .scalar()
    )
    return {"total_diaries": total, "start_date": str(start_date), "end_date": str(end_date)}
