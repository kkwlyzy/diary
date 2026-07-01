import sys
import os

_extra_packages = os.path.join(os.path.dirname(__file__), 'packages')
if os.path.exists(_extra_packages):
    sys.path.insert(0, _extra_packages)

os.environ['ARK_API_KEY'] = 'ark-008c7019-c676-43cd-98c3-967476ca543b-56875'

import uvicorn

if __name__ == "__main__":
    uvicorn.run("app.main:app", host="0.0.0.0", port=8001)
