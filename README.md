# Installation

## macOS and Linux (via Homebrew)

```shell
brew install teamlumos/tap/lumos
```

Supported platforms:
- macOS (Apple Silicon and Intel)
- Linux (x86_64 and ARM64)

## Other Installation Methods

Download the latest release binary for your platform from the [releases page](https://github.com/teamlumos/lumos-cli/releases).

# Documentation
### Examples

You can run commands like:

`lumos request`

`lumos list apps --like sales`

`lumos list users --like Albus`

`lumos request --app APP_ID --permission PERMISSION_ID_1 --permision PERMISSION_ID_2`

`lumos status --last`

If you know
- you have a lot of requestable apps
- the app you're requesting has a lot of permissions
- you're requesting the app for one of many users
- or just generally don't like long lists

you can narrow down the options presented to you when requesting by using:

`lumos request --app-like github --permission-like dev --user-like sirius`

An example of a `.zshrc` function to impersonate for 12h:
```
impersonate() {
    lumos request --app c463381c-1ed1-47ef-9bba-cba1ab4d195c --permission-like $1 --length 43200 --reason $2
}
```

### Commands
#### `lumos whoami`
Give current user details

#### `lumos login`
Logs into Lumos via OAuth

#### `lumos setup`
Lets you setup/re-setup your authentication

#### `lumos logout`
Clears stored credentials

#### `lumos list [apps|permissions|users|requests] [--like]`
Lists details of the corresponding collections, with `--like` narrowing the list on partial match (i.e. partial match on name or email for users, partial match on app name, partial match on permissions name)

#### `lumos request`

| Flag | Type | Required? |  Description |
|------|------|-----------|--------------|
| `--app`| UUID | ✅ | App UUID. Takes precedence over `--app-like` |
| `--app-like` | text | | App name like--filters apps shown as options when selecting |
| `--reason` | text | ✅ |Business justification for request |
| `--for-user` | UUID  | | user for whom to request access. Takes precedence over --user-like |
| `--for-me`  | ||  Makes the request for the current user. |
| `--user-like` | text | | User like--filters users shown as options when requesting for someone else |
| `--permission` | UUID | ✅ | List of permission UUIDs (i.e. `--permission permission1 --permission permission2`. Takes precedence over `--permission-like` |
| `--permission-like` | text | | Permission name like--filters permissions shown as options when selecting |
| `--length` | integer | ✅ | Length of access request in seconds. Don't populate unless you know your app permission's specific settings |
| `--wait` |  | | Poll request once submitted |
| `--dry-run` |  | | Don't submit the request, just get the command to do it |

#### `lumos request status [--last]`
Gets the last request you made, or if `--request-id` is passed/`--last` flag not present, prompts you for a request ID


# Development Setup

```shell
uv sync
```

It is recommended that you create this alias:
`alias lumosdev='uv run python -m lumos'`


## Releasing

The release process is automated via semantic-release:

1. Trigger the Release workflow from GitHub Actions
2. Semantic-release will:
   - Analyze commits to determine the version
   - Create a changelog
   - Create a git tag and GitHub release
3. The Build workflow will automatically build and upload binaries for all platforms
4. The Homebrew formula will be automatically updated

For more details on Homebrew distribution, see [scripts/README.md](scripts/README.md).


