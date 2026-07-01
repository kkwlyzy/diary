from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .database import engine, Base
from .routers import auth, diary, statistics, ai, captcha

# 创建数据库表
Base.metadata.create_all(bind=engine)

app = FastAPI(title="AI心情日记", description="AI Mood Diary API", version="1.0.0")

# CORS 配置
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["X-Captcha-Session"],
)

# 注册路由
app.include_router(auth.router)
app.include_router(diary.router)
app.include_router(statistics.router)
app.include_router(ai.router)
app.include_router(captcha.router)


@app.get("/")
def root():
    return {"message": "AI心情日记 API 服务运行中"}
