import sys

print("Step 1: Loading config...")
sys.stdout.flush()

import os
os.environ['ARK_API_KEY'] = 'ark-008c7019-c676-43cd-98c3-967476ca543b-56875'

print("Step 2: Loading database...")
sys.stdout.flush()

try:
    from app.database import engine, SessionLocal, Base
    print("Step 2a: Database loaded")
    sys.stdout.flush()
except Exception as e:
    print(f"DB Error: {e}")
    import traceback
    traceback.print_exc()
    sys.stdout.flush()
    sys.exit(1)

print("Step 3: Loading models...")
sys.stdout.flush()

try:
    from app.models.user import User
    print("Step 3a: User model")
    sys.stdout.flush()
    
    from app.models.diary import Diary
    print("Step 3b: Diary model")
    sys.stdout.flush()
    
    from app.models.emotion import EmotionAnalysis
    print("Step 3c: Emotion model")
    sys.stdout.flush()
except Exception as e:
    print(f"Model Error: {e}")
    import traceback
    traceback.print_exc()
    sys.stdout.flush()
    sys.exit(1)

print("Step 4: Creating tables...")
sys.stdout.flush()

try:
    Base.metadata.create_all(bind=engine)
    print("Step 4a: Tables created")
    sys.stdout.flush()
except Exception as e:
    print(f"Table Error: {e}")
    import traceback
    traceback.print_exc()
    sys.stdout.flush()
    sys.exit(1)

print("Step 5: Loading app...")
sys.stdout.flush()

try:
    from app.main import app
    print("Step 5a: App loaded")
    sys.stdout.flush()
except Exception as e:
    print(f"App Error: {e}")
    import traceback
    traceback.print_exc()
    sys.stdout.flush()
    sys.exit(1)

print("Step 6: Starting uvicorn...")
sys.stdout.flush()

try:
    import uvicorn
    uvicorn.run(app, host='0.0.0.0', port=8001, log_level='info')
except Exception as e:
    print(f"Server Error: {e}")
    import traceback
    traceback.print_exc()
    sys.stdout.flush()
