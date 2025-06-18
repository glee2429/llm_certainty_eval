# Makefile for linting and formatting

.PHONY: lint lint-flake8 lint-pylint lint-mypy format

# Run all linters
lint: lint-flake8 lint-pylint lint-mypy

# Run Flake8
lint-flake8:
	@echo "Running Flake8..."
	poetry run flake8 llm_reflection

# Run Pylint
lint-pylint:
	@echo "Running Pylint..."
	poetry run pylint llm_reflection

# Run MyPy
lint-mypy:
	@echo "Running MyPy..."
	poetry run mypy llm_reflection

# Format code with Black
format:
	@echo "Running Black..."
	poetry run black llm_reflection
