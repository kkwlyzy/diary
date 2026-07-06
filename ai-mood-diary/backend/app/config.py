import os
from dotenv import load_dotenv

load_dotenv(override=True)

# 数据库配置
DB_CONFIG = {
    "host": os.getenv("DB_HOST", "192.168.100.130"),
    "port": int(os.getenv("DB_PORT", 3306)),
    "user": os.getenv("DB_USER", "bookadmin"),
    "password": os.getenv("DB_PASSWORD", "123456"),
    "database": os.getenv("DB_NAME", "ai_mood_diary"),
}

DATABASE_URL = f"mysql+pymysql://{DB_CONFIG['user']}:{DB_CONFIG['password']}@{DB_CONFIG['host']}:{DB_CONFIG['port']}/{DB_CONFIG['database']}?charset=utf8mb4"

# JWT 配置
JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY", "ai-mood-diary-secret-key-2024")
JWT_ALGORITHM = "HS256"
JWT_ACCESS_TOKEN_EXPIRE_MINUTES = 60 * 24  # 24小时

# 火山引擎方舟 AI 配置（Coding Plan - Anthropic 兼容接口）
# ⚠️ 所有 API 配置统一在此管理，config.py 是唯一真相源
# 通过环境变量覆盖默认值，运行前设置：$env:ARK_API_KEY="your-key"
ARK_API_KEY = os.getenv("ARK_API_KEY")
ARK_API_BASE = os.getenv("ARK_API_BASE") or "https://ark.cn-beijing.volces.com/api/coding"
ARK_MODEL = os.getenv("ARK_MODEL") or "ark-code-latest"
