.PHONY: install-dev format lint release

install-dev:
	pip install -e ".[dev]"
	pre-commit install

format:
	black aiogqlc examples setup.py

lint:
	flake8 aiogqlc examples setup.py

test:
	py.test aiogqlc --cov=aiogqlc -vv

test-with-tox:
	tox

release:
	python3 setup.py sdist bdist_wheel
	twine upload dist/*
