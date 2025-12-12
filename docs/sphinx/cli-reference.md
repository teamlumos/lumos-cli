# CLI Reference

This page provides a complete reference for all Lumos CLI commands with live examples.

```{click:source}
:hide-source:
from lumos_cli.cli import lumos

```

## Getting Help

You can get help for any command by using the `--help` flag:

```{click:run}
invoke(lumos, args=["--no-color", "--help"])
```

## Authentication Commands

### `lumos whoami`

Show information about the currently logged in user.

```{click:run}
invoke(lumos, args=["--no-color", "whoami", "--help"])
```

### `lumos setup`

Setup your Lumos CLI authentication. Can be used to login or change your authentication method.

```{click:run}
invoke(lumos, args=["--no-color", "setup", "--help"])
```

### `lumos login`

Login to your Lumos account via OAuth. You must be logged in to Lumos on your browser.

```{click:run}
invoke(lumos, args=["--no-color", "login", "--help"])
```

### `lumos logout`

Logout of your Lumos account and clear stored credentials.

```{click:run}
invoke(lumos, args=["--no-color", "logout", "--help"])
```

## List Commands

The `list` command group provides access to various Lumos resources.

```{click:run}
invoke(lumos, args=["--no-color", "list", "--help"])
```

### `lumos list apps`

List apps available in the appstore.

```{click:run}
invoke(lumos, args=["list", "--no-color", "apps", "--help"])
```

### `lumos list users`

List users in Lumos.

```{click:run}
invoke(lumos, args=["list", "--no-color", "users", "--help"])
```

### `lumos list permissions`

List permissions for a given app.

```{click:run}
invoke(lumos, args=["list", "--no-color", "permissions", "--help"])
```

### `lumos list groups`

List groups for the domain or a specific app.

```{click:run}
invoke(lumos, args=["list", "--no-color", "groups", "--help"])
```

### `lumos list requests`

List access requests.

```{click:run}
invoke(lumos, args=["list", "--no-color", "requests", "--help"])
```

## Request Commands

The `request` command group handles access requests.

```{click:run}
invoke(lumos, args=["--no-color", "request", "--help"])
```

### `lumos request status`

Check the status of a request by ID or use `--last` for the most recent request.

**Options:**

| Flag | Description |
|------|-------------|
| `--request-id` | Request ID to check |
| `--last` | Get the last request |
| `--status-only` | Output status only |
| `--permission-only` | Output permission only |
| `--id-only` | Output request ID only |

### `lumos request poll`

Poll a request by ID for up to 5 minutes, waiting for completion.

**Options:**

| Flag | Description |
|------|-------------|
| `--request-id` | Request ID to poll |
| `--wait` | How many minutes to wait (max 5) |

### `lumos request cancel`

Cancel a pending request.

**Options:**

| Flag | Description |
|------|-------------|
| `--request-id` | Request ID to cancel |
| `--reason` | Reason for cancellation |
