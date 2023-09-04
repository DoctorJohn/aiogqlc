.PHONY: dev
dev:
	poetry install
	poetry run pre-commit install

.PHONY: format
format:
	poetry run ruff aiogqlc tests --fix
	poetry run black aiogqlc tests

.PHONY: lint
lint:
	poetry run ruff aiogqlc tests
	poetry run black aiogqlc tests --check
	poetry run mypy aiogqlc

.PHONY: test
test:
	poetry run pytest --cov=aiogqlc --cov-report=term-missing --cov-branch -vv tests
