# Linting and Type Checking

This project uses `ruff` for linting/formatting and `basedpyright` for type checking.

## Quick Start

### Install Development Dependencies

```bash
uv sync --group dev
```

### Run All Checks

```bash
# Run linter
uv run ruff check .

# Run formatter check
uv run ruff format --check .

# Run type checker
uv run basedpyright
```

### Auto-fix Issues

```bash
# Fix linting issues
uv run ruff check . --fix

# Format code
uv run ruff format .
```

## Pre-commit Hooks

This project uses pre-commit hooks to automatically check and fix issues before commits.

### Install Pre-commit Hooks

```bash
uv run pre-commit install
```

### Run Pre-commit on All Files

```bash
uv run pre-commit run --all-files
```

### Pre-commit Hooks Include:
- **ruff** - Linting with auto-fix
- **ruff-format** - Code formatting
- **basedpyright** - Type checking
- **trailing-whitespace** - Remove trailing whitespace
- **end-of-file-fixer** - Ensure files end with a newline
- **check-yaml** - Validate YAML files
- **check-added-large-files** - Prevent large files from being committed
- **check-merge-conflict** - Detect merge conflict markers
- **detect-private-key** - Prevent committing private keys

## CI/CD Integration

Linting and type checking are enforced in the GitHub Actions CI pipeline. The `lint` job runs before building and will fail the build if any issues are found.

## Configuration

### Ruff Configuration (`pyproject.toml`)

Ruff is configured with:
- Line length: 120 characters
- Target Python version: 3.10+
- Enabled rule sets: pycodestyle, pyflakes, isort, pep8-naming, pyupgrade, flake8-bugbear, flake8-comprehensions, flake8-simplify

### Basedpyright Configuration (`pyproject.toml`)

Basedpyright is configured with:
- Type checking mode: standard
- Relaxed type checking for existing codebase (focuses on imports and unused variables)
- Can be made stricter as the codebase improves

## Editor Integration

### VS Code

Install the following extensions:
- [Ruff](https://marketplace.visualstudio.com/items?itemName=charliermarsh.ruff)
- [BasedPyright](https://marketplace.visualstudio.com/items?itemName=detachhead.basedpyright)

### Other Editors

Most modern editors have plugins for ruff and pyright/basedpyright. Check your editor's extension marketplace.
