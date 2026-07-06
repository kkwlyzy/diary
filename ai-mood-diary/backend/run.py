import sys
import os

_extra_packages = os.path.join(os.path.dirname(__file__), 'packages')
if os.path.exists(_extra_packages):
    sys.path.insert(0, _extra_packages)

import uvicorn

if __name__ == "__main__":
    uvicorn.run("app.main:app", host="0.0.0.0", port=8001)
