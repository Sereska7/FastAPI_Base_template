# Load environment variables
include .env
export

# Define files/folders for formatting and checking
files_to_fmt     ?= app tests
files_to_check   ?= app tests

# Sphinx documentation settings
SPHINX_BUILD     ?= sphinx-build
SPHINX_TEMPLATES ?= ./docs/_templates
SOURCE_DIR       = ./docs
BUILD_DIR        = ./docs/_build

# Default target
.DEFAULT_GOAL := run

# Docker setup
## Build and run API Docker containers
docker_up:
	docker-compose up --build -d

# Run the application
run:
	uvicorn app:create_app --host localhost --reload --port ${API__PORT}

# Documentation tasks
## Build Sphinx documentation
docs: build_docs rst_builder

## Generate .rst files from docstrings
build_docs:
	poetry run sphinx-apidoc -f -o "$(SOURCE_DIR)" . -t="$(SPHINX_TEMPLATES)"

## Build HTML pages from .rst files
rst_builder:
	poetry run $(SPHINX_BUILD) -b html "$(SOURCE_DIR)" "$(BUILD_DIR)"

# Code formatting
## Format all code
fmt: format

format: remove_imports isort black docformatter add_trailing_comma

## Remove unused imports
remove_imports:
	autoflake -ir --remove-unused-variables \
		--ignore-init-module-imports \
		--remove-all-unused-imports \
		${files_to_fmt}

## Sort imports
isort:
	isort ${files_to_fmt}

## Format code with Black
black:
	black ${files_to_fmt}

## Format docstrings to PEP 257 with docformatter
docformatter:
	docformatter -ir ${files_to_fmt}

## Add trailing commas (Unix only)
add_trailing_comma:
	find ${files_to_fmt} -name "*.py" -exec add-trailing-comma '{}' --py36-plus \;

# Code quality checks
## Run all checks
chk: check

check: flake8 pylint ruff black_check docformatter_check safety bandit mypy

## Check Black formatting
black_check:
	black --check ${files_to_check}

## Check docstring formatting
docformatter_check:
	docformatter -cr ${files_to_check}

## Run flake8 for PEP8 compliance
flake8:
	flake8 ${files_to_check}

## Run pylint for Google style checks
pylint:
	pylint ${files_to_check}

## Run ruff for additional linting
ruff:
	ruff ${files_to_check}

## Check typing with mypy
mypy:
	mypy ${files_to_check}

## Check for security vulnerabilities in dependencies
safety:
	safety check --full-report

## Check code security with Bandit
bandit:
	bandit -r ${files_to_check} -x tests

# Database migration
## Run migrations
migrate:
	poetry run python -m scripts.migrate

## Rollback migrations
migrate-rollback:
	poetry run python -m scripts.migrate --rollback

## Reload migrations
migrate-reload:
	poetry run python -m scripts.migrate --reload

migrate-testing:
	poetry run python -m scripts.migrate --testing

## Pre-commit hooks
pre-commit:
	pre-commit run --all-files
