# Reference

This page provides a complete reference for all Lumos CLI commands.

## Getting Help

You can get help for any command by using the `--help` flag:

## Authentication Commands

### `lumos whoami`

Show information about the currently logged in user.

### `lumos setup`

Setup your Lumos CLI authentication. Can be used to login or change your authentication method.

### `lumos login`

Login to your Lumos account via OAuth. You must be logged in to Lumos on your browser.

### `lumos logout`

Logout of your Lumos account and clear stored credentials.

## List Commands

The `list` command group provides access to various Lumos resources.

### `lumos list apps`

List apps available in the appstore.

### `lumos list users`

List users in Lumos.

### `lumos list permissions`

List permissions for a given app.

### `lumos list groups`

List groups for the domain or a specific app.

### `lumos list requests`

List access requests.

## Request Commands

The `request` command group handles access requests.

### `lumos request status`

Check the status of a request by ID or use `--last` for the most recent request.

**Options:**

| Flag                | Description            |
|:--------------------|:-----------------------|
| `--request-id`      | Request ID to check    |
| `--last`            | Get the last request   |
| `--status-only`     | Output status only     |
| `--permission-only` | Output permission only |
| `--id-only`         | Output request ID only |

### `lumos request poll`

Poll a request by ID for up to 5 minutes, waiting for completion.

**Options:**

| Flag           | Description                      |
|:---------------|:---------------------------------|
| `--request-id` | Request ID to poll               |
| `--wait`       | How many minutes to wait (max 5) |

### `lumos request cancel`

Cancel a pending request.

**Options:**

| Flag           | Description             |
|:---------------|:------------------------|
| `--request-id` | Request ID to cancel    |
| `--reason`     | Reason for cancellation |
