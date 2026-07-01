import json
import requests
import logging
from sqlalchemy.orm import Session
from ..config import ARK_API_KEY, ARK_API_BASE, ARK_MODEL
from ..models.emotion import EmotionAnalysis
from ..models.user import User
from ..models.diary import Diary
from ..database import SessionLocal, Base, engine

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def analyze_emotion(diary_id: int, user_id: int, content: str, title: str = ""):
    log_path = r"e:\keshe\ai_analysis_log.txt"
    
    with open(log_path, "a", encoding="utf-8") as f:
        f.write(f"  [ai_service] ARK_API_KEY: {ARK_API_KEY[:20]}...\n")
        f.write(f"  [ai_service] ARK_API_BASE: {ARK_API_BASE}\n")
        f.write(f"  [ai_service] ARK_MODEL: {ARK_MODEL}\n")

    prompt = f"""你是一个温柔的心理咨询师。请分析以下日记内容的情绪倾向，以JSON格式返回。

日记标题：{title}
日记内容：{content}

请从以下情绪标签中选择最匹配的一个：happy（快乐）, sad（悲伤）, anxious（焦虑）, calm（平静）, angry（愤怒）, surprised（惊讶）

返回格式（只返回JSON，不要其他文字）：
{{
    "emotion_label": "情绪标签",
    "emotion_score": 0.00-1.00之间的情绪强度分数,
    "analysis_detail": "50字以内的情绪分析",
    "suggestion": "50字以内的温暖建议"
}}"""

    headers = {
        "Authorization": f"Bearer {ARK_API_KEY}",
        "Content-Type": "application/json",
        "anthropic-version": "2023-06-01",
    }
    payload = {
        "model": ARK_MODEL,
        "max_tokens": 1000,
        "messages": [{"role": "user", "content": prompt}],
    }

    db = None
    try:
        with open(log_path, "a", encoding="utf-8") as f:
            f.write(f"  [ai_service] 创建数据库会话...\n")
        db = SessionLocal()
        with open(log_path, "a", encoding="utf-8") as f:
            f.write(f"  [ai_service] 数据库会话创建成功\n")
            f.write(f"  [ai_service] 开始调用API...\n")
        
        resp = requests.post(
            f"{ARK_API_BASE}/v1/messages",
            headers=headers,
            json=payload,
            timeout=30,
        )
        
        with open(log_path, "a", encoding="utf-8") as f:
            f.write(f"  [ai_service] API响应状态: {resp.status_code}\n")
        
        resp.raise_for_status()
        result = resp.json()
        
        with open(log_path, "a", encoding="utf-8") as f:
            f.write(f"  [ai_service] API响应长度: {len(json.dumps(result))}\n")

        ai_text = ""
        for block in result.get("content", []):
            if block.get("type") == "text":
                ai_text = block["text"]
        
        with open(log_path, "a", encoding="utf-8") as f:
            f.write(f"  [ai_service] 提取文本长度: {len(ai_text)}\n")
            f.write(f"  [ai_service] 文本内容: {ai_text[:200]}...\n")

        cleaned_text = ai_text.strip().strip("```json").strip("```").strip()
        import re
        cleaned_text = re.sub(r'":":\s*', '": "', cleaned_text)
        ai_data = json.loads(cleaned_text)
        
        with open(log_path, "a", encoding="utf-8") as f:
            f.write(f"  [ai_service] 解析JSON成功: emotion={ai_data.get('emotion_label')}\n")

        analysis = EmotionAnalysis(
            diary_id=diary_id,
            user_id=user_id,
            emotion_label=ai_data.get("emotion_label"),
            emotion_score=ai_data.get("emotion_score"),
            analysis_detail=ai_data.get("analysis_detail"),
            suggestion=ai_data.get("suggestion"),
            model_used=result.get("model", ARK_MODEL),
            prompt=prompt,
            raw_response=json.dumps(result, ensure_ascii=False),
            ai_text=ai_text,
        )
        db.add(analysis)
        db.commit()
        
        with open(log_path, "a", encoding="utf-8") as f:
            f.write(f"  [ai_service] 数据库提交成功\n")
            f.write(f"  [ai_service] AI分析完成: emotion={ai_data.get('emotion_label')}\n")
            
    except Exception as e:
        with open(log_path, "a", encoding="utf-8") as f:
            f.write(f"  [ai_service] 错误: {e}\n")
            import traceback
            f.write(traceback.format_exc())
        if db:
            db.rollback()
    finally:
        if db:
            db.close()
            with open(log_path, "a", encoding="utf-8") as f:
                f.write(f"  [ai_service] 数据库会话关闭\n")
