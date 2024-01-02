.PHONY: dev
dev:
	poetry install
	poetry run pre-commit install

.PHONY: format
format:
	poetry run ruff check --fix aiogqlc tests
	poetry run ruff format aiogqlc tests

.PHONY: lint
lint:
	poetry run ruff check aiogqlc tests
	poetry run ruff format --check aiogqlc tests
	poetry run mypy aiogqlc tests

.PHONY: test
test:
	poetry run pytest --cov=aiogqlc --cov-report=term-missing --cov-branch -vv tests
