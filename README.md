# Lumos CLI

A command-line interface for the Lumos platform. Manage access requests, list resources, and automate workflows.

## Installation

### Homebrew (macOS and Linux)

```shell
brew install teamlumos/tap/lumos
```

### Other Methods

See [Installation Guide](docs/_build/markdown/installation.md) for pip, uv, and binary installation options.

## Quick Start

```shell
# Setup authentication
lumos setup

# Check current user
lumos whoami

# List available apps
lumos list apps --like github

# Request access
lumos request
```

## Documentation

Full documentation is available in the [`docs/_build/markdown/`](docs/_build/markdown/) directory:

- **[Installation](docs/_build/markdown/installation.md)** - Detailed installation instructions for all platforms
- **[Examples](docs/_build/markdown/examples.md)** - Usage examples with code samples
- **[CLI Reference](docs/_build/markdown/cli-reference.md)** - Complete command reference

Online documentation: [teamlumos.github.io/lumos-cli](https://teamlumos.github.io/lumos-cli/)

## Development

See [CONTRIBUTING.md](CONTRIBUTING.md) for development setup and guidelines.

## License

MIT
