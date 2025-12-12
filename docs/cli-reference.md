# CLI Reference

This page provides a complete reference for all Lumos CLI commands with live examples.

## Getting Help

You can get help for any command by using the `--help` flag:

```ansi-shell-session
$ lumos --no-color --help
Usage: lumos [OPTIONS] COMMAND [ARGS]...

  Lumos CLI - Command line interface for Lumos

Options:
  --time / --no-time    Measure and print elapsed execution time.  [default: no-
                        time]
  --color, --ansi / --no-color, --no-ansi
                        Strip out all colors and all ANSI codes from output.
                        [default: color]
  --config CONFIG_PATH  Location of the configuration file. Supports local path
                        with glob patterns or remote URL.  [default:
                        ~/.config/lumos/*.toml|*.yaml|*.yml|*.json|*.ini]
  --no-config           Ignore all configuration files and only use command line
                        parameters and environment variables.
  --show-params         Show all CLI parameters, their provenance, defaults and
                        value, then exit.
  --table-format [asciidoc|csv|csv-excel|csv-excel-tab|csv-unix|double-grid|double-outline|fancy-grid|fancy-outline|github|grid|heavy-grid|heavy-outline|html|jira|latex|latex-booktabs|latex-longtable|latex-raw|mediawiki|mixed-grid|mixed-outline|moinmoin|orgtbl|outline|pipe|plain|presto|pretty|psql|rounded-grid|rounded-outline|rst|simple|simple-grid|simple-outline|textile|tsv|unsafehtml|vertical|youtrack]
                        Rendering style of tables.  [default: rounded-outline]
  --verbosity LEVEL     Either CRITICAL, ERROR, WARNING, INFO, DEBUG.  [default:
                        WARNING]
  -v, --verbose         Increase the default WARNING verbosity by one level for
                        each additional repetition of the option.  [default: 0]
  --version             Show the version and exit.
  -h, --help            Show this message and exit.

Commands:
  list     List various Lumos resources
  login    Login to your Lumos account via OAuth.
  logout   Logout of your Lumos account.
  request  Request access to an app.
  setup    Setup your Lumos CLI.
  whoami   Show information about the currently logged in user.
```

## Authentication Commands

### `lumos whoami`

Show information about the currently logged in user.

```ansi-shell-session
$ lumos --no-color whoami --help
Usage: lumos whoami [OPTIONS]

  Show information about the currently logged in user.

Options:
  --username  Show the current user's username only
  --id        Show the current user's ID only
  -h, --help  Show this message and exit.
```

### `lumos setup`

Setup your Lumos CLI authentication. Can be used to login or change your authentication method.

```ansi-shell-session
$ lumos --no-color setup --help
Usage: lumos setup [OPTIONS]

  Setup your Lumos CLI. Can be used to login or change your authentication
  method.

Options:
  -h, --help  Show this message and exit.
```

### `lumos login`

Login to your Lumos account via OAuth. You must be logged in to Lumos on your browser.

```ansi-shell-session
$ lumos --no-color login --help
Usage: lumos login [OPTIONS]

  Login to your Lumos account via OAuth. You must be logged in to Lumos on your
  browser.

Options:
  --admin     Log in as an admin, if you have the permission to do so
  -h, --help  Show this message and exit.
```

### `lumos logout`

Logout of your Lumos account and clear stored credentials.

```ansi-shell-session
$ lumos --no-color logout --help
Usage: lumos logout [OPTIONS]

  Logout of your Lumos account.

Options:
  -h, --help  Show this message and exit.
```

## List Commands

The `list` command group provides access to various Lumos resources.

```ansi-shell-session
$ lumos --no-color list --help
Usage: lumos list [OPTIONS] COMMAND [ARGS]...

  List various Lumos resources

Options:
  --time / --no-time    Measure and print elapsed execution time.  [default: no-
                        time]
  --color, --ansi / --no-color, --no-ansi
                        Strip out all colors and all ANSI codes from output.
                        [default: color]
  --config CONFIG_PATH  Location of the configuration file. Supports local path
                        with glob patterns or remote URL.  [default:
                        ~/.config/lumos/*.toml|*.yaml|*.yml|*.json|*.ini]
  --no-config           Ignore all configuration files and only use command line
                        parameters and environment variables.
  --show-params         Show all CLI parameters, their provenance, defaults and
                        value, then exit.
  --table-format [asciidoc|csv|csv-excel|csv-excel-tab|csv-unix|double-grid|double-outline|fancy-grid|fancy-outline|github|grid|heavy-grid|heavy-outline|html|jira|latex|latex-booktabs|latex-longtable|latex-raw|mediawiki|mixed-grid|mixed-outline|moinmoin|orgtbl|outline|pipe|plain|presto|pretty|psql|rounded-grid|rounded-outline|rst|simple|simple-grid|simple-outline|textile|tsv|unsafehtml|vertical|youtrack]
                        Rendering style of tables.  [default: rounded-outline]
  --verbosity LEVEL     Either CRITICAL, ERROR, WARNING, INFO, DEBUG.  [default:
                        WARNING]
  -v, --verbose         Increase the default WARNING verbosity by one level for
                        each additional repetition of the option.  [default: 0]
  --version             Show the version and exit.
  -h, --help            Show this message and exit.

Commands:
  apps         List apps in the appstore
  groups       List groups for the domain or the specified --app
  permissions  List permissions for a given app
  requests     List access requests
  users        List users in Lumos
```

### `lumos list apps`

List apps available in the appstore.

```ansi-shell-session
$ lumos list --no-color apps --help
Usage: lumos list apps [OPTIONS]

  List apps in the appstore

Options:
  --like TEXT                 Filters apps by search term
  --mine                      Show only my apps.
  --csv                       Output as CSV
  --json                      Output as JSON
  --paginate / --no-paginate  Pagination  [default: paginate]
  --page-size INTEGER         Page size  [default: 100]
  --page INTEGER              Page  [default: 1]
  --id-only                   Output ID only
  -h, --help                  Show this message and exit.
```

### `lumos list users`

List users in Lumos.

```ansi-shell-session
$ lumos list --no-color users --help
Usage: lumos list users [OPTIONS]

  List users in Lumos

Options:
  --like TEXT                 Search by name or email
  --csv                       Output as CSV
  --json                      Output as JSON
  --paginate / --no-paginate  Pagination  [default: paginate]
  --page-size INTEGER         Page size  [default: 100]
  --page INTEGER              Page  [default: 1]
  --id-only                   Output ID only
  -h, --help                  Show this message and exit.
```

### `lumos list permissions`

List permissions for a given app.

```ansi-shell-session
$ lumos list --no-color permissions --help
Usage: lumos list permissions [OPTIONS]

  List permissions for a given app

Options:
  --app TEXT                  App UUID  [required]
  --like TEXT                 Filters permissions
  --csv                       Output as CSV
  --json                      Output as JSON
  --paginate / --no-paginate  Pagination  [default: paginate]
  --page-size INTEGER         Page size  [default: 100]
  --page INTEGER              Page  [default: 1]
  --id-only                   Output ID only
  -h, --help                  Show this message and exit.
```

### `lumos list groups`

List groups for the domain or a specific app.

```ansi-shell-session
$ lumos list --no-color groups --help
Usage: lumos list groups [OPTIONS]

  List groups for the domain or the specified --app

Options:
  --app TEXT                  App ID to filter groups by. If not provided, lists
                              all groups.
  --like TEXT                 Filters groups
  --csv                       Output as CSV
  --json                      Output as JSON
  --paginate / --no-paginate  Pagination  [default: paginate]
  --page-size INTEGER         Page size  [default: 100]
  --page INTEGER              Page  [default: 1]
  --id-only                   Output ID only
  -h, --help                  Show this message and exit.
```

### `lumos list requests`

List access requests.

```ansi-shell-session
$ lumos list --no-color requests --help
Usage: lumos list requests [OPTIONS]

  List access requests

Options:
  --for-user TEXT             Show only requests for ('targetting') a particular
                              user
  --mine                      Show only requests for ('targetting') me. Takes
                              precedence over --for-user.
  --status TEXT               One of `PENDING`, `COMPLETED`,
                              `DENIED_PROVISIONING`, etc
  --pending                   Show only pending requests
  --past                      Show only past requests
  --csv                       Output as CSV
  --json                      Output as JSON
  --paginate / --no-paginate  Pagination  [default: paginate]
  --page-size INTEGER         Page size  [default: 100]
  --page INTEGER              Page  [default: 1]
  --id-only                   Output ID only
  -h, --help                  Show this message and exit.
```

## Request Commands

The `request` command group handles access requests.

```ansi-shell-session
$ lumos --no-color request --help
Usage: lumos request [OPTIONS] COMMAND [ARGS]...

  Request access to an app.

Options:
  --reason TEXT           Business justification for request
  --for-user TEXT         UUID of user for whom to request access. Takes
                          precedence over --user-like
  --for-me                Makes the request for the current user.
  --mine                  Makes the request for the current user. Duplicate of
                          --for-me for convenience.
  --app TEXT              App UUID. Takes precedence over --app-like
  --permission TEXT       List of permission UUIDs. Takes precedence over
                          --permission-like
  --length TEXT           Length of access request in seconds, or a string like
                          '12 hours', '2d', 'unlimited', etc. Every
                          app/permission has different configurations.
  --user-like TEXT        User name/email like--filters users shown as options
                          when selecting, if the request is not for the current
                          user
  --app-like TEXT         App name like--filters apps shown as options when
                          selecting
  --permission-like TEXT  Permission name like--filters permissions shown as
                          options when selecting
  --wait / --no-wait      Wait for the request to complete
  --dry-run               Print the request command without actually making the
                          request
  --time / --no-time      Measure and print elapsed execution time.  [default:
                          no-time]
  --color, --ansi / --no-color, --no-ansi
                          Strip out all colors and all ANSI codes from output.
                          [default: color]
  --config CONFIG_PATH    Location of the configuration file. Supports local
                          path with glob patterns or remote URL.  [default:
                          ~/.config/lumos/*.toml|*.yaml|*.yml|*.json|*.ini]
  --no-config             Ignore all configuration files and only use command
                          line parameters and environment variables.
  --show-params           Show all CLI parameters, their provenance, defaults
                          and value, then exit.
  --table-format [asciidoc|csv|csv-excel|csv-excel-tab|csv-unix|double-grid|double-outline|fancy-grid|fancy-outline|github|grid|heavy-grid|heavy-outline|html|jira|latex|latex-booktabs|latex-longtable|latex-raw|mediawiki|mixed-grid|mixed-outline|moinmoin|orgtbl|outline|pipe|plain|presto|pretty|psql|rounded-grid|rounded-outline|rst|simple|simple-grid|simple-outline|textile|tsv|unsafehtml|vertical|youtrack]
                          Rendering style of tables.  [default: rounded-outline]
  --verbosity LEVEL       Either CRITICAL, ERROR, WARNING, INFO, DEBUG.
                          [default: WARNING]
  -v, --verbose           Increase the default WARNING verbosity by one level
                          for each additional repetition of the option.
                          [default: 0]
  --version               Show the version and exit.
  -h, --help              Show this message and exit.

Commands:
  cancel  Cancel a request by ID
  poll    Poll a request by ID for up to 5 minutes
  status  Check the status of a request by ID or `--last` for the most recent...
```

### `lumos request status`

Check the status of a request by ID or use `--last` for the most recent request.

**Options:**

| Flag                | Description            |
| ------------------- | ---------------------- |
| `--request-id`      | Request ID to check    |
| `--last`            | Get the last request   |
| `--status-only`     | Output status only     |
| `--permission-only` | Output permission only |
| `--id-only`         | Output request ID only |

### `lumos request poll`

Poll a request by ID for up to 5 minutes, waiting for completion.

**Options:**

| Flag           | Description                      |
| -------------- | -------------------------------- |
| `--request-id` | Request ID to poll               |
| `--wait`       | How many minutes to wait (max 5) |

### `lumos request cancel`

Cancel a pending request.

**Options:**

| Flag           | Description             |
| -------------- | ----------------------- |
| `--request-id` | Request ID to cancel    |
| `--reason`     | Reason for cancellation |
