.PHONY: dev
dev:
	pip install -e ".[dev]"
	pre-commit install

.PHONY: format
format:
	isort aiogqlc examples tests setup.py
	black aiogqlc examples tests setup.py

.PHONY: lint
lint:
	flake8 aiogqlc examples tests setup.py
	isort aiogqlc examples tests setup.py --check-only
	black aiogqlc examples tests setup.py --check
	mypy aiogqlc

.PHONY: test
test:
	py.test aiogqlc --cov=aiogqlc --cov-report term-missing -vv tests

.PHONY: tox
tox:
	tox

.PHONY: release
release:
	python3 setup.py sdist bdist_wheel
	twine upload dist/*
