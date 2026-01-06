# Contributing to Lumos CLI

Thank you for your interest in contributing to the Lumos CLI! This document provides guidelines and instructions for contributors and maintainers.

## Development Setup

### Prerequisites

- Python 3.10.6 or higher
- [uv](https://github.com/astral-sh/uv) (recommended) or pip

### Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/teamlumos/lumos-cli.git
   cd lumos-cli
   ```

2. Install dependencies with uv:

   ```bash
   uv sync --group dev --group docs
   ```

3. Set up pre-commit hooks:

   ```bash
   uv run pre-commit install
   ```

### Running the CLI Locally

Create an alias for development:

```bash
alias lumosdev='uv run python -m lumos'
```

Or run directly:

```bash
uv run python -m lumos --help
```

## Project Structure

```
lumos-cli/
├── src/lumos/           # Main source code
│   ├── __init__.py
│   ├── __main__.py          # Entry point for `python -m lumos`
│   ├── cli.py               # Main CLI group and core commands
│   ├── common/              # Shared utilities
│   │   ├── client.py        # API client
│   │   ├── client_helpers.py
│   │   ├── helpers.py       # Authentication helpers
│   │   ├── keyhelpers.py    # Credential storage
│   │   ├── logging.py       # Debug logging
│   │   └── models.py        # Pydantic models
│   ├── list_collections/    # `lumos list` subcommands
│   │   └── cli.py
│   └── request/             # `lumos request` subcommands
│       └── cli.py
├── tests/                   # Test files
├── docs/                    # Sphinx documentation (auto-generated)
├── sample-scripts/          # Example scripts for users
├── pyproject.toml           # Project configuration
├── .releaserc.yaml          # Semantic release configuration
└── .github/workflows/       # CI/CD workflows
```

## Development Workflow

### Creating a Branch

1. Create a feature branch from `main`:

   ```bash
   git checkout -b feat/your-feature-name
   ```

2. Follow [Angular commit conventions](https://www.conventionalcommits.org/):
   - `feat:` - New features
   - `fix:` - Bug fixes
   - `docs:` - Documentation changes
   - `refactor:` - Code refactoring
   - `test:` - Adding or updating tests
   - `chore:` - Maintenance tasks

### Adding a New Command

1. Create a new module in the appropriate directory (e.g., `src/lumos/your_feature/cli.py`)

2. Define your click command:

   ```python
   from click_extra import command, option
   from lumos.common.helpers import authenticate

   @command("your-command", help="Description of your command")
   @option("--flag", is_flag=True, help="Option description")
   @authenticate
   def your_command(flag: bool) -> None:
       """Your command implementation."""
       pass
   ```

3. Register the command in `src/lumos/cli.py`:

   ```python
   def register_subcommands():
       from lumos.your_feature.cli import your_command
       cli.add_command(your_command)
   ```

4. Add tests in `tests/`

5. Update documentation in `docs/`

## Code Style

We use [ruff](https://github.com/astral-sh/ruff) for linting and formatting, and [basedpyright](https://github.com/DetachHead/basedpyright) for type checking.

### Running Linters

```bash
# Run all checks
uv run ruff check .
uv run ruff format --check .
uv run basedpyright

# Auto-fix issues
uv run ruff check --fix .
uv run ruff format .
```

### Style Guidelines

- Maximum line length: 120 characters
- Use double quotes for strings
- Use type hints for all function parameters and return values
- Follow PEP 8 naming conventions

## Testing

### Running Tests

```bash
uv run pytest
```

### Running Tests with Coverage

```bash
uv run pytest --cov=lumos --cov-report=html
```

### Writing Tests

- Place test files in the `tests/` directory
- Name test files with `_test.py` suffix
- Use descriptive test function names: `test_command_does_expected_behavior`

## Documentation

Documentation is built using [Sphinx](https://www.sphinx-doc.org/) with [MyST Markdown](https://myst-parser.readthedocs.io/) and [click-extra's Sphinx extension](https://kdeldycke.github.io/click-extra/sphinx.html) for interactive CLI documentation with ANSI color support.

### Building Documentation Locally

```bash
# Install docs dependencies
uv sync --group docs

# Build both HTML and Markdown, copy markdown to docs/
make -C docs docs

# Or build individually:
make -C docs html      # HTML only
make -C docs markdown  # Markdown only

# View the HTML docs
open docs/sphinx/_build/html/index.html
```

### Documentation Structure

Source files (in `docs/sphinx/`):
- `docs/sphinx/index.md` - Main landing page
- `docs/sphinx/installation.md` - Installation instructions
- `docs/sphinx/examples.md` - Usage examples with code samples
- `docs/sphinx/cli-reference.md` - CLI reference with live examples (via click-extra sphinx)

Generated output:
- `docs/sphinx/_build/html/` - HTML documentation (deployed to GitHub Pages via semantic-release)
- `docs/*.md` - Markdown documentation (copied from build, committed during releases)

### Using click-extra Sphinx Directives

The documentation uses click-extra's Sphinx directives to show live CLI examples:

```markdown
# Define CLI source (hidden by default)
\`\`\`{click:source}
:hide-results:
from lumos.cli import cli
\`\`\`

# Run CLI command and show output with ANSI colors
\`\`\`{click:run}
invoke(cli, args=["--help"])
\`\`\`
```

### Updating Documentation

1. **For CLI changes**: Update docstrings in the source code. The CLI reference uses `click:run` directives to execute commands and display their help.

2. **For usage examples**: Edit `docs/examples.md` with new code samples.

3. **For installation changes**: Update `docs/installation.md` and `README.md`.

## Release Process

Releases are automated via [semantic-release](https://semantic-release.gitbook.io/) and GitHub Actions.

### Triggering a Release

1. Go to the GitHub Actions page
2. Select the "Release" workflow
3. Click "Run workflow"
4. Optionally enable "Dry run" to preview the release

### What Happens During Release

1. **Version Analysis**: semantic-release analyzes commits to determine the next version
2. **Build**: Cross-platform binaries are built for Linux, macOS, and Windows
3. **Documentation**: Documentation is regenerated with the new version
4. **Release**:
   - `CHANGELOG.md` is updated
   - `pyproject.toml` version is bumped
   - Git tag is created
   - GitHub Release is published with binaries
   - Homebrew formula is updated

### Version Bumping

Version bumps are determined by commit messages:
- `feat:` → Minor version bump (e.g., 1.0.0 → 1.1.0)
- `fix:` → Patch version bump (e.g., 1.0.0 → 1.0.1)
- `BREAKING CHANGE:` in commit body → Major version bump (e.g., 1.0.0 → 2.0.0)

### Manual Release (Emergency)

If automated release fails:

```bash
# Update version manually
uv version X.Y.Z

# Build artifacts
uv build
uv run pyinstaller src/lumos/__main__.py

# Create and push tag
git tag vX.Y.Z
git push origin vX.Y.Z
```

## Getting Help

- **Issues**: [GitHub Issues](https://github.com/teamlumos/lumos-cli/issues)
- **Discussions**: [GitHub Discussions](https://github.com/teamlumos/lumos-cli/discussions)

## License

This project is licensed under the MIT License - see the LICENSE file for details.
