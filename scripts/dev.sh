#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
BACKEND_DIR="${ROOT_DIR}/backend"
FRONTEND_DIR="${ROOT_DIR}/frontend"
VENV_DIR="${BACKEND_DIR}/.venv"
BACKEND_HOST="127.0.0.1"
BACKEND_PORT="8000"

COLOR_RESET="\033[0m"
COLOR_GREEN="\033[32m"
COLOR_YELLOW="\033[33m"
COLOR_BLUE="\033[34m"
COLOR_RED="\033[31m"
BACKEND_PID=""
FRONTEND_PID=""

log_info()    { echo -e "${COLOR_BLUE}[INFO]${COLOR_RESET}  $1"; }
log_success() { echo -e "${COLOR_GREEN}[OK]${COLOR_RESET}    $1"; }
log_warn()    { echo -e "${COLOR_YELLOW}[WARN]${COLOR_RESET}  $1"; }
log_error()   { echo -e "${COLOR_RED}[ERROR]${COLOR_RESET} $1"; }

cmd_exists() { command -v "$1" >/dev/null 2>&1; }

require_cmd() {
    if ! cmd_exists "$1"; then
        log_error "缺少必需命令: $1，请先安装后再运行本脚本。"
        exit 1
    fi
}

run_with_retry() {
    local max_retries="$1"; shift
    local desc="$1"; shift
    local retry=0
    while [ "${retry}" -le "${max_retries}" ]; do
        if "$@"; then
            return 0
        fi
        retry=$((retry + 1))
        if [ "${retry}" -le "${max_retries}" ]; then
            log_warn "${desc} 失败 (${retry}/${max_retries})，2 秒后重试..."
            sleep 2
        fi
    done
    log_error "${desc} 在 ${max_retries} 次尝试后仍失败。"
    return 1
}

venv_valid() {
    [ -d "${VENV_DIR}" ] || return 1
    [ -x "${VENV_DIR}/bin/python" ] || return 1
    [ -x "${VENV_DIR}/bin/pip" ] || return 1
    "${VENV_DIR}/bin/python" --version >/dev/null 2>&1 || return 1
    "${VENV_DIR}/bin/pip" --version >/dev/null 2>&1 || return 1
    return 0
}

rebuild_venv() {
    log_warn "虚拟环境无效或损坏，正在清理并重建..."
    if [ -d "${VENV_DIR}" ]; then
        rm -rf "${VENV_DIR}"
    fi
    log_info "创建新的 Python 虚拟环境..."
    python3 -m venv "${VENV_DIR}"
    log_success "虚拟环境已重建"
}

ensure_venv() {
    require_cmd python3
    if ! venv_valid; then
        rebuild_venv
    fi
    PYTHON="${VENV_DIR}/bin/python"
    PIP="${VENV_DIR}/bin/pip"
}

pip_install_with_fallback() {
    local tag="$1"; shift
    if run_with_retry 2 "${tag} (官方源)" "${PIP}" install "$@"; then
        return 0
    fi
    log_warn "官方源安装失败，尝试国内镜像源（不修改全局配置）..."
    if run_with_retry 2 "${tag} (清华镜像)" \
        "${PIP}" install -i https://pypi.tuna.tsinghua.edu.cn/simple "$@"; then
        return 0
    fi
    if run_with_retry 1 "${tag} (阿里镜像)" \
        "${PIP}" install -i https://mirrors.aliyun.com/pypi/simple/ "$@"; then
        return 0
    fi
    return 1
}

step_backend_deps() {
    ensure_venv
    log_info "检查并安装后端 Python 依赖..."
    if ! pip_install_with_fallback "升级 pip" --upgrade pip; then
        log_warn "pip 升级失败，继续使用当前版本..."
    fi
    pip_install_with_fallback "安装后端依赖" -r "${BACKEND_DIR}/requirements.txt"
    if ! "${PYTHON}" -c "import django; import rest_framework; import corsheaders" >/dev/null 2>&1; then
        log_warn "依赖校验未通过，重建虚拟环境后重试..."
        rebuild_venv
        ensure_venv
        pip_install_with_fallback "重装后端依赖" -r "${BACKEND_DIR}/requirements.txt"
    fi
    log_success "后端依赖已就绪"
}

step_migrate() {
    ensure_venv
    log_info "执行数据库迁移..."
    cd "${BACKEND_DIR}"
    run_with_retry 2 "执行数据库迁移" \
        "${PYTHON}" manage.py makemigrations --check --dry-run >/dev/null 2>&1 || true
    run_with_retry 2 "执行数据库迁移" \
        "${PYTHON}" manage.py migrate --noinput
    log_success "数据库迁移完成"
}

step_seed_demo() {
    ensure_venv
    log_info "填充演示数据（已存在的数据会自动跳过）..."
    cd "${BACKEND_DIR}"
    run_with_retry 1 "填充演示数据" \
        "${PYTHON}" manage.py seed_demo
    log_success "演示数据处理完成"
}

step_backend_check() {
    log_info "检查后端服务健康状态..."
    local max_retries=5
    local retry=0
    local url="http://${BACKEND_HOST}:${BACKEND_PORT}/api/health/"

    while [ "${retry}" -lt "${max_retries}" ]; do
        if cmd_exists curl; then
            local response
            response=$(curl -s -o /dev/null -w "%{http_code}" "${url}" 2>/dev/null || true)
            if [ "${response}" = "200" ]; then
                log_success "后端服务健康检查通过: ${url}"
                return 0
            fi
        else
            ensure_venv
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

npm_install_with_fallback() {
    local tag="$1"; shift
    if run_with_retry 2 "${tag} (当前源)" npm install "$@"; then
        return 0
    fi
    log_warn "安装失败，尝试切换至国内镜像源（不修改全局配置）..."
    if run_with_retry 2 "${tag} (npmmirror)" npm install --registry=https://registry.npmmirror.com "$@"; then
        return 0
    fi
    if run_with_retry 1 "${tag} (taobao)" npm install --registry=https://registry.npm.taobao.org "$@"; then
        return 0
    fi
    return 1
}

step_frontend_deps() {
    require_cmd node
    require_cmd npm
    log_info "检查并安装前端依赖..."
    cd "${FRONTEND_DIR}"
    if [ ! -d "node_modules" ] || [ "package.json" -nt "node_modules" ]; then
        if [ -d "node_modules" ]; then
            log_warn "package.json 已更新，清理旧 node_modules..."
            rm -rf node_modules package-lock.json 2>/dev/null || true
        fi
        npm_install_with_fallback "安装前端依赖"
        log_success "前端依赖安装完成"
    else
        if ! npm ls --depth=0 >/dev/null 2>&1; then
            log_warn "node_modules 完整性校验失败，重新安装..."
            rm -rf node_modules package-lock.json 2>/dev/null || true
            npm_install_with_fallback "重装前端依赖"
            log_success "前端依赖已重装"
        else
            log_success "前端依赖已是最新"
        fi
    fi
}

step_frontend_build() {
    require_cmd node
    require_cmd npm
    step_frontend_deps
    log_info "构建前端项目..."
    cd "${FRONTEND_DIR}"
    if [ -d "dist" ]; then
        rm -rf dist
    fi
    run_with_retry 2 "前端构建" npm run build
    log_success "前端构建完成"
}

start_backend() {
    ensure_venv
    log_info "启动后端开发服务器..."
    cd "${BACKEND_DIR}"
    "${PYTHON}" manage.py runserver "${BACKEND_HOST}:${BACKEND_PORT}" &
    BACKEND_PID=$!
    log_info "后端 PID: ${BACKEND_PID}"
    sleep 3
    if ! kill -0 "${BACKEND_PID}" 2>/dev/null; then
        log_error "后端服务启动失败，查看上方日志排错。"
        return 1
    fi
}

start_frontend() {
    require_cmd node
    require_cmd npm
    log_info "启动前端开发服务器..."
    cd "${FRONTEND_DIR}"
    npm run dev -- --host "${BACKEND_HOST}" --port 5173 &
    FRONTEND_PID=$!
    log_info "前端 PID: ${FRONTEND_PID}"
    sleep 2
    if ! kill -0 "${FRONTEND_PID}" 2>/dev/null; then
        log_error "前端服务启动失败，查看上方日志排错。"
        return 1
    fi
}

cleanup() {
    log_info "正在停止服务..."
    if [ -n "${BACKEND_PID}" ] && kill -0 "${BACKEND_PID}" 2>/dev/null; then
        kill "${BACKEND_PID}" 2>/dev/null || true
        wait "${BACKEND_PID}" 2>/dev/null || true
    fi
    if [ -n "${FRONTEND_PID}" ] && kill -0 "${FRONTEND_PID}" 2>/dev/null; then
        kill "${FRONTEND_PID}" 2>/dev/null || true
        wait "${FRONTEND_PID}" 2>/dev/null || true
    fi
    log_info "服务已停止"
    exit 0
}

trap cleanup INT TERM

usage() {
    cat <<EOF
Usage: $(basename "$0") <command>

Commands:
  setup     完整初始化：安装依赖、迁移、填充演示数据、前端构建
  deps      仅安装后端和前端依赖
  migrate   仅执行数据库迁移
  seed      仅填充演示数据（已存在数据会自动跳过）
  build     仅构建前端
  check     检查后端服务健康状态
  start     启动前后端开发服务器（前台运行）
  all       setup + start，一键启动完整开发环境
  help      显示此帮助信息
EOF
}

PYTHON="${VENV_DIR}/bin/python"
PIP="${VENV_DIR}/bin/pip"

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
        step_frontend_build
        ;;
    check)
        step_backend_check
        ;;
    start)
        start_backend || exit 1
        step_backend_check || exit 1
        start_frontend || exit 1
        log_success "开发环境已启动"
        log_info "前端:            http://127.0.0.1:5173"
        log_info "后端健康检查:    http://127.0.0.1:8000/api/health/"
        log_info "Django Admin:    http://127.0.0.1:8000/admin/"
        log_info "按 Ctrl+C 停止服务"
        wait
        ;;
    all)
        step_backend_deps
        step_migrate
        step_seed_demo
        step_frontend_deps
        step_frontend_build
        start_backend || exit 1
        step_backend_check || exit 1
        start_frontend || exit 1
        log_success "开发环境已启动"
        log_info "前端:            http://127.0.0.1:5173"
        log_info "后端健康检查:    http://127.0.0.1:8000/api/health/"
        log_info "Django Admin:    http://127.0.0.1:8000/admin/"
        log_info "按 Ctrl+C 停止服务"
        wait
        ;;
    help|*)
        usage
        ;;
esac
