.PHONY: help setup deps migrate seed build check start all

DEV_SCRIPT := ./scripts/dev.sh

help:
	@echo "快递柜管理系统 - 开发环境命令"
	@echo ""
	@echo "Usage:"
	@echo "  make setup     初始化：安装依赖、迁移、填充演示数据、前端构建"
	@echo "  make deps      安装后端和前端依赖"
	@echo "  make migrate   执行数据库迁移"
	@echo "  make seed      填充演示数据"
	@echo "  make build     构建前端项目"
	@echo "  make check     检查后端服务健康状态"
	@echo "  make start     启动前后端开发服务器"
	@echo "  make all       一键初始化并启动完整开发环境"

setup:
	@$(DEV_SCRIPT) setup

deps:
	@$(DEV_SCRIPT) deps

migrate:
	@$(DEV_SCRIPT) migrate

seed:
	@$(DEV_SCRIPT) seed

build:
	@$(DEV_SCRIPT) build

check:
	@$(DEV_SCRIPT) check

start:
	@$(DEV_SCRIPT) start

all:
	@$(DEV_SCRIPT) all
