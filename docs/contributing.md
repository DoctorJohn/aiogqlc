# Contributing

## Setup

1. Clone the repository
2. Make sure you have [uv](https://github.com/astral-sh/uv) installed
3. Install project dependencies with `uv sync`

## Linting

- Run `make format` to format the code.
- Run `make lint` to lint the code.

If you don't have make installed, take a look at the `Makefile` and run it's commands manually.

### pre-commit

If you want to run the linter automatically on every commit, you can install the pre-commit hooks by running:

```bash
uv run pre-commit install
```

## Testing

Run `make test` to run all tests in your local environment.

## Documentation

Preview the documentation website locally by running `uv run mkdocs serve`.
