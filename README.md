# AI 心情日记 (AI Mood Diary)

一个基于 AI 的情绪日记系统。撰写日记后自动调用大语言模型分析情绪，提供可视化的情绪追踪与统计。

## 项目作用

- **智能情绪分析**：写日记后自动由 AI 识别情绪（快乐、悲伤、焦虑、平静、愤怒、惊讶），返回情绪强度评分、分析描述和温暖建议
- **情绪可视化**：日历视图、情绪趋势折线图、情绪分布饼图，直观追踪情绪变化
- **日记管理**：完整的增删改查，支持情绪筛选、日期筛选、批量操作、批量导出
- **用户系统**：JWT 认证、验证码注册、个人中心

## 技术栈

| 层级 | 技术 |
|------|------|
| 前端 | Vue 3 + Vite + Element Plus + Pinia + ECharts |
| 后端 | FastAPI + SQLAlchemy + JWT |
| 数据库 | MySQL / SQLite（自动回退） |
| AI | 火山引擎方舟（Anthropic 兼容接口） |
| 部署 | Docker Compose + Nginx |

## 项目结构

```
ai-mood-diary/
├── docker-compose.yml          # Docker 编排
├── Dockerfile.backend           # 后端镜像
├── Dockerfile.frontend          # 前端镜像
├── nginx.conf                   # 前端 Nginx 配置
├── backend/
│   ├── run.py                   # 启动入口
│   ├── .env                     # 环境变量配置（API Key 等）
│   └── app/
│       ├── main.py              # FastAPI 应用入口
│       ├── config.py            # 统一配置中心
│       ├── database.py          # 数据库引擎（MySQL/SQLite 自动回退）
│       ├── models/              # 数据模型（User, Diary, EmotionAnalysis）
│       ├── schemas/             # Pydantic 请求/响应模型
│       ├── routers/             # API 路由（auth, diary, ai, statistics, captcha）
│       ├── services/            # 业务逻辑层
│       └── utils/               # 工具（JWT）
└── frontend/
    └── src/
        ├── views/               # 页面（登录、日记列表、编辑、详情、日历、统计、个人中心）
        ├── components/          # 公共组件
        ├── api/                 # API 请求封装
        ├── stores/              # Pinia 状态管理
        └── router/              # 路由配置
```

## 本地开发部署

### 环境要求

- Python 3.12+
- Node.js 20+
- MySQL 8.0+（可选，连接失败自动回退 SQLite）

### 1. 克隆项目

```bash
git clone <仓库地址>
cd ai-mood-diary
```

### 2. 配置 API Key

编辑 `backend/.env` 文件，填入火山引擎方舟 API Key：

```env
ARK_API_KEY=你的API_Key
```

其他配置项（数据库、JWT 等）已有默认值，按需修改。

### 3. 启动后端

```bash
cd backend

# 创建虚拟环境
python -m venv venv
venv\Scripts\activate     # Windows
source venv/bin/activate  # Linux/Mac

# 安装依赖
pip install -r requirements.txt

# 启动服务
python run.py
```

后端运行在 `http://localhost:8001`。

### 4. 启动前端

```bash
cd frontend

# 安装依赖
npm install

# 启动开发服务器
npm run dev
```

前端运行在 `http://localhost:5173`，自动代理 API 请求到后端。

## Docker 部署

### 一键启动

```bash
# 设置 API Key 环境变量
export ARK_API_KEY=你的API_Key    # Linux/Mac
$env:ARK_API_KEY="你的API_Key"    # Windows PowerShell

# 构建并启动
docker-compose up -d --build
```

### 服务端口

| 服务 | 端口 | 说明 |
|------|------|------|
| 前端 (Nginx) | 80 | 静态资源 + API 反向代理 |
| 后端 (Uvicorn) | 8000 | FastAPI 服务 |

访问 `http://localhost` 即可使用。

## API 配置

所有配置统一在 `backend/app/config.py` 中管理，通过 `backend/.env` 文件覆盖：

| 配置项 | 说明 | 默认值 |
|--------|------|--------|
| `ARK_API_KEY` | 火山引擎 API Key | 无（必填） |
| `ARK_API_BASE` | API 地址 | `https://ark.cn-beijing.volces.com/api/coding` |
| `ARK_MODEL` | 模型名称 | `ark-code-latest` |
| `DB_HOST` | 数据库地址 | `192.168.100.130` |
| `DB_PORT` | 数据库端口 | `3306` |
| `DB_USER` | 数据库用户 | `bookadmin` |
| `DB_PASSWORD` | 数据库密码 | `123456` |
| `DB_NAME` | 数据库名 | `ai_mood_diary` |
| `JWT_SECRET_KEY` | JWT 密钥 | 内置默认值 |

> 数据库连接失败时自动回退到 SQLite，无需手动切换。

## 主要功能

- 用户注册/登录（图形验证码 + JWT 认证）
- 日记创建/编辑/删除/查看（含 AI 实时分析）
- 情绪筛选与日期筛选
- 批量删除、批量修改情绪、批量导出（Markdown/JSON）
- 日历视图（情绪颜色标记）
- 情绪趋势折线图与分布饼图
- 个人中心（修改昵称、邮箱、头像）
