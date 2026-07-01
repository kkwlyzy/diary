import sys
sys.stdout.flush()
sys.stderr.flush()

print("Step 1: Loading config...")
sys.stdout.flush()

import os
os.environ['ARK_API_KEY'] = 'ark-008c7019-c676-43cd-98c3-967476ca543b-56875'

print("Step 2: Loading app...")
sys.stdout.flush()

try:
    from app.main import app
    print("Step 3: App loaded successfully")
    sys.stdout.flush()
    
    print("Step 4: Starting uvicorn...")
    sys.stdout.flush()
    
    import uvicorn
    uvicorn.run(app, host='0.0.0.0', port=8001, log_level='info')
except Exception as e:
    print(f"Error: {e}")
    import traceback
    traceback.print_exc()
    sys.stdout.flush()
