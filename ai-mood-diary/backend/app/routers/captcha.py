import uuid
import base64
from fastapi import APIRouter, HTTPException
from fastapi.responses import Response
from ..services import captcha_service

router = APIRouter(prefix="/api/captcha", tags=["验证码"])


@router.get("/")
def get_captcha():
    session_id = str(uuid.uuid4())
    image_data = captcha_service.create_captcha(session_id)
    return Response(
        content=image_data,
        media_type="image/png",
        headers={"X-Captcha-Session": session_id}
    )


@router.get("/json")
def get_captcha_json():
    session_id = str(uuid.uuid4())
    image_data = captcha_service.create_captcha(session_id)
    b64 = base64.b64encode(image_data).decode("utf-8")
    return {
        "session_id": session_id,
        "image_base64": f"data:image/png;base64,{b64}"
    }