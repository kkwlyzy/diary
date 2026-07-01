import random
import string
import time
from io import BytesIO
from PIL import Image, ImageDraw, ImageFont
from typing import Optional

_captcha_store = {}
_CAPTCHA_EXPIRE_SECONDS = 120
_MAX_SEND_INTERVAL = 60


def generate_captcha_text(length: int = 4) -> str:
    chars = string.digits + string.ascii_uppercase
    return ''.join(random.choice(chars) for _ in range(length))


def generate_captcha_image(text: str) -> bytes:
    width = 120
    height = 40
    image = Image.new('RGB', (width, height), (255, 255, 255))
    draw = ImageDraw.Draw(image)
    
    font_size = 24
    try:
        font = ImageFont.truetype('arial.ttf', font_size)
    except:
        font = ImageFont.load_default()
    
    for i, char in enumerate(text):
        x = 15 + i * 25
        y = random.randint(5, 10)
        draw.text((x, y), char, fill=(0, 0, 0), font=font)
    
    for _ in range(30):
        x1 = random.randint(0, width)
        y1 = random.randint(0, height)
        x2 = random.randint(0, width)
        y2 = random.randint(0, height)
        draw.line((x1, y1, x2, y2), fill=(180, 180, 180), width=1)
    
    for _ in range(50):
        x = random.randint(0, width)
        y = random.randint(0, height)
        draw.point((x, y), fill=(180, 180, 180))
    
    buffer = BytesIO()
    image.save(buffer, format='PNG')
    return buffer.getvalue()


def create_captcha(session_id: str) -> bytes:
    text = generate_captcha_text()
    _captcha_store[session_id] = {
        'text': text,
        'created_at': time.time(),
        'send_count': 1
    }
    return generate_captcha_image(text)


def validate_captcha(session_id: str, input_text: str) -> bool:
    data = _captcha_store.get(session_id)
    if not data:
        return False
    if time.time() - data['created_at'] > _CAPTCHA_EXPIRE_SECONDS:
        del _captcha_store[session_id]
        return False
    result = data['text'].lower() == input_text.strip().lower()
    if result:
        del _captcha_store[session_id]
    return result


def can_send_captcha(session_id: str) -> bool:
    data = _captcha_store.get(session_id)
    if not data:
        return True
    if time.time() - data['created_at'] >= _MAX_SEND_INTERVAL:
        return True
    return False


def cleanup_expired_captchas():
    now = time.time()
    expired_keys = [k for k, v in _captcha_store.items() if now - v['created_at'] > _CAPTCHA_EXPIRE_SECONDS]
    for key in expired_keys:
        del _captcha_store[key]