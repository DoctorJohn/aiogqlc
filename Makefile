.PHONY: doc format install-dev lint release

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

doc:
	rm -rf docs/
	pdoc \
        --config 'git_link_template="https://github.com/DoctorJohn/aiogqlc/blob/master/{path}#L{start_line}-L{end_line}"' \
        --config 'sort_identifiers=False' \
        --force \
        --html \
        --output-dir docs/ \
        aiogqlc
	mv docs/aiogqlc/* docs/
