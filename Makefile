.PHONY: dev
dev:
	poetry install
	poetry run pre-commit install

.PHONY: format
format:
	poetry run isort aiogqlc tests
	poetry run black aiogqlc tests

.PHONY: lint
lint:
	poetry run flake8 aiogqlc tests
	poetry run isort aiogqlc tests --check-only
	poetry run black aiogqlc tests --check
	poetry run mypy aiogqlc

.PHONY: test
test:
	poetry run pytest --cov=aiogqlc --cov-report=term-missing --cov-branch -vv tests

.PHONY: tox
tox:
	poetry run tox
