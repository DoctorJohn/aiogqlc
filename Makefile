.PHONY: format
format:
	uv run ruff check --fix aiogqlc tests
	uv run ruff format aiogqlc tests

.PHONY: lint
lint:
	uv run ruff check aiogqlc tests
	uv run ruff format --check aiogqlc tests
	uv run mypy aiogqlc tests

.PHONY: test
test:
	uv run pytest
