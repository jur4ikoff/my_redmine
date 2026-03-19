# ==============================================================================
# Makefile для Python-проекта (FastAPI + Poetry + Ruff + mypy)
# ==============================================================================

# Переменные
PYTHON := python3
POETRY := poetry
RUFF := $(POETRY) run ruff
MYPY := $(POETRY) run mypy
PYTEST := $(POETRY) run pytest
UVICORN := $(POETRY) run uvicorn

# Пути
SRC_DIR := control-project-system
TEST_DIR := tests
APP_MODULE := src.main:app  # Замените на ваш путь к FastAPI app

# Цвета для вывода (опционально)
GREEN := \033[0;32m
YELLOW := \033[0;33m
RED := \033[0;31m
NC := \033[0m

.PHONY: help
help:  ## 📋 Показать справку по доступным командам
	@echo "$(GREEN)Доступные команды:$(NC)"
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | \
		awk 'BEGIN {FS = ":.*?## "}; {printf "  $(YELLOW)%-20s$(NC) %s\n", $$1, $$2}'

# ==============================================================================
# Установка и окружение
# ==============================================================================

.PHONY: install
install:  ## 📦 Установить зависимости через Poetry
	@echo "$(GREEN)→ Установка зависимостей...$(NC)"
	$(POETRY) install
	@echo "$(GREEN)✓ Готово!$(NC)"

.PHONY: install-dev
install-dev:  ## 📦 Установить зависимости + dev-зависимости
	@echo "$(GREEN)→ Установка всех зависимостей...$(NC)"
	$(POETRY) install --with dev
	@echo "$(GREEN)✓ Готово!$(NC)"

.PHONY: up
up:  ## 🚀 Запустить FastAPI приложение (uvicorn)
	@echo "$(GREEN)→ Запуск сервера на http://localhost:8000$(NC)"
	$(UVICORN) $(APP_MODULE) --reload --host 0.0.0.0 --port 8000

.PHONY: up-prod
up-prod:  ## 🚀 Запустить в продакшн-режиме (без reload)
	@echo "$(GREEN)→ Запуск сервера (production)$(NC)"
	$(UVICORN) $(APP_MODULE) --host 0.0.0.0 --port 8000

# ==============================================================================
# Форматирование и линтинг
# ==============================================================================

.PHONY: format
format:  ## ✨ Отформатировать код (Ruff format + isort)
	@echo "$(GREEN)→ Форматирование кода...$(NC)"
	$(RUFF) format $(SRC_DIR) $(TEST_DIR)
	@echo "$(GREEN)✓ Код отформатирован!$(NC)"

.PHONY: lint
lint:  ## 🔍 Проверить код на ошибки (Ruff check, без автофикса)
	@echo "$(GREEN)→ Запуск линтера...$(NC)"
	$(RUFF) check $(SRC_DIR) $(TEST_DIR)
	@echo "$(GREEN)✓ Линтинг завершён$(NC)"

.PHONY: lint-fix
lint-fix:  ## 🔧 Проверить и автоматически исправить ошибки (Ruff --fix)
	@echo "$(GREEN)→ Проверка и автоисправление...$(NC)"
	$(RUFF) check --fix $(SRC_DIR) $(TEST_DIR)
	@echo "$(GREEN)✓ Исправления применены!$(NC)"

.PHONY: type-check
type-check:  ## 🔎 Проверка типов (mypy)
	@echo "$(GREEN)→ Запуск mypy...$(NC)"
	$(MYPY) $(SRC_DIR)
	@echo "$(GREEN)✓ Проверка типов завершена$(NC)"

# ==============================================================================
# Комплексные проверки
# ==============================================================================

.PHONY: check
check: lint type-check  ## ✅ Запустить все проверки (lint + mypy)
	@echo "$(GREEN)✓ Все проверки пройдены!$(NC)"

.PHONY: check-all
check-all: lint-fix format type-check  ## 🔄 Форматировать + исправить + проверить типы
	@echo "$(GREEN)✓ Полный цикл проверок завершён!$(NC)"

# ==============================================================================
# Тесты
# ==============================================================================

.PHONY: test
test:  ## 🧪 Запустить тесты (pytest)
	@echo "$(GREEN)→ Запуск тестов...$(NC)"
	$(PYTEST) $(TEST_DIR) -v

.PHONY: test-cov
test-cov:  ## 📊 Запустить тесты с отчётом о покрытии
	@echo "$(GREEN)→ Запуск тестов с coverage...$(NC)"
	$(PYTEST) $(TEST_DIR) --cov=$(SRC_DIR) --cov-report=html --cov-report=term
	@echo "$(GREEN)✓ Отчёт о покрытии: htmlcov/index.html$(NC)"

.PHONY: test-fast
test-fast:  ## ⚡ Запустить тесты быстро (без coverage, с xdist)
	@echo "$(GREEN)→ Быстрый запуск тестов...$(NC)"
	$(PYTEST) $(TEST_DIR) -n auto -q

# ==============================================================================
# Очистка
# ==============================================================================

.PHONY: clean
clean:  ## 🧹 Удалить артефакты (__pycache__, .pytest_cache, и т.д.)
	@echo "$(YELLOW)→ Очистка проекта...$(NC)"
	find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name "*.pyc" -delete 2>/dev/null || true
	find . -type f -name "*.pyo" -delete 2>/dev/null || true
	find . -type f -name "*.pyd" -delete 2>/dev/null || true
	rm -rf .pytest_cache .mypy_cache htmlcov .ruff_cache 2>/dev/null || true
	rm -rf dist build *.egg-info 2>/dev/null || true
	@echo "$(GREEN)✓ Очистка завершена$(NC)"

.PHONY: clean-venv
clean-venv:  ## 🗑️ Удалить виртуальное окружение Poetry
	@echo "$(RED)→ Удаление виртуального окружения...$(NC)"
	$(POETRY) env remove python
	@echo "$(GREEN)✓ Окружение удалено$(NC)"

# ==============================================================================
# CI/CD и пре-коммит
# ==============================================================================

.PHONY: pre-commit
pre-commit: check-all test  ## 🔒 Запустить все проверки перед коммитом
	@echo "$(GREEN)✓ Pre-commit проверки пройдены!$(NC)"

.PHONY: ci
ci: clean install-dev check-all test-cov  ## 🤖 Полный цикл для CI/CD
	@echo "$(GREEN)✓ CI pipeline завершён успешно!$(NC)"

# ==============================================================================
# Документация (опционально)
# ==============================================================================

.PHONY: docs
docs:  ## 📚 Сгенерировать документацию (если используете mkdocs/sphinx)
	@echo "$(YELLOW)⚠️  Документация не настроена$(NC)"
	# Раскомментируйте и настройте под ваш инструмент:
	# $(POETRY) run mkdocs build
	# $(POETRY) run sphinx-build -b html docs/ docs/_build

# ==============================================================================
# По умолчанию
# ==============================================================================

.DEFAULT_GOAL := help