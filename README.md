## Contilio TransportAPI

[![Test Coverage](https://codecov.io/gh/pointtonull/contilio/branch/main/graph/badge.svg)](https://codecov.io/gh/pointtonull/contilio)
[![GitHub issues](https://img.shields.io/github/issues/pointtonull/contilio)](https://github.com/pointtonull/contilio/issues)
[![GitHub forks](https://img.shields.io/github/forks/pointtonull/contilio)](https://github.com/pointtonull/contilio/network)
[![GitHub stars](https://img.shields.io/github/stars/pointtonull/contilio)](https://github.com/pointtonull/contilio/stargazers)

## Description

Production-ready dockerized async REST API on FastAPI with SQLAlchemy and SQLite.


### After `git clone` run

```bash
just --list
```

## 🛠 Tooling Decisions

### `uv` for Dependency Management

We use [`uv`](https://github.com/astral-sh/uv), a fast and modern Python package manager written in Rust. It replaces `pip`, `pip-tools`, and `poetry` with a single unified workflow that installs and locks dependencies via `pyproject.toml` and `uv.lock`. This improves reproducibility and dramatically reduces installation time in development and CI environments.

### `just` for Task Automation

[`just`](https://github.com/casey/just) is used as a lightweight command runner, similar to `make`, but focused on scripting rather than file-based build automation. It simplifies repetitive developer tasks like building, testing, running migrations, and linting by consolidating them into a single `Justfile`.

### SQLite for Lightweight Local Storage

For local development and testing, we use SQLite via the `aiosqlite` driver. It's fast, requires no setup, and integrates cleanly with SQLAlchemy's async ORM. In CI environments, SQLite is run in-memory to speed up test execution and reduce I/O overhead.

### Docker + Buildx Bake

The project uses Docker with `buildx bake` for efficient, declarative builds. This allows for consistent local and CI builds, reproducible caching, and easy parallelism. The configuration lives in a `docker-bake.hcl` file, and the `Justfile` provides a clean interface to trigger builds and runs.
