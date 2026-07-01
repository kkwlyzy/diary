import sys
sys.path.insert(0, '.')
print("Python version:", sys.version)

import os
os.environ['ARK_API_KEY'] = 'ark-008c7019-c676-43cd-98c3-967476ca543b-56875'

print("Step 1: Creating SQLite engine...")
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

SQLITE_URL = "sqlite:///./test.db"
engine = create_engine(SQLITE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

print("Step 2: Loading models...")
from app.models.user import User
from app.models.diary import Diary
from app.models.emotion import EmotionAnalysis

print("Step 3: Creating tables...")
Base.metadata.create_all(bind=engine)

print("Step 4: Creating app...")
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

print("Step 5: Loading routers...")
from app.routers import auth, diary, statistics, ai
app.include_router(auth.router)
app.include_router(diary.router)
app.include_router(statistics.router)
app.include_router(ai.router)

@app.get("/")
def root():
    return {"message": "AI心情日记 API 服务运行中"}

print("Step 6: Starting server...")
import uvicorn
uvicorn.run(app, host='0.0.0.0', port=8001, log_level='info')
