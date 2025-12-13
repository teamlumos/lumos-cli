# CLI Reference

This page provides a complete reference for all Lumos CLI commands with live examples.

## Command Structure

The Lumos CLI follows RESTful conventions with `lumos <noun> <verb>` syntax:

```
lumos <noun> <verb> [OPTIONS]
```

**Noun-based command groups:**
- `app` - Manage apps
- `user` - Manage users
- `group` - Manage groups
- `permission` - Manage permissions
- `request` - Manage access requests

**Root-level authentication commands:**
- `whoami` - Show current user
- `setup` - Setup authentication
- `login` - Login via OAuth
- `logout` - Logout

## Getting Help

You can get help for any command by using the `--help` flag:

```bash
lumos --help
lumos app --help
lumos app list --help
```

## Authentication Commands

### `lumos whoami`

Show information about the currently logged in user.

```bash
lumos whoami [OPTIONS]
```

**Options:**

| Option | Description |
|--------|-------------|
| `--username` | Show the current user's username only |
| `--id` | Show the current user's ID only |

### `lumos setup`

Setup your Lumos CLI authentication. Can be used to login or change your authentication method.

```bash
lumos setup
```

### `lumos login`

Login to your Lumos account via OAuth. You must be logged in to Lumos on your browser.

```bash
lumos login [OPTIONS]
```

**Options:**

| Option | Description |
|--------|-------------|
| `--admin` | Log in as an admin, if you have the permission to do so |

### `lumos logout`

Logout of your Lumos account and clear stored credentials.

```bash
lumos logout
```

## App Commands

### `lumos app list`

List apps available in the appstore.

```bash
lumos app list [OPTIONS]
```

**Options:**

| Option | Description | Default |
|--------|-------------|---------|
| `--like TEXT` | Filter apps by search term | |
| `--mine` | Show only my apps | |
| `--csv` | Output as CSV | |
| `--json` | Output as JSON | |
| `--paginate / --no-paginate` | Enable/disable pagination | `paginate` |
| `--page-size INTEGER` | Page size | `100` |
| `--page INTEGER` | Page number | `1` |
| `--id-only` | Output ID only | |

**Examples:**

```bash
# List all apps
lumos app list

# Search for GitHub apps
lumos app list --like github

# Export as JSON
lumos app list --json

# List my apps only
lumos app list --mine
```

## User Commands

### `lumos user list`

List users in Lumos.

```bash
lumos user list [OPTIONS]
```

**Options:**

| Option | Description | Default |
|--------|-------------|---------|
| `--like TEXT` | Search by name or email | |
| `--csv` | Output as CSV | |
| `--json` | Output as JSON | |
| `--paginate / --no-paginate` | Enable/disable pagination | `paginate` |
| `--page-size INTEGER` | Page size | `100` |
| `--page INTEGER` | Page number | `1` |
| `--id-only` | Output ID only | |

**Examples:**

```bash
# List all users
lumos user list

# Search for users
lumos user list --like "john.doe"

# Export user IDs
lumos user list --id-only
```

## Group Commands

### `lumos group list`

List groups for the domain or a specific app.

```bash
lumos group list [OPTIONS]
```

**Options:**

| Option | Description | Default |
|--------|-------------|---------|
| `--app TEXT` | App ID to filter groups by | |
| `--like TEXT` | Filter groups by name | |
| `--csv` | Output as CSV | |
| `--json` | Output as JSON | |
| `--paginate / --no-paginate` | Enable/disable pagination | `paginate` |
| `--page-size INTEGER` | Page size | `100` |
| `--page INTEGER` | Page number | `1` |
| `--id-only` | Output ID only | |

**Examples:**

```bash
# List all groups
lumos group list

# List groups for a specific app
lumos group list --app APP_UUID

# Filter groups
lumos group list --like "engineering"
```

## Permission Commands

### `lumos permission list`

List permissions for a given app.

```bash
lumos permission list --app APP_UUID [OPTIONS]
```

**Options:**

| Option | Description | Default |
|--------|-------------|---------|
| `--app TEXT` | App UUID (required) | |
| `--like TEXT` | Filter permissions by name | |
| `--csv` | Output as CSV | |
| `--json` | Output as JSON | |
| `--paginate / --no-paginate` | Enable/disable pagination | `paginate` |
| `--page-size INTEGER` | Page size | `100` |
| `--page INTEGER` | Page number | `1` |
| `--id-only` | Output ID only | |

**Examples:**

```bash
# List all permissions for an app
lumos permission list --app APP_UUID

# Filter permissions
lumos permission list --app APP_UUID --like "admin"

# Get permission IDs only
lumos permission list --app APP_UUID --id-only
```

## Request Commands

### `lumos request create`

Create an access request for an app.

```bash
lumos request create [OPTIONS]
```

**Options:**

| Option | Description |
|--------|-------------|
| `--reason TEXT` | Business justification for request |
| `--for-user TEXT` | UUID of user for whom to request access |
| `--for-me` | Make the request for the current user |
| `--mine` | Alias for `--for-me` |
| `--app TEXT` | App UUID |
| `--permission TEXT` | Permission UUID (can be repeated) |
| `--length TEXT` | Duration in seconds or friendly string (e.g., "12 hours", "2d") |
| `--user-like TEXT` | Filter users when selecting interactively |
| `--app-like TEXT` | Filter apps when selecting interactively |
| `--permission-like TEXT` | Filter permissions when selecting interactively |
| `--wait / --no-wait` | Wait for the request to complete |
| `--dry-run` | Print the request command without submitting |

**Examples:**

```bash
# Interactive request
lumos request create

# Fully scripted request
lumos request create \
  --app APP_UUID \
  --permission PERMISSION_UUID \
  --reason "Need access for deployment" \
  --length 43200 \
  --for-me \
  --wait

# Request with multiple permissions
lumos request create \
  --app APP_UUID \
  --permission PERM_1 \
  --permission PERM_2 \
  --reason "Project access" \
  --for-me

# Dry run to preview command
lumos request create --dry-run
```

### `lumos request list`

List access requests.

```bash
lumos request list [OPTIONS]
```

**Options:**

| Option | Description | Default |
|--------|-------------|---------|
| `--for-user TEXT` | Show only requests targeting a particular user | |
| `--mine` | Show only requests targeting me | |
| `--status TEXT` | Filter by status (can be repeated) | |
| `--pending` | Show only pending requests | |
| `--past` | Show only past requests | |
| `--csv` | Output as CSV | |
| `--json` | Output as JSON | |
| `--paginate / --no-paginate` | Enable/disable pagination | `paginate` |
| `--page-size INTEGER` | Page size | `100` |
| `--page INTEGER` | Page number | `1` |
| `--id-only` | Output ID only | |

**Examples:**

```bash
# List my pending requests
lumos request list --mine --pending

# List all completed requests
lumos request list --status COMPLETED

# Export requests as JSON
lumos request list --json
```

### `lumos request status`

Check the status of a request by ID or `--last` for the most recent request.

```bash
lumos request status [OPTIONS]
```

**Options:**

| Option | Description |
|--------|-------------|
| `--request-id TEXT` | Request ID to check |
| `--last` | Get the last request |
| `--status-only` | Output status only |
| `--permission-only` | Output permission only |
| `--id-only` | Output request ID only |

**Examples:**

```bash
# Check last request status
lumos request status --last

# Check specific request
lumos request status --request-id REQUEST_UUID

# Get just the status
lumos request status --request-id REQUEST_UUID --status-only
```

### `lumos request poll`

Poll a request by ID for up to 5 minutes, waiting for completion.

```bash
lumos request poll [OPTIONS]
```

**Options:**

| Option | Description | Default |
|--------|-------------|---------|
| `--request-id TEXT` | Request ID to poll | |
| `--wait INTEGER` | How many minutes to wait (max 5) | `2` |

**Examples:**

```bash
# Poll with default 2-minute timeout
lumos request poll --request-id REQUEST_UUID

# Poll with 5-minute timeout
lumos request poll --request-id REQUEST_UUID --wait 5
```

### `lumos request cancel`

Cancel a pending request.

```bash
lumos request cancel [OPTIONS]
```

**Options:**

| Option | Description |
|--------|-------------|
| `--request-id TEXT` | Request ID to cancel |
| `--reason TEXT` | Reason for cancellation |

**Examples:**

```bash
# Cancel a request
lumos request cancel --request-id REQUEST_UUID

# Cancel with reason
lumos request cancel --request-id REQUEST_UUID --reason "No longer needed"
```

## Deprecated Commands

The following `lumos list *` commands are deprecated but still supported for backward compatibility. They will show a deprecation warning when used.

| Deprecated Command | New Command |
|-------------------|-------------|
| `lumos list apps` | `lumos app list` |
| `lumos list users` | `lumos user list` |
| `lumos list groups` | `lumos group list` |
| `lumos list permissions` | `lumos permission list` |
| `lumos list requests` | `lumos request list` |

## Global Options

These options are available on all commands:

| Option | Description |
|--------|-------------|
| `--time / --no-time` | Measure and print elapsed execution time |
| `--color / --no-color` | Enable/disable colored output |
| `--config CONFIG_PATH` | Location of configuration file |
| `--no-config` | Ignore all configuration files |
| `--show-params` | Show all CLI parameters and their values |
| `--table-format FORMAT` | Rendering style of tables |
| `--verbosity LEVEL` | Logging verbosity (CRITICAL, ERROR, WARNING, INFO, DEBUG) |
| `-v, --verbose` | Increase verbosity |
| `--version` | Show version and exit |
| `-h, --help` | Show help and exit |
