# 快递柜管理系统

基于 Django REST Framework + React + Vite 的快递柜管理系统，覆盖快件入库通知、取件码开箱、柜格状态监控、退件处理等核心流程。

## 功能模块

- 快件入库：登记运单、自动分配空柜格、生成取件码、写入通知记录。
- 取件开箱：输入取件码校验快件，更新快件状态并将柜格标记为已开门。
- 柜格监控：查看柜格空闲、占用、开门、维护状态，支持释放柜格和标记维护。
- 退件处理：对在柜快件创建退件单，完成退件后释放柜格。
- 通知记录：查看入库后生成的短信/App/微信通知记录。

## 项目结构

```text
backend/
  apps/
    lockers/        # 柜格模型、状态接口、演示数据命令
    parcels/        # 快件入库、取件码开箱
    notifications/  # 入库通知记录
    returns/        # 退件单处理
  config/           # Django 配置和路由
frontend/
  src/
    api/            # API 客户端与模块封装
    components/     # 通用表格、状态标签、指标卡
    layouts/        # 应用布局和导航
    pages/          # 各业务页面
docker-compose.yml
```

## Docker 启动

```bash
docker compose up --build
```

启动后访问：

- 前端：http://localhost:5173
- 后端健康检查：http://localhost:8000/api/health/
- Django Admin：http://localhost:8000/admin/

容器启动时会自动执行数据库迁移和 `seed_demo`，生成演示柜格、快件和通知数据。

## 本地开发启动（推荐：统一命令）

项目提供 `Makefile` 和 `scripts/dev.sh` 两种方式，一键完成依赖安装、数据库迁移、演示数据填充、健康检查和前端构建。

### 方式一：Make（推荐）

在项目根目录执行：

```bash
make all
```

其他可用命令：

```bash
make setup     # 初始化：安装依赖、迁移、填充演示数据、前端构建
make deps      # 仅安装后端和前端依赖
make migrate   # 仅执行数据库迁移
make seed      # 仅填充演示数据
make build     # 仅构建前端项目
make check     # 检查后端服务健康状态
make start     # 启动前后端开发服务器
make help      # 查看所有命令
```

### 方式二：Shell 脚本

```bash
./scripts/dev.sh all      # 一键初始化并启动
./scripts/dev.sh setup    # 仅执行初始化
./scripts/dev.sh start    # 仅启动开发服务器
./scripts/dev.sh help     # 查看所有命令
```

启动后访问：

- 前端：http://127.0.0.1:5173
- 后端健康检查：http://127.0.0.1:8000/api/health/
- Django Admin：http://127.0.0.1:8000/admin/

按 `Ctrl+C` 可同时停止前后端服务。

## 本地开发启动（手动方式）

后端：

```bash
cd backend
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python manage.py migrate
python manage.py seed_demo
python manage.py runserver 127.0.0.1:8000
```

前端（另开一个终端）：

```bash
cd frontend
npm install
npm run dev -- --host 127.0.0.1 --port 5173
```

## 主要 API

- `GET /api/lockers/cells/`：柜格列表
- `GET /api/lockers/cells/summary/`：柜格状态汇总
- `POST /api/parcels/inbound/`：快件入库
- `POST /api/parcels/open/`：取件码开箱
- `GET /api/notifications/`：通知记录
- `POST /api/returns/`：创建退件单
- `POST /api/returns/{id}/complete/`：完成退件
