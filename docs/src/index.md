---
title: Command Line Interface
slug: cli
category:
  uri: TOOLS
content:
  excerpt:
    Welcome to the Lumos CLI documentation.
---

# Lumos CLI Documentation

Welcome to the [Lumos CLI](https://github.com/teamlumos/lumos-cli) documentation. The Lumos CLI is a command-line interface for interacting with the Lumos platform, enabling you to manage access requests, list resources, and automate workflows.

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

## Reporting Issues

If you run into issues, please reach out to your Lumos admin or your Lumos contact for support. You can also open an issue [here](https://github.com/teamlumos/lumos-cli/issues/new).


## Table of Contents

```{toctree}
:maxdepth: 1
:caption: Docs

installation
authentication
reference
examples
contributing

```
