import requests
import json

BASE_URL = "http://localhost:8001/api"

def test_captcha_flow():
    print("=== 测试1: 获取验证码 ===")
    resp = requests.get(f"{BASE_URL}/captcha/")
    print(f"状态码: {resp.status_code}")
    print(f"响应头: {resp.headers}")
    
    captcha_session = resp.headers.get('X-Captcha-Session')
    print(f"Captcha Session: {captcha_session}")
    
    if resp.status_code != 200:
        print("获取验证码失败")
        return
    
    print("\n=== 测试2: 使用错误验证码注册 ===")
    register_data = {
        "username": "testcaptcha",
        "password": "test123456",
        "nickname": "测试用户",
        "email": "testcaptcha@example.com",
        "captcha": "WRONG",
        "captcha_session": captcha_session
    }
    
    register_resp = requests.post(f"{BASE_URL}/auth/register", json=register_data)
    print(f"状态码: {register_resp.status_code}")
    print(f"响应: {register_resp.text}")
    
    if register_resp.status_code == 400:
        error_detail = register_resp.json().get("detail")
        if error_detail == "验证码错误":
            print("✅ 错误验证码测试通过")
        else:
            print(f"❌ 错误提示不正确: {error_detail}")
    else:
        print("❌ 未返回400状态码")
    
    print("\n=== 测试3: 获取新验证码 ===")
    resp2 = requests.get(f"{BASE_URL}/captcha/")
    captcha_session2 = resp2.headers.get('X-Captcha-Session')
    print(f"新 Captcha Session: {captcha_session2}")
    
    print("\n测试完成!")

if __name__ == "__main__":
    test_captcha_flow()