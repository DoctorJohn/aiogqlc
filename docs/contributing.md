# Contributing

## Setup

1. Clone the repo
2. Create and enter a dedicated virtual environment
3. Install dependencies and the project editable: `pip install -e ".[dev]"`

## Linting

- Run `make format` to format the code.
- Run `make lint` to lint the code.

If you don't have make installed, take a look at the `Makefile` and run it's commands manually.

## Testing

- Run `pytest tests` to run all tests in your local environment.
- Run `tox` to run all tests against all supported Python versions.
