---
title: Installation
slug: cli-installation
category:
  uri: TOOLS
content:
  excerpt: Installing the Lumos CLI
parent:
  uri: cli
---

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


## Install from Source

You can install Lumos CLI directly from the GitHub repository using pip or uv with the git protocol.

```bash
# Install from the main branch
pip install git+https://github.com/teamlumos/lumos-cli.git

# Install as a tool from the main branch
uv tool install git+https://github.com/teamlumos/lumos-cli.git
```
