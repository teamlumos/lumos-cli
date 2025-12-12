# Installation

## macOS and Linux (via Homebrew)

The recommended way to install Lumos CLI on macOS and Linux is via Homebrew:

```bash
brew install teamlumos/tap/lumos
```

This installs a native binary with no Python dependencies required.

### Supported Platforms

- macOS (Apple Silicon / ARM64)
- Linux (x86_64 / AMD64)
- Linux (ARM64)
- Windows (x86_64)

## Python Package (via pip or uv)

You can also install Lumos CLI as a Python package from GitHub Releases.

### Using pip

```bash
# Download the wheel from the latest release
pip install https://github.com/teamlumos/lumos-cli/releases/latest/download/lumos_cli-VERSION-py3-none-any.whl
```

Replace `VERSION` with the actual version number from the [releases page](https://github.com/teamlumos/lumos-cli/releases).

### Using uv

```bash
# Install from GitHub releases
uv tool install https://github.com/teamlumos/lumos-cli/releases/latest/download/lumos_cli-VERSION-py3-none-any.whl
```

## Binary Downloads

Download pre-built binaries directly from the [GitHub Releases page](https://github.com/teamlumos/lumos-cli/releases):

| Platform | Architecture | Download |
|----------|--------------|----------|
| Linux | AMD64 (x86_64) | `lumos-linux-amd64-vX.X.X.tar.gz` |
| Linux | ARM64 | `lumos-linux-arm64-vX.X.X.tar.gz` |
| macOS | ARM64 (Apple Silicon) | `lumos-macos-arm64-vX.X.X.tar.gz` |
| Windows | x86_64 | `lumos-windows-vX.X.X.tar.gz` |

### Linux/macOS Installation

```bash
# Download and extract (example for Linux AMD64)
curl -LO https://github.com/teamlumos/lumos-cli/releases/latest/download/lumos-linux-amd64-vX.X.X.tar.gz
tar -xzf lumos-linux-amd64-vX.X.X.tar.gz

# Move to a directory in your PATH
sudo mv lumos /usr/local/bin/

# Verify installation
lumos --version
```

### Windows Installation

1. Download the Windows binary from the releases page
2. Extract the archive
3. Add the extracted directory to your PATH
4. Open a new terminal and run `lumos --version`

## Initial Setup

After installation, authenticate with your Lumos account:

```bash
# Setup authentication (first time)
lumos setup

# Or login directly via OAuth
lumos login
```

You'll be directed to authenticate in your browser. Once complete, you can verify your login:

```bash
lumos whoami
```

## Troubleshooting

### Command not found

Ensure the installation directory is in your PATH:

```bash
# For Homebrew
export PATH="/opt/homebrew/bin:$PATH"

# For manual installation
export PATH="/usr/local/bin:$PATH"
```

### Permission denied

If you get permission errors when installing to `/usr/local/bin`:

```bash
# Use sudo
sudo mv lumos /usr/local/bin/

# Or install to a user directory
mkdir -p ~/.local/bin
mv lumos ~/.local/bin/
export PATH="$HOME/.local/bin:$PATH"
```

### Authentication issues

If you have trouble logging in:

```bash
# Clear existing credentials
lumos logout

# Re-run setup
lumos setup
```
