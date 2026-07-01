from sqlalchemy import Column, Integer, String, Text, Date, DateTime, ForeignKey, SmallInteger
from sqlalchemy.sql import func
from ..database import Base


class Diary(Base):
    __tablename__ = "diaries"

    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, comment="用户ID")
    title = Column(String(200), comment="标题")
    content = Column(Text, comment="正文")
    mood_tag = Column(String(20), comment="情绪标签")
    weather = Column(String(20), comment="天气")
    date = Column(Date, nullable=False, comment="日记日期")
    is_public = Column(SmallInteger, default=0, comment="是否公开")
    created_at = Column(DateTime, server_default=func.now(), comment="创建时间")
    updated_at = Column(DateTime, server_default=func.now(), onupdate=func.now(), comment="更新时间")
