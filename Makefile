.PHONY: dev
dev:
	pip install -e ".[dev]"
	pre-commit install

.PHONY: format
format:
	isort aiogqlc tests setup.py
	black aiogqlc tests setup.py

.PHONY: lint
lint:
	flake8 aiogqlc tests setup.py
	isort aiogqlc tests setup.py --check-only
	black aiogqlc tests setup.py --check
	mypy aiogqlc

.PHONY: test
test:
	pytest --cov=aiogqlc --cov-report=term-missing --cov-branch -vv tests

.PHONY: tox
tox:
	tox

.PHONY: release
release:
	python3 setup.py sdist bdist_wheel
	twine upload dist/*
