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
lumos app list --like github

# Request access (interactive)
lumos request create

# Request access (scripted)
lumos request create --app APP_UUID --reason "Need access" --for-me --wait
```

## Command Structure

The CLI follows RESTful conventions with `lumos <noun> <verb>` syntax:

| Command | Description |
|---------|-------------|
| `lumos app list` | List apps in the appstore |
| `lumos user list` | List users |
| `lumos group list` | List groups |
| `lumos permission list --app UUID` | List permissions for an app |
| `lumos request create` | Create an access request |
| `lumos request list` | List access requests |
| `lumos request status` | Check request status |
| `lumos request poll` | Poll request for completion |
| `lumos request cancel` | Cancel a request |

Authentication commands remain at the root level:

| Command | Description |
|---------|-------------|
| `lumos whoami` | Show current user |
| `lumos setup` | Setup authentication |
| `lumos login` | Login via OAuth |
| `lumos logout` | Logout |

## Documentation

- **[Installation](docs/installation.md)** - Detailed installation instructions for all platforms
- **[Examples](docs/examples.md)** - Usage examples with code samples
- **[CLI Reference](docs/cli-reference.md)** - Complete command reference

Online documentation: [teamlumos.github.io/lumos-cli](https://teamlumos.github.io/lumos-cli/)

## Development

See [CONTRIBUTING.md](CONTRIBUTING.md) for development setup and guidelines.

## License

MIT
