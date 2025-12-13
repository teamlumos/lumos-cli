<!--
  AUTO-GENERATED SOURCE FILE
  This is the source file for Sphinx documentation.
  Edit this file, then run \`make markdown\` from docs/ to regenerate docs/\*.md
-->

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

## User Guide

* [Installation](installation.md)
  * [macOS and Linux (via Homebrew)](installation.md#macos-and-linux-via-homebrew)
  * [Python Package (via pip or uv)](installation.md#python-package-via-pip-or-uv)
  * [Binary Downloads](installation.md#binary-downloads)
  * [Initial Setup](installation.md#initial-setup)
  * [Troubleshooting](installation.md#troubleshooting)
* [Examples](examples.md)
  * [Authentication](examples.md#authentication)
  * [Listing Resources](examples.md#listing-resources)
  * [Making Access Requests](examples.md#making-access-requests)
  * [Monitoring Requests](examples.md#monitoring-requests)
  * [Scripting Examples](examples.md#scripting-examples)
  * [Output Formats](examples.md#output-formats)
  * [Migration from Old Syntax](examples.md#migration-from-old-syntax)

## Reference

* [CLI Reference](cli-reference.md)
  * [Getting Help](cli-reference.md#getting-help)
  * [Authentication Commands](cli-reference.md#authentication-commands)
    * [`lumos whoami`](cli-reference.md#lumos-whoami)
    * [`lumos setup`](cli-reference.md#lumos-setup)
    * [`lumos login`](cli-reference.md#lumos-login)
    * [`lumos logout`](cli-reference.md#lumos-logout)
  * [App Commands](cli-reference.md#app-commands)
    * [`lumos app list`](cli-reference.md#lumos-app-list)
  * [User Commands](cli-reference.md#user-commands)
    * [`lumos user list`](cli-reference.md#lumos-user-list)
  * [Group Commands](cli-reference.md#group-commands)
    * [`lumos group list`](cli-reference.md#lumos-group-list)
  * [Permission Commands](cli-reference.md#permission-commands)
    * [`lumos permission list`](cli-reference.md#lumos-permission-list)
  * [Request Commands](cli-reference.md#request-commands)
    * [`lumos request create`](cli-reference.md#lumos-request-create)
    * [`lumos request list`](cli-reference.md#lumos-request-list)
    * [`lumos request status`](cli-reference.md#lumos-request-status)
    * [`lumos request poll`](cli-reference.md#lumos-request-poll)
    * [`lumos request cancel`](cli-reference.md#lumos-request-cancel)
