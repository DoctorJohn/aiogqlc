.PHONY: install-dev format lint release

install-dev:
	pip install -e ".[dev]"

format:
	black aiogqlc setup.py

lint:
	flake8 aiogqlc setup.py

release:
	python3 setup.py sdist bdist_wheel
	twine upload dist/*
