# Lumos CLI

A command-line interface for the Lumos platform. Manage access requests, list resources, and automate workflows.

## Installation

### Homebrew (macOS and Linux)

```shell
brew install teamlumos/tap/lumos
```

### Other Methods

See [Installation Guide](docs/installation.md) for pip, uv, and binary installation options.

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

- **[Installation](docs/installation.md)** - Detailed installation instructions for all platforms
- **[Examples](docs/examples.md)** - Usage examples with code samples
- **[CLI Reference](docs/reference.md)** - Complete command reference

Online documentation: [teamlumos.github.io/lumos-cli](https://teamlumos.github.io/lumos-cli/)

## Development

See [CONTRIBUTING.md](CONTRIBUTING.md) for development setup and guidelines.

## License

MIT
