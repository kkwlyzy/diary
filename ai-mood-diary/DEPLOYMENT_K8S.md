# AI 心情日记 - Kubernetes 部署文档

## 项目简介

AI 心情日记是一款基于 AI 的情感分析日记应用，帮助用户记录日常心情，通过 AI 分析日记内容，提供情绪统计和建议。

### 技术栈

| 层级 | 技术 | 说明 |
|------|------|------|
| 前端 | Vue 3 + Vite | 单页应用，响应式设计 |
| 后端 | FastAPI + Python | RESTful API，AI 分析服务 |
| 数据库 | MySQL 8.0 | 数据持久化存储 |
| AI 服务 | 火山引擎 ARK | 情感分析 API |

### 项目功能

- **日记管理**：创建、编辑、删除日记
- **AI 情感分析**：自动分析日记情绪
- **情绪统计**：可视化情绪变化趋势
- **用户系统**：注册、登录、JWT 认证

---

## Kubernetes 部署架构

```
┌─────────────────────────────────────────────────────────┐
│                      Ingress                            │
│            mood-diary.example.com                       │
├──────────────┬──────────────────────────────────────────┤
│   /api/*     │           /*                             │
├──────────────┼──────────────────────────────────────────┤
│  Backend     │          Frontend                        │
│  Service     │          Service                         │
│  (ClusterIP) │          (ClusterIP)                     │
├──────────────┼──────────────────────────────────────────┤
│  Deployment  │          Deployment                      │
│  (2-5 pods)  │          (2-5 pods)                      │
├──────────────┴──────────────────────────────────────────┤
│                    MySQL                                │
│              (StatefulSet)                              │
│            PersistentVolume                             │
└─────────────────────────────────────────────────────────┘
```

---

## 部署前提

### 环境要求

- Kubernetes 集群 >= 1.24
- Docker 环境（用于构建镜像）
- kubectl 已配置并连接到集群
- 已安装 Nginx Ingress Controller（可选）

### 镜像构建

在部署前，需要先构建前端和后端镜像：

```bash
# 构建后端镜像
docker build -t mood-diary-backend:latest -f Dockerfile.backend .

# 构建前端镜像
docker build -t mood-diary-frontend:latest -f Dockerfile.frontend .

# 如果使用私有镜像仓库，推送到仓库
docker tag mood-diary-backend:latest your-registry/mood-diary-backend:latest
docker tag mood-diary-frontend:latest your-registry/mood-diary-frontend:latest
docker push your-registry/mood-diary-backend:latest
docker push your-registry/mood-diary-frontend:latest
```

---

## 配置文件说明

所有配置文件位于 `k8s/` 目录下，按顺序部署：

| 文件 | 资源类型 | 说明 |
|------|----------|------|
| `00-resourcequota.yaml` | ResourceQuota | 命名空间资源配额限制 |
| `00-limitrange.yaml` | LimitRange | 容器资源默认请求和限制 |
| `01-namespace.yaml` | Namespace | 创建专用命名空间 |
| `02-configmap.yaml` | ConfigMap | 数据库连接、JWT、API 地址等配置 |
| `03-secret.yaml` | Secret | 数据库密码、ARK API Key（Base64 编码） |
| `08-backend-deployment.yaml` | Deployment | 后端 API 服务部署 |
| `09-backend-service.yaml` | Service | 后端服务（ClusterIP） |
| `10-frontend-deployment.yaml` | Deployment | 前端应用部署 |
| `11-frontend-service.yaml` | Service | 前端服务（ClusterIP） |
| `12-ingress.yaml` | Ingress | 路由配置（可选） |
| `13-hpa-backend.yaml` | HPA | 后端自动扩缩容 |
| `13-hpa-frontend.yaml` | HPA | 前端自动扩缩容 |

---

## 部署步骤

### 1. 创建命名空间

```bash
kubectl apply -f k8s/01-namespace.yaml
```

### 2. 部署资源配额和限制范围

```bash
kubectl apply -f k8s/00-resourcequota.yaml
kubectl apply -f k8s/00-limitrange.yaml
```

### 3. 更新 Secret 配置

**重要**：`03-secret.yaml` 中的敏感数据需要使用 Base64 编码。

```bash
# 生成数据库密码 Base64（示例：123456）
echo -n "123456" | base64

# 生成 ARK API Key Base64（替换为你的真实 Key）
echo -n "ark-your-api-key" | base64
```

编辑 `k8s/03-secret.yaml`，替换 `DB_PASSWORD` 和 `ARK_API_KEY` 的值。

### 4. 部署配置和密钥

```bash
kubectl apply -f k8s/02-configmap.yaml
kubectl apply -f k8s/03-secret.yaml
```

### 5. 部署后端服务

```bash
kubectl apply -f k8s/08-backend-deployment.yaml
kubectl apply -f k8s/09-backend-service.yaml
```

### 6. 部署前端服务

```bash
kubectl apply -f k8s/10-frontend-deployment.yaml
kubectl apply -f k8s/11-frontend-service.yaml
```

### 7. 部署 Ingress（可选）

首先确保集群已安装 Nginx Ingress Controller：

```bash
# 检查 Ingress Controller 是否安装
kubectl get pods -n ingress-nginx
```

如果未安装，执行：

```bash
kubectl apply -f https://raw.githubusercontent.com/kubernetes/ingress-nginx/main/deploy/static/provider/cloud/deploy.yaml
```

然后部署 Ingress：

```bash
kubectl apply -f k8s/12-ingress.yaml
```

### 8. 部署自动扩缩容（可选）

```bash
kubectl apply -f k8s/13-hpa-backend.yaml
kubectl apply -f k8s/13-hpa-frontend.yaml
```

---

## 快速部署命令

使用一行命令部署所有资源：

```bash
kubectl apply -f k8s/
```

---

## 验证部署

### 查看所有资源

```bash
# 查看命名空间
kubectl get ns ai-mood-diary

# 查看 Pod
kubectl get pods -n ai-mood-diary -o wide

# 查看 Service
kubectl get svc -n ai-mood-diary

# 查看 Deployment
kubectl get deploy -n ai-mood-diary

# 查看 Ingress
kubectl get ingress -n ai-mood-diary
```

### 测试后端 API

```bash
# 端口转发测试
kubectl port-forward svc/mood-diary-backend 8000:8000 -n ai-mood-diary

# 访问健康检查接口
curl http://localhost:8000/health
```

### 测试前端

```bash
# 端口转发测试
kubectl port-forward svc/mood-diary-frontend 8080:80 -n ai-mood-diary

# 打开浏览器访问
# http://localhost:8080
```

---

## 配置说明

### ConfigMap 配置项

| 配置项 | 默认值 | 说明 |
|--------|--------|------|
| DB_HOST | mood-diary-mysql | MySQL 服务名 |
| DB_PORT | 3306 | MySQL 端口 |
| DB_USER | bookadmin | 数据库用户名 |
| DB_NAME | ai_mood_diary | 数据库名 |
| JWT_SECRET_KEY | ai-mood-diary-secret-key-2024 | JWT 密钥 |
| ARK_API_BASE | https://ark.cn-beijing.volces.com/api/coding | ARK API 地址 |
| ARK_MODEL | arkmind-v2 | 使用的 AI 模型 |

### Secret 配置项

| 配置项 | 说明 |
|--------|------|
| DB_PASSWORD | 数据库密码（Base64 编码） |
| ARK_API_KEY | 火山引擎 ARK API Key（Base64 编码） |

### ResourceQuota 配置项

| 配置项 | 值 | 说明 |
|--------|-----|------|
| requests.cpu | 1 | 总 CPU 请求限制 |
| requests.memory | 2Gi | 总内存请求限制 |
| limits.cpu | 3 | 总 CPU 上限 |
| limits.memory | 4Gi | 总内存上限 |
| requests.storage | 15Gi | 总存储请求限制 |
| persistentvolumeclaims | 5 | PVC 数量限制 |
| pods | 10 | Pod 数量限制 |
| services | 5 | Service 数量限制 |

### LimitRange 配置项

| 配置项 | 值 | 说明 |
|--------|-----|------|
| default.cpu | 200m | 容器默认 CPU 上限 |
| default.memory | 512Mi | 容器默认内存上限 |
| defaultRequest.cpu | 50m | 容器默认 CPU 请求 |
| defaultRequest.memory | 128Mi | 容器默认内存请求 |
| max.cpu | 1 | 容器最大 CPU |
| max.memory | 2Gi | 容器最大内存 |
| min.cpu | 10m | 容器最小 CPU |
| min.memory | 32Mi | 容器最小内存 |

---

## 环境变量覆盖

可以通过修改 ConfigMap 和 Secret 来覆盖默认配置：

```bash
# 更新 ConfigMap
kubectl edit configmap mood-diary-config -n ai-mood-diary

# 更新 Secret
kubectl edit secret mood-diary-secret -n ai-mood-diary

# 或者使用 kubectl set
kubectl set env deployment/mood-diary-backend ARK_MODEL=arkmind-v3 -n ai-mood-diary
```

---

## 日志查看

```bash
# 查看后端日志
kubectl logs -f deployment/mood-diary-backend -n ai-mood-diary

# 查看前端日志
kubectl logs -f deployment/mood-diary-frontend -n ai-mood-diary

# 查看 MySQL 日志
kubectl logs -f deployment/mood-diary-mysql -n ai-mood-diary
```

---

## 删除部署

```bash
# 删除所有资源
kubectl delete -f k8s/

# 删除命名空间（会删除所有资源）
kubectl delete ns ai-mood-diary
```

---

## 常见问题

### 1. MySQL 数据持久化问题

如果使用 `hostPath` 方式持久化，需要确保节点上 `/mnt/data/mysql` 目录存在且有正确权限：

```bash
# 在每个节点上执行
mkdir -p /mnt/data/mysql
chmod -R 777 /mnt/data/mysql
```

生产环境建议使用云存储服务（如 AWS EBS、阿里云云盘等）。

### 2. Ingress 无法访问

- 确保 Nginx Ingress Controller 已安装
- 检查 Ingress 状态：`kubectl describe ingress mood-diary-ingress -n ai-mood-diary`
- 检查 DNS 是否正确解析到 Ingress Controller 的外部 IP

### 3. 后端连接数据库失败

- 检查 MySQL 是否正常运行：`kubectl get pods -n ai-mood-diary`
- 检查数据库密码是否正确
- 检查网络连通性：在后端 Pod 中 ping MySQL 服务

### 4. HPA 不生效

- 确保集群已安装 Metrics Server：`kubectl get deployment metrics-server -n kube-system`
- 检查 HPA 状态：`kubectl describe hpa mood-diary-backend-hpa -n ai-mood-diary`

---

## 生产环境建议

### 1. 数据库

- 使用云数据库（如 RDS）替代自建 MySQL
- 配置数据库备份策略
- 启用主从复制

### 2. 安全

- 使用 TLS/SSL 证书（Let's Encrypt）
- 限制 Ingress 访问来源
- 使用 NetworkPolicy 限制 Pod 间通信
- 定期轮换 Secret

### 3. 监控

- 部署 Prometheus + Grafana 监控
- 配置告警规则
- 收集日志到 ELK 或 Loki

### 4. CI/CD

- 使用 GitLab CI 或 GitHub Actions 自动构建镜像
- 配置滚动更新策略
- 实现蓝绿部署或金丝雀发布