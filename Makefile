.PHONY: install lint typecheck test clean build dev up down

install:
	uv sync --group dev

lint:
	ruff check src/ tests/
	ruff format --check src/ tests/

typecheck:
	mypy src/

test:
	pytest tests/ -v --cov=src --cov-report=term-missing

test-ci:
	pytest tests/ -v --cov=src --cov-report=xml --cov-report=term-missing

clean:
	rm -rf .venv/
	rm -rf __pycache__/
	rm -rf .pytest_cache/
	rm -rf .ruff_cache/
	rm -rf .mypy_cache/
	rm -rf htmlcov/
	rm -rf coverage/
	rm -rf dist/
	rm -rf *.egg-info/

build:
	docker compose build

up:
	docker compose up -d

down:
	docker compose down

logs:
	docker compose logs -f

pre-commit:
	pre-commit run --all-files
