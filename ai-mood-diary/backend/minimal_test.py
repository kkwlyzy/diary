import sys
print("Python version:", sys.version)

import uvicorn
from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def root():
    return {"message": "Hello World"}

print("Starting server...")
uvicorn.run(app, host='0.0.0.0', port=8001)
