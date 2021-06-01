.PHONY: dev
dev:
	pip install -e ".[dev]"
	pre-commit install

.PHONY: format
format:
	black aiogqlc examples setup.py

.PHONY: lint
lint:
	flake8 aiogqlc examples setup.py

.PHONY: test
test:
	py.test aiogqlc --cov=aiogqlc --cov-report term-missing -vv

.PHONY: tox
tox:
	tox

.PHONY: release
release:
	python3 setup.py sdist bdist_wheel
	twine upload dist/*
