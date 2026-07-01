from sqlalchemy.orm import Session
from sqlalchemy import and_
from typing import Optional, List
from datetime import date
from ..models.diary import Diary
from ..models.emotion import EmotionAnalysis
from ..schemas.diary import DiaryCreate, DiaryUpdate


def create_diary(db: Session, user_id: int, data: DiaryCreate) -> Diary:
    diary = Diary(
        user_id=user_id,
        title=data.title,
        content=data.content,
        mood_tag=data.mood_tag,
        weather=data.weather,
        date=data.date,
    )
    db.add(diary)
    db.commit()
    db.refresh(diary)
    return diary


def get_diary(db: Session, diary_id: int, user_id: int) -> Diary:
    diary = db.query(Diary).filter(and_(Diary.id == diary_id, Diary.user_id == user_id)).first()
    if not diary:
        raise ValueError("日记不存在")
    return diary


def list_diaries(
    db: Session,
    user_id: int,
    page: int = 1,
    page_size: int = 20,
    mood_tag: Optional[str] = None,
    start_date: Optional[date] = None,
    end_date: Optional[date] = None,
) -> dict:
    query = db.query(Diary).filter(Diary.user_id == user_id)
    if mood_tag:
        query = query.filter(Diary.mood_tag == mood_tag)
    if start_date:
        query = query.filter(Diary.date >= start_date)
    if end_date:
        query = query.filter(Diary.date <= end_date)
    total = query.count()
    items = query.order_by(Diary.date.desc(), Diary.created_at.desc()).offset(
        (page - 1) * page_size
    ).limit(page_size).all()
    return {"total": total, "page": page, "page_size": page_size, "items": items}


def update_diary(db: Session, diary_id: int, user_id: int, data: DiaryUpdate) -> Diary:
    diary = get_diary(db, diary_id, user_id)
    if data.title is not None:
        diary.title = data.title
    if data.content is not None:
        diary.content = data.content
    if data.mood_tag is not None:
        diary.mood_tag = data.mood_tag
    if data.weather is not None:
        diary.weather = data.weather
    if data.date is not None:
        diary.date = data.date
    db.commit()
    db.refresh(diary)
    return diary


def delete_diary(db: Session, diary_id: int, user_id: int):
    diary = get_diary(db, diary_id, user_id)
    db.query(EmotionAnalysis).filter(EmotionAnalysis.diary_id == diary_id).delete()
    db.delete(diary)
    db.commit()


def batch_delete(db: Session, ids: List[int], user_id: int):
    db.query(EmotionAnalysis).filter(EmotionAnalysis.diary_id.in_(ids)).delete(synchronize_session=False)
    db.query(Diary).filter(and_(Diary.id.in_(ids), Diary.user_id == user_id)).delete(
        synchronize_session=False
    )
    db.commit()


def batch_update_mood(db: Session, ids: List[int], user_id: int, mood_tag: str):
    db.query(Diary).filter(and_(Diary.id.in_(ids), Diary.user_id == user_id)).update(
        {"mood_tag": mood_tag}, synchronize_session=False
    )
    db.commit()


def batch_export(db: Session, ids: List[int], user_id: int, fmt: str = "markdown"):
    diaries = (
        db.query(Diary)
        .filter(and_(Diary.id.in_(ids), Diary.user_id == user_id))
        .order_by(Diary.date.asc())
        .all()
    )
    if fmt == "json":
        return [
            {
                "id": d.id,
                "title": d.title,
                "content": d.content,
                "mood_tag": d.mood_tag,
                "weather": d.weather,
                "date": str(d.date),
                "created_at": str(d.created_at),
            }
            for d in diaries
        ]
    # markdown
    lines = []
    for d in diaries:
        lines.append(f"# {d.title or '无标题'}")
        lines.append(f"**日期：** {d.date}  **心情：** {d.mood_tag or '未标记'}")
        if d.weather:
            lines.append(f"**天气：** {d.weather}")
        lines.append("")
        lines.append(d.content or "")
        lines.append("\n---\n")
    return "\n".join(lines)
