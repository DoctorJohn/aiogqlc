.PHONY: install-dev format lint release

install-dev:
	pip install -e ".[dev]"
	pre-commit install

format:
	black aiogqlc examples setup.py

lint:
	flake8 aiogqlc examples setup.py

release:
	python3 setup.py sdist bdist_wheel
	twine upload dist/*
