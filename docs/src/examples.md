---
title: Examples
slug: cli-examples
category:
  uri: TOOLS
content:
  excerpt: Lumos CLI Examples
parent:
  uri: cli
---
# Examples

This page provides practical examples for common Lumos CLI workflows with code samples.

## Authentication

### Initial Setup

Set up the CLI for first-time use:

```bash
lumos setup
```

This will guide you through the authentication process and store your credentials securely.

### Login with Admin Privileges

If you need admin access:

```bash
lumos login --admin
```

### Check Current User

Verify who you're logged in as:

```bash
lumos whoami
```

Get just the username:

```bash
lumos whoami --username
```

Get just the user ID:

```bash
lumos whoami --id
```

## Listing Resources

### List Apps

Browse all available apps in the appstore:

```bash
lumos list apps
```

Filter apps by name:

```bash
lumos list apps --like github
```

List only apps you have access to:

```bash
lumos list apps --mine
```

### List Users

Search for users:

```bash
lumos list users --like "john.doe"
```

Output as JSON for scripting:

```bash
lumos list users --json
```

Output as CSV:

```bash
lumos list users --csv > users.csv
```

### List Permissions

List permissions for a specific app:

```bash
lumos list permissions --app APP_UUID
```

Filter permissions by name:

```bash
lumos list permissions --app APP_UUID --like "admin"
```

### List Groups

List all groups:

```bash
lumos list groups
```

List groups for a specific app:

```bash
lumos list groups --app APP_UUID
```

### List Access Requests

List your pending requests:

```bash
lumos list requests --mine --pending
```

List all past requests:

```bash
lumos list requests --past
```

Filter by status:

```bash
lumos list requests --status COMPLETED
lumos list requests --status PENDING
lumos list requests --status DENIED_PROVISIONING
```

## Making Access Requests

### Interactive Request

The simplest way to make a request is interactively:

```bash
lumos request
```

This will guide you through selecting an app, permissions, and duration.

### Request with App Filter

Filter the app list to make selection faster:

```bash
lumos request --app-like github
```

### Fully Scripted Request

For automation, specify all parameters:

```bash
lumos request \
  --app APP_UUID \
  --permission PERMISSION_UUID \
  --reason "Need access for deployment" \
  --length 43200 \
  --for-me \
  --no-wait
```

### Request Multiple Permissions

Request multiple permissions at once:

```bash
lumos request \
  --app APP_UUID \
  --permission PERMISSION_UUID_1 \
  --permission PERMISSION_UUID_2 \
  --reason "Project access" \
  --for-me
```

### Request for Another User

Request access on behalf of another user:

```bash
lumos request \
  --app APP_UUID \
  --for-user USER_UUID \
  --reason "Team onboarding"
```

### Request with Duration

Specify access duration (in seconds):

```bash
# 12 hours
lumos request --app APP_UUID --length 43200 --reason "Temporary access"

# Or use friendly duration strings
lumos request --app APP_UUID --length "12 hours" --reason "Temporary access"
```

### Dry Run

Preview the request command without submitting:

```bash
lumos request --dry-run
```

This outputs the exact command you would run, useful for building automation scripts.

## Monitoring Requests

### Check Request Status

Get status of your last request:

```bash
lumos request status --last
```

Check a specific request:

```bash
lumos request status --request-id REQUEST_UUID
```

### Poll for Completion

Wait for a request to complete (with 2-minute timeout):

```bash
lumos request poll --request-id REQUEST_UUID --wait 2
```

### Cancel a Request

Cancel a pending request:

```bash
lumos request cancel --request-id REQUEST_UUID --reason "No longer needed"
```

## Scripting Examples

### Shell Script: Impersonation Function

Add this to your `.zshrc` or `.bashrc` for quick impersonation requests:

```bash
impersonate() {
    local permission="$1"
    local reason="${2:-Impersonation for debugging}"

    lumos request \
        --app c463381c-1ed1-47ef-9bba-cba1ab4d195c \
        --permission-like "$permission" \
        --length 43200 \
        --reason "$reason" \
        --for-me \
        --wait
}

# Usage: impersonate "admin" "Debugging production issue"
```

### Python Script: Batch Access Requests

```python
#!/usr/bin/env python3
"""Batch access request script using Lumos CLI."""

import subprocess
import json


def request_access(app_id: str, permission_ids: list[str], reason: str):
    """Request access to an app with specified permissions."""
    cmd = [
        "lumos", "request",
        "--app", app_id,
        "--reason", reason,
        "--for-me",
        "--no-wait",
    ]

    for perm_id in permission_ids:
        cmd.extend(["--permission", perm_id])

    result = subprocess.run(cmd, capture_output=True, text=True)
    return result.returncode == 0


def list_apps(search: str = None) -> list[dict]:
    """List apps, optionally filtered by search term."""
    cmd = ["lumos", "list", "apps", "--json"]
    if search:
        cmd.extend(["--like", search])

    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode == 0:
        return json.loads(result.stdout)
    return []


def main():
    # Find GitHub app
    apps = list_apps("github")
    if apps:
        print(f"Found {len(apps)} GitHub-related apps")
        for app in apps:
            print(f"  - {app.get('name', 'Unknown')} ({app.get('id', 'N/A')})")


if __name__ == "__main__":
    main()
```

### Bash Script: Auto-Request with Retry

```bash
#!/bin/bash
# Auto-request access with retry logic

APP_ID="your-app-uuid"
PERMISSION_ID="your-permission-uuid"
REASON="Automated access request"
MAX_RETRIES=3

request_access() {
    lumos request \
        --app "$APP_ID" \
        --permission "$PERMISSION_ID" \
        --reason "$REASON" \
        --for-me \
        --wait
}

for i in $(seq 1 $MAX_RETRIES); do
    echo "Attempt $i of $MAX_RETRIES..."
    if request_access; then
        echo "Access granted!"
        exit 0
    fi
    echo "Request failed or pending approval. Retrying in 30 seconds..."
    sleep 30
done

echo "Failed to obtain access after $MAX_RETRIES attempts"
exit 1
```

### JSON Output for Automation

Get request data in JSON format for processing:

```bash
# List pending requests as JSON
lumos list requests --mine --pending --json | jq '.[] | {id, status, app: .app_name}'

# Get user IDs only
lumos list users --like "engineering" --id-only

# Export apps to CSV for analysis
lumos list apps --csv > apps.csv
```

## Output Formats

All `list` commands support multiple output formats:

| Format | Flag | Use Case |
|--------|------|----------|
| Table | (default) | Human-readable terminal output |
| JSON | `--json` | Scripting and API integration |
| CSV | `--csv` | Spreadsheet import/export |
| ID Only | `--id-only` | Piping to other commands |

### Pagination

Control pagination for large result sets:

```bash
# Disable pagination (fetch all)
lumos list apps --no-paginate

# Custom page size
lumos list users --page-size 50 --page 2
```
