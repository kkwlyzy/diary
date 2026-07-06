# 开发过程关键 Prompt 记录

## 一、大模型 API 调用 Prompt

### 1.1 情绪分析 Prompt（核心）

**调用位置**：[ai_service.py:25-38](file:///e:/keshe/ai-mood-diary/backend/app/services/ai_service.py#L25-L38)

```
你是一个温柔的心理咨询师。请分析以下日记内容的情绪倾向，以JSON格式返回。

日记标题：{title}
日记内容：{content}

请从以下情绪标签中选择最匹配的一个：happy（快乐）, sad（悲伤）, anxious（焦虑）, calm（平静）, angry（愤怒）, surprised（惊讶）

返回格式（只返回JSON，不要其他文字）：
{{
    "emotion_label": "情绪标签",
    "emotion_score": 0.00-1.00之间的情绪强度分数,
    "analysis_detail": "50字以内的情绪分析",
    "suggestion": "50字以内的温暖建议"
}}
```

**设计要点**：
- 角色定位：温柔的心理咨询师，确保输出语气温暖友好
- 输入变量：日记标题和内容，通过 Python f-string 动态填充
- 情绪标签约束：限定6种情绪标签，确保前端可以正确映射
- 输出格式：强制 JSON 格式，便于后端解析
- 字数限制：分析和建议均限制在50字以内，保证响应简洁

**API 调用参数**：
- 模型：`ark-code-latest`（火山引擎方舟 Coding Plan）
- 最大 token：1000
- 接口：`/v1/messages`（Anthropic 兼容）

---

## 二、开发过程向 AI 编程助手提问的关键 Prompt

### 2.1 API Key 统一管理

**提问**：查看项目中 apikey，我怀疑出现了很多 apikey 不能统一管理

**背景**：发现项目中多处配置文件存在 API Key，担心管理混乱和安全问题

**解决方案**：确认 API Key 已统一管理，但存在日志泄露问题，随后进行了以下优化：
1. 移除 [ai_service.py](file:///e:/keshe/ai-mood-diary/backend/app/services/ai_service.py) 中泄露 API Key 的日志行
2. 将 config.py 设为唯一真相源，移除 docker-compose.yml 和 .env 中的重复默认值
3. 修复硬编码的日志路径

---

### 2.2 AI 分析失败处理

**提问**：现在修改日记的ai分析问题，如果ai分析日记失败，则出现，ai咱不可用

**背景**：AI 分析失败时前端统一显示"正在生成中"，无法区分失败和处理中状态

**解决方案**：
1. 在 [ai_service.py](file:///e:/keshe/ai-mood-diary/backend/app/services/ai_service.py) 中添加 fallback 逻辑，AI 调用失败时写入 `emotion_label="unavailable"` 标记记录
2. 在 [DiaryDetail.vue](file:///e:/keshe/ai-mood-diary/frontend/src/views/DiaryDetail.vue) 和 [DiaryList.vue](file:///e:/keshe/ai-mood-diary/frontend/src/views/DiaryList.vue) 中添加三态判断（completed/unavailable/pending）
3. 后端返回 `ai_status` 字段，支持时间判断（日记创建超过60秒无分析结果视为失败）

---

### 2.3 AI 状态时间判断

**提问**：我觉得 AI 情绪分析正在生成中，请稍后查看... 这个需要改变，如果说 我的ai调用失败，怎么输出，应该输出什么

**背景**：用户创建日记后立即查看，AI 可能还在处理或已失败，但此时 `emotion` 都是 `null`，前端无法区分

**解决方案**：
1. 在 [diary.py](file:///e:/keshe/ai-mood-diary/backend/app/routers/diary.py) 的 `GET /{id}` 接口中添加 `ai_status` 字段
2. 实现状态判断逻辑：
   - emotion 存在且非 unavailable → completed
   - emotion 存在且为 unavailable → unavailable
   - emotion 不存在 + 日记创建 > 60s → unavailable
   - emotion 不存在 + 日记创建 ≤ 60s → pending
3. 在 [ai.py](file:///e:/keshe/ai-mood-diary/backend/app/routers/ai.py) 的 `/today-analysis` 接口中同样添加时间判断

---

### 2.4 API 重试机制

**提问**：添加重试机制

**背景**：短时间内连续创建日记导致火山引擎 API 返回 429 Too Many Requests，AI 分析失败

**解决方案**：
1. 在 [ai_service.py](file:///e:/keshe/ai-mood-diary/backend/app/services/ai_service.py) 中实现指数退避重试机制
2. 重试策略：最多3次，延迟分别为 3秒、6秒、12秒
3. 可重试错误码：429（限流）、500/502/503/504（服务端错误）、网络连接超时

---

### 2.5 系统文档生成

**提问**：用系统框图说明系统的功能模块划分，并文字描述各模块职责

**背景**：需要为项目生成技术文档，说明系统架构和模块职责

**解决方案**：生成包含系统架构图、功能模块划分、模块交互流程和核心技术栈的详细文档

---

### 2.6 测试用例整理

**提问**：列出测试用例与测试结果，须包含批量处理场景与 AI 错误兜底场景。以表格的形式列出

**背景**：需要整理项目的测试用例和测试结果，确保覆盖核心功能和边缘场景

**解决方案**：生成包含30个测试用例的表格，覆盖用户认证、日记管理、AI 分析、批量操作、统计分析等场景

---

## 三、Prompt 设计原则总结

### 3.1 大模型 API Prompt 设计原则

1. **明确角色定位**：为 AI 指定清晰的角色（如"温柔的心理咨询师"）
2. **输入约束**：明确输入格式和变量
3. **输出格式**：强制指定输出格式（如 JSON），便于程序解析
4. **内容限制**：限定输出内容范围（如情绪标签列表、字数限制）
5. **语气要求**：根据业务场景指定语气风格（如温暖、专业）

### 3.2 开发提问 Prompt 设计原则

1. **明确问题**：清晰描述问题现象和预期结果
2. **提供上下文**：说明项目技术栈和相关文件
3. **分阶段提问**：复杂问题拆分为多个步骤，逐步深入
4. **验证反馈**：测试后及时反馈结果，调整提问方向
5. **安全意识**：涉及 API Key 等敏感信息时，确保不在日志中暴露