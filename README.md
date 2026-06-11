# url-shortener

A URL shortener with analytics, built in phases as a deep-dive backend project
in Python (FastAPI).

## Structure

```
url-shortener/
├── backend/          # API (FastAPI) + business logic + tests
│   ├── app/
│   │   └── core/     # core utilities (Base62, config, ...)
│   ├── tests/
│   └── pyproject.toml
├── docs/adr/         # Architecture Decision Records
└── README.md
```

## Getting started

Requires Python 3.12+ and [uv](https://docs.astral.sh/uv/).

```bash
cd backend
uv sync          # install dependencies (incl. dev tools)
uv run pytest    # run the test suite
uv run ruff check .   # lint
uv run mypy app tests # type-check
```

## Development tooling

This project uses [ruff](https://docs.astral.sh/ruff/) (linter + formatter) and
[mypy](https://mypy.readthedocs.io/) (static type checker), enforced via
[pre-commit](https://pre-commit.com/):

```bash
uv run pre-commit install        # set up the git hook (once)
uv run pre-commit run --all-files # run all checks manually
```

## Architecture decisions

- [ADR-001: Short code generation strategy](docs/adr/0001-short-code-generation.md)
- [ADR-002: Code assignment strategy](docs/adr/0002-code-assignment.md)