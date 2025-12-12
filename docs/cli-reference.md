# CLI Reference

This page provides a complete reference for all Lumos CLI commands with live examples.

## Getting Help

You can get help for any command by using the `--help` flag:

```{click:source}
:hide-results:
import sys
sys.path.insert(0, "../src")
from lumos_cli.cli import cli
```

```{click:run}
invoke(cli, args=["--help"])
```

## Authentication Commands

### `lumos whoami`

Show information about the currently logged in user.

```{click:run}
invoke(cli, args=["whoami", "--help"])
```

### `lumos setup`

Setup your Lumos CLI authentication. Can be used to login or change your authentication method.

```{click:run}
invoke(cli, args=["setup", "--help"])
```

### `lumos login`

Login to your Lumos account via OAuth. You must be logged in to Lumos on your browser.

```{click:run}
invoke(cli, args=["login", "--help"])
```

### `lumos logout`

Logout of your Lumos account and clear stored credentials.

```{click:run}
invoke(cli, args=["logout", "--help"])
```

## List Commands

The `list` command group provides access to various Lumos resources.

```{click:run}
invoke(cli, args=["list", "--help"])
```

### `lumos list apps`

List apps available in the appstore.

```{click:run}
invoke(cli, args=["list", "apps", "--help"])
```

### `lumos list users`

List users in Lumos.

```{click:run}
invoke(cli, args=["list", "users", "--help"])
```

### `lumos list permissions`

List permissions for a given app.

```{click:run}
invoke(cli, args=["list", "permissions", "--help"])
```

### `lumos list groups`

List groups for the domain or a specific app.

```{click:run}
invoke(cli, args=["list", "groups", "--help"])
```

### `lumos list requests`

List access requests.

```{click:run}
invoke(cli, args=["list", "requests", "--help"])
```

## Request Commands

The `request` command group handles access requests.

```{click:run}
invoke(cli, args=["request", "--help"])
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
