#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
BACKEND_DIR="${ROOT_DIR}/backend"
FRONTEND_DIR="${ROOT_DIR}/frontend"
VENV_DIR="${BACKEND_DIR}/.venv"
PYTHON="${VENV_DIR}/bin/python"
PIP="${VENV_DIR}/bin/pip"
BACKEND_HOST="127.0.0.1"
BACKEND_PORT="8000"

COLOR_RESET="\033[0m"
COLOR_GREEN="\033[32m"
COLOR_YELLOW="\033[33m"
COLOR_BLUE="\033[34m"
COLOR_RED="\033[31m"

log_info() {
    echo -e "${COLOR_BLUE}[INFO]${COLOR_RESET} $1"
}

log_success() {
    echo -e "${COLOR_GREEN}[OK]${COLOR_RESET} $1"
}

log_warn() {
    echo -e "${COLOR_YELLOW}[WARN]${COLOR_RESET} $1"
}

log_error() {
    echo -e "${COLOR_RED}[ERROR]${COLOR_RESET} $1"
}

step_backend_deps() {
    log_info "检查后端 Python 虚拟环境..."
    if [ ! -d "${VENV_DIR}" ]; then
        log_info "创建虚拟环境..."
        python3 -m venv "${VENV_DIR}"
        log_success "虚拟环境已创建"
    fi

    log_info "安装/更新后端依赖..."
    "${PIP}" install --upgrade pip >/dev/null
    "${PIP}" install -r "${BACKEND_DIR}/requirements.txt"
    log_success "后端依赖安装完成"
}

step_migrate() {
    log_info "执行数据库迁移..."
    cd "${BACKEND_DIR}"
    "${PYTHON}" manage.py migrate --noinput
    log_success "数据库迁移完成"
}

step_seed_demo() {
    log_info "填充演示数据..."
    cd "${BACKEND_DIR}"
    "${PYTHON}" manage.py seed_demo
    log_success "演示数据填充完成"
}

step_backend_check() {
    log_info "检查后端服务健康状态..."
    local max_retries=5
    local retry=0
    local url="http://${BACKEND_HOST}:${BACKEND_PORT}/api/health/"

    while [ ${retry} -lt ${max_retries} ]; do
        if command -v curl >/dev/null 2>&1; then
            local response
            response=$(curl -s -o /dev/null -w "%{http_code}" "${url}" 2>/dev/null || true)
            if [ "${response}" = "200" ]; then
                log_success "后端服务健康检查通过: ${url}"
                return 0
            fi
        elif command -v python3 >/dev/null 2>&1; then
            if "${PYTHON}" -c "
import urllib.request, sys
try:
    r = urllib.request.urlopen('${url}', timeout=3)
    sys.exit(0 if r.status == 200 else 1)
except Exception:
    sys.exit(1)
" 2>/dev/null; then
                log_success "后端服务健康检查通过: ${url}"
                return 0
            fi
        fi
        retry=$((retry + 1))
        log_warn "后端尚未就绪 (${retry}/${max_retries})，等待 2 秒..."
        sleep 2
    done

    log_error "后端健康检查失败，请确认服务是否在 ${BACKEND_HOST}:${BACKEND_PORT} 运行"
    return 1
}

step_frontend_deps() {
    log_info "检查并安装前端依赖..."
    cd "${FRONTEND_DIR}"
    if [ ! -d "node_modules" ] || [ "package.json" -nt "node_modules" ]; then
        npm install
        log_success "前端依赖安装完成"
    else
        log_success "前端依赖已是最新"
    fi
}

step_frontend_build() {
    log_info "构建前端项目..."
    cd "${FRONTEND_DIR}"
    npm run build
    log_success "前端构建完成"
}

start_backend() {
    log_info "启动后端开发服务器..."
    cd "${BACKEND_DIR}"
    "${PYTHON}" manage.py runserver "${BACKEND_HOST}:${BACKEND_PORT}" &
    BACKEND_PID=$!
    log_info "后端 PID: ${BACKEND_PID}"
    sleep 3
}

start_frontend() {
    log_info "启动前端开发服务器..."
    cd "${FRONTEND_DIR}"
    npm run dev -- --host "${BACKEND_HOST}" --port 5173 &
    FRONTEND_PID=$!
    log_info "前端 PID: ${FRONTEND_PID}"
}

cleanup() {
    log_info "正在停止服务..."
    if [ -n "${BACKEND_PID:-}" ] && kill -0 "${BACKEND_PID}" 2>/dev/null; then
        kill "${BACKEND_PID}" 2>/dev/null || true
    fi
    if [ -n "${FRONTEND_PID:-}" ] && kill -0 "${FRONTEND_PID}" 2>/dev/null; then
        kill "${FRONTEND_PID}" 2>/dev/null || true
    fi
    log_info "服务已停止"
    exit 0
}

trap cleanup INT TERM

usage() {
    cat <<EOF
Usage: $(basename "$0") <command>

Commands:
  setup     执行完整初始化：安装依赖、迁移、填充演示数据、前端构建
  deps      仅安装后端和前端依赖
  migrate   仅执行数据库迁移
  seed      仅填充演示数据
  build     仅构建前端
  check     检查后端服务健康状态
  start     启动前后端开发服务器（前台运行）
  all       setup + start（一键启动完整开发环境）
  help      显示此帮助信息
EOF
}

cmd="${1:-help}"

case "${cmd}" in
    setup)
        step_backend_deps
        step_migrate
        step_seed_demo
        step_frontend_deps
        step_frontend_build
        log_success "初始化完成！使用 '$0 start' 启动开发服务器"
        ;;
    deps)
        step_backend_deps
        step_frontend_deps
        ;;
    migrate)
        step_backend_deps
        step_migrate
        ;;
    seed)
        step_backend_deps
        step_migrate
        step_seed_demo
        ;;
    build)
        step_frontend_deps
        step_frontend_build
        ;;
    check)
        step_backend_check
        ;;
    start)
        step_backend_check || true
        start_backend
        step_backend_check
        start_frontend
        log_success "开发环境已启动"
        log_info "前端: http://127.0.0.1:5173"
        log_info "后端: http://127.0.0.1:8000/api/health/"
        log_info "按 Ctrl+C 停止服务"
        wait
        ;;
    all)
        step_backend_deps
        step_migrate
        step_seed_demo
        step_frontend_deps
        step_frontend_build
        start_backend
        step_backend_check
        start_frontend
        log_success "开发环境已启动"
        log_info "前端: http://127.0.0.1:5173"
        log_info "后端: http://127.0.0.1:8000/api/health/"
        log_info "按 Ctrl+C 停止服务"
        wait
        ;;
    help|*)
        usage
        ;;
esac
