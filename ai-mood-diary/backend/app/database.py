import os
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker, declarative_base
from .config import DB_CONFIG, DATABASE_URL

SQLITE_URL = "sqlite:///./ai_mood_diary.db"

try:
    init_engine = create_engine(
        f"mysql+pymysql://{DB_CONFIG['user']}:{DB_CONFIG['password']}@{DB_CONFIG['host']}:{DB_CONFIG['port']}?charset=utf8mb4",
        connect_args={"connect_timeout": 3}
    )
    with init_engine.connect() as conn:
        conn.execute(text(f"CREATE DATABASE IF NOT EXISTS `{DB_CONFIG['database']}` CHARACTER SET utf8mb4"))
        conn.commit()
    init_engine.dispose()

    engine = create_engine(DATABASE_URL, pool_size=10, max_overflow=20)
    print("[INFO] 已连接到 MySQL 数据库")
except Exception as e:
    print(f"[WARN] MySQL 连接失败 ({e})，自动回退到 SQLite")
    engine = create_engine(SQLITE_URL, connect_args={"check_same_thread": False})

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
