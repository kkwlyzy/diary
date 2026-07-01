from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey, Numeric
from sqlalchemy.sql import func
from ..database import Base


class EmotionAnalysis(Base):
    __tablename__ = "emotion_analyses"

    id = Column(Integer, primary_key=True, autoincrement=True)
    diary_id = Column(Integer, ForeignKey("diaries.id"), nullable=False, comment="关联日记ID")
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, comment="用户ID")
    emotion_label = Column(String(20), comment="AI识别的主要情绪")
    emotion_score = Column(Numeric(3, 2), comment="情绪强度0.00~1.00")
    analysis_detail = Column(Text, comment="详细分析文本")
    suggestion = Column(Text, comment="AI建议")
    model_used = Column(String(50), comment="使用的模型名称")
    prompt = Column(Text, comment="发送给AI的完整提示")
    raw_response = Column(Text, comment="AI的原始响应JSON")
    ai_text = Column(Text, comment="AI返回的文本内容")
    created_at = Column(DateTime, server_default=func.now(), comment="分析时间")
