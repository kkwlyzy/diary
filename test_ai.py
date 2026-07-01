import httpx, time, sys

try:
    print('注册用户...', flush=True)
    r = httpx.post('http://localhost:8001/api/auth/register', json={'username':'test4','password':'123456'}, timeout=10)
    print(f'注册状态: {r.status_code}', flush=True)

    r = httpx.post('http://localhost:8001/api/auth/login', json={'username':'test4','password':'123456'}, timeout=10)
    print(f'登录状态: {r.status_code}', flush=True)
    if r.status_code != 200:
        print(f'登录失败: {r.text}', flush=True)
        sys.exit(1)
    token = r.json()['access_token']
    headers = {'Authorization': f'Bearer {token}'}
    print('登录成功', flush=True)

    r = httpx.post('http://localhost:8001/api/diaries', json={
        'title': 'AI测试',
        'content': '今天心情非常好，阳光明媚，和朋友一起去了公园散步，感觉生活很美好。',
        'mood_tag': 'happy',
        'weather': '晴',
        'date': '2026-06-26'
    }, headers=headers, timeout=10)
    print(f'创建日记状态: {r.status_code}', flush=True)
    if r.status_code != 200:
        print(f'创建失败: {r.text}', flush=True)
        sys.exit(1)
    diary_id = r.json()['id']
    print(f'创建日记成功, id={diary_id}', flush=True)

    print('等待 AI 分析...', flush=True)
    time.sleep(15)

    r = httpx.get(f'http://localhost:8001/api/diaries/{diary_id}', headers=headers, timeout=10)
    print(f'查询状态: {r.status_code}', flush=True)
    data = r.json()
    emotion = data.get('emotion')
    if emotion:
        print('AI分析完成!', flush=True)
        print(f'情绪: {emotion["emotion_label"]}', flush=True)
        print(f'建议: {emotion["suggestion"]}', flush=True)
    else:
        print('AI分析尚未完成', flush=True)
        print(f'日记数据: {data}', flush=True)
except Exception as e:
    print(f'错误: {e}', flush=True)
    import traceback
    traceback.print_exc()
