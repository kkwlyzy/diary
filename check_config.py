import sys
sys.path.insert(0, 'e:/keshe/ai-mood-diary/backend')

from app.config import ARK_API_KEY, ARK_API_BASE, ARK_MODEL

print(f"ARK_API_KEY: {ARK_API_KEY}")
print(f"ARK_API_BASE: {ARK_API_BASE}")
print(f"ARK_MODEL: {ARK_MODEL}")

import os
print(f"\n环境变量 ARK_API_KEY: {os.getenv('ARK_API_KEY', '未设置')}")
