import requests
import json

BASE_URL = "http://localhost:8001/api"

def test_update_diary():
    # 1. 注册/登录用户
    print("=== 步骤1: 登录用户 ===")
    login_data = {
        "username": "testuser2",
        "password": "test123456"
    }
    
    # 尝试登录
    login_resp = requests.post(f"{BASE_URL}/auth/login", json=login_data)
    print(f"登录状态: {login_resp.status_code}")
    
    if login_resp.status_code != 200:
        # 尝试注册
        print("用户不存在，尝试注册...")
        register_data = {
            "username": "testuser2",
            "password": "test123456",
            "email": "test2@example.com"
        }
        reg_resp = requests.post(f"{BASE_URL}/auth/register", json=register_data)
        print(f"注册状态: {reg_resp.status_code}")
        print(f"注册响应: {reg_resp.text}")
        
        if reg_resp.status_code == 200:
            login_resp = requests.post(f"{BASE_URL}/auth/login", json=login_data)
            print(f"登录状态: {login_resp.status_code}")
    
    if login_resp.status_code != 200:
        print(f"登录失败: {login_resp.text}")
        return
    
    token_data = login_resp.json()
    token = token_data.get("access_token")
    print(f"获取到token: {token[:20]}...")
    
    headers = {"Authorization": f"Bearer {token}"}
    
    # 2. 创建一篇测试日记
    print("\n=== 步骤2: 创建测试日记 ===")
    create_data = {
        "title": "测试日记标题",
        "content": "这是一篇测试日记的内容",
        "mood_tag": "happy",
        "weather": "晴天",
        "date": "2024-01-15"
    }
    create_resp = requests.post(f"{BASE_URL}/diaries", json=create_data, headers=headers)
    print(f"创建日记状态: {create_resp.status_code}")
    print(f"创建日记响应: {json.dumps(create_resp.json(), ensure_ascii=False, indent=2)}")
    
    if create_resp.status_code != 200:
        print("创建日记失败")
        return
    
    diary_id = create_resp.json().get("id")
    print(f"日记ID: {diary_id}")
    
    # 3. 获取日记详情
    print("\n=== 步骤3: 获取日记详情 ===")
    get_resp = requests.get(f"{BASE_URL}/diaries/{diary_id}", headers=headers)
    print(f"获取日记状态: {get_resp.status_code}")
    if get_resp.status_code == 200:
        print(f"日记详情: {json.dumps(get_resp.json(), ensure_ascii=False, indent=2)}")
    
    # 4. 编辑日记
    print("\n=== 步骤4: 编辑日记 ===")
    update_data = {
        "title": "修改后的标题",
        "content": "这是修改后的日记内容",
        "mood_tag": "calm",
        "weather": "多云",
        "date": "2024-01-16"
    }
    update_resp = requests.put(f"{BASE_URL}/diaries/{diary_id}", json=update_data, headers=headers)
    print(f"更新日记状态: {update_resp.status_code}")
    print(f"更新日记响应: {update_resp.text}")
    
    if update_resp.status_code == 200:
        print("\n✅ 更新成功！")
        print(f"更新后的数据: {json.dumps(update_resp.json(), ensure_ascii=False, indent=2)}")
    else:
        print(f"\n❌ 更新失败: {update_resp.text}")
        
        # 检查后端日志
        print("\n=== 检查错误详情 ===")
        try:
            error_data = update_resp.json()
            print(f"错误详情: {json.dumps(error_data, ensure_ascii=False, indent=2)}")
        except:
            print(f"无法解析错误响应: {update_resp.text}")

if __name__ == "__main__":
    test_update_diary()