# Lumos CLI Documentation

Welcome to the Lumos CLI documentation. The Lumos CLI is a command-line interface for interacting with the Lumos platform, enabling you to manage access requests, list resources, and automate workflows.

## Quick Start

```bash
# Install via Homebrew (macOS and Linux)
brew install teamlumos/tap/lumos

# Login to your Lumos account
lumos login

# Check who you're logged in as
lumos whoami

# List available apps
lumos list apps --like github

# Request access to an app
lumos request
```

## Features

- **OAuth Authentication**: Securely login to your Lumos account
- **Access Requests**: Request, monitor, and cancel access to applications
- **Resource Listing**: Browse apps, permissions, users, and groups
- **Scriptable**: Output in JSON or CSV for automation
- **Interactive Mode**: User-friendly prompts for selecting apps and permissions

## Table of Contents

```{toctree}
:maxdepth: 2
:caption: User Guide

installation
examples
```

```{toctree}
:maxdepth: 3
:caption: Reference

cli-reference
```

```{toctree}
:maxdepth: 1
:caption: Contributing
contributing
```
