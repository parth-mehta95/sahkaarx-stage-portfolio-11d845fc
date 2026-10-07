.PHONY: help setup lint format test test-conflicts clean train evaluate run-pipeline simulate-conflict

help:
	@echo "Available commands:"
	@echo "  make setup             - Install dependencies and setup environment"
	@echo "  make lint              - Run ruff and black check"
	@echo "  make format            - Auto-format code with black and ruff"
	@echo "  make test              - Run pytest test suite with coverage"
	@echo "  make test-conflicts    - Verify conflict resolution integrity tests"
	@echo "  make train             - Train ML model with active profile"
	@echo "  make evaluate          - Evaluate model against quality & latency gates"
	@echo "  make run-pipeline      - Run end-to-end ML pipeline"
	@echo "  make simulate-conflict - Run automated branch conflict & resolution simulation"
	@echo "  make clean             - Clean cache, checkpoints, and bytecode"

setup:
	python -m pip install --upgrade pip
	pip install -r requirements-dev.txt

lint:
	ruff check src/ tests/
	black --check src/ tests/

format:
	black src/ tests/
	ruff check --fix src/ tests/

test:
	pytest tests/ -v --cov=src --cov-report=term-missing

test-conflicts:
	pytest tests/test_conflict_resolution.py -v

train:
	python -m src.models.train

evaluate:
	python -m src.models.evaluate

run-pipeline:
	python -m src.pipelines.pipeline_runner

simulate-conflict:
	@powershell -ExecutionPolicy Bypass -File ./simulate_conflict.ps1

clean:
	find . -type f -name "*.py[co]" -delete
	find . -type d -name "__pycache__" -delete
	rm -rf .pytest_cache .coverage htmlcov
