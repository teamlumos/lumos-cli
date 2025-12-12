# CLI Reference

This page provides a complete reference for all Lumos CLI commands with live examples.

## Getting Help

You can get help for any command by using the `--help` flag:

```python
import sys
sys.path.insert(0, "../src")
from lumos_cli.cli import cli
```

```ansi-shell-session
$ cli --help
[94m[1m[4mUsage:[0m [97mcli[0m [36m[2m[OPTIONS][0m [36m[2mCOMMAND [ARGS]...[0m

  Lumos CLI - Command line interface for Lumos

[94m[1m[4mOptions:[0m
  [36m--time[0m / [36m--no-time[0m    Measure and print elapsed execution time.  [2m[[0m[2mdefault: [0m[32m[2m[3mno-
                        time[0m[2m][0m
  [36m--color[0m, [36m--ansi[0m / [36m--no-color[0m, [36m--no-ansi[0m
                        Strip out all colors and all ANSI codes from output.
                        [2m[[0m[2mdefault: [0m[32m[2m[3mcolor[0m[2m][0m
  [36m--config[0m [36m[2mCONFIG_PATH[0m  Location of the configuration file. Supports local path
                        with glob patterns or remote URL.  [2m[[0m[2mdefault:
                        [0m[32m[2m[3m~/.config/cli/*.toml|*.yaml|*.yml|*.json|*.ini[0m[2m][0m
  [36m--no-config[0m           Ignore all configuration files and only use command line
                        parameters and environment variables.
  [36m--show-params[0m         Show all CLI parameters, their provenance, defaults and
                        value, then exit.
  [36m--table-format[0m [[35masciidoc[0m|[35mcsv[0m|[35mcsv-excel[0m|[35mcsv-excel-tab[0m|[35mcsv-unix[0m|[35mdouble-grid[0m|[35mdouble-outline[0m|[35mfancy-grid[0m|[35mfancy-outline[0m|[35mgithub[0m|[35mgrid[0m|[35mheavy-grid[0m|[35mheavy-outline[0m|[35mhtml[0m|[35mjira[0m|[35mlatex[0m|[35mlatex-booktabs[0m|[35mlatex-longtable[0m|[35mlatex-raw[0m|[35mmediawiki[0m|[35mmixed-grid[0m|[35mmixed-outline[0m|[35mmoinmoin[0m|[35morgtbl[0m|[35moutline[0m|[35mpipe[0m|[35mplain[0m|[35mpresto[0m|[35mpretty[0m|[35mpsql[0m|[35mrounded-grid[0m|[35mrounded-outline[0m|[35mrst[0m|[35msimple[0m|[35msimple-grid[0m|[35msimple-outline[0m|[35mtextile[0m|[35mtsv[0m|[35munsafehtml[0m|[35mvertical[0m|[35myoutrack[0m]
                        Rendering style of tables.  [2m[[0m[2mdefault: [0m[32m[2m[3mrounded-[35moutline[0m[0m[2m][0m
  [36m--verbosity[0m [36m[2mLEVEL[0m     Either [35mCRITICAL[0m, [35mERROR[0m, [35mWARNING[0m, [35mINFO[0m, [35mDEBUG[0m.  [2m[[0m[2mdefault:
                        [0m[32m[2m[3mWARNING[0m[2m][0m
  [36m-v[0m, [36m--verbose[0m         Increase the default [35mWARNING[0m verbosity by one level for
                        each additional repetition of the option.  [2m[[0m[2mdefault: [0m[32m[2m[3m0[0m[2m][0m
  [36m--version[0m             Show the version and exit.
  [36m-h[0m, [36m--help[0m            Show this message and exit.

[94m[1m[4mCommands:[0m
  [36mlist[0m     List various Lumos resources
  [36mlogin[0m    Login to your Lumos account via OAuth.
  [36mlogout[0m   Logout of your Lumos account.
  [36mrequest[0m  Request access to an app.
  [36msetup[0m    Setup your Lumos CLI.
  [36mwhoami[0m   Show information about the currently logged in user.
```

## Authentication Commands

### `lumos whoami`

Show information about the currently logged in user.

```ansi-shell-session
$ cli whoami --help
Usage: cli whoami [OPTIONS]

  Show information about the currently logged in user.

Options:
  --username  Show the current user's username only
  --id        Show the current user's ID only
  -h, --help  Show this message and exit.
```

### `lumos setup`

Setup your Lumos CLI authentication. Can be used to login or change your authentication method.

```ansi-shell-session
$ cli setup --help
Usage: cli setup [OPTIONS]

  Setup your Lumos CLI. Can be used to login or change your authentication
  method.

Options:
  -h, --help  Show this message and exit.
```

### `lumos login`

Login to your Lumos account via OAuth. You must be logged in to Lumos on your browser.

```ansi-shell-session
$ cli login --help
Usage: cli login [OPTIONS]

  Login to your Lumos account via OAuth. You must be logged in to Lumos on your
  browser.

Options:
  --admin     Log in as an admin, if you have the permission to do so
  -h, --help  Show this message and exit.
```

### `lumos logout`

Logout of your Lumos account and clear stored credentials.

```ansi-shell-session
$ cli logout --help
Usage: cli logout [OPTIONS]

  Logout of your Lumos account.

Options:
  -h, --help  Show this message and exit.
```

## List Commands

The `list` command group provides access to various Lumos resources.

```ansi-shell-session
$ cli list --help
Usage: cli list [OPTIONS] COMMAND [ARGS]...

  List various Lumos resources

Options:
  --time / --no-time    Measure and print elapsed execution time.  [default: no-
                        time]
  --color, --ansi / --no-color, --no-ansi
                        Strip out all colors and all ANSI codes from output.
                        [default: color]
  --config CONFIG_PATH  Location of the configuration file. Supports local path
                        with glob patterns or remote URL.  [default:
                        ~/.config/cli/*.toml|*.yaml|*.yml|*.json|*.ini]
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
$ cli list apps --help
Usage: cli list apps [OPTIONS]

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
$ cli list users --help
Usage: cli list users [OPTIONS]

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
$ cli list permissions --help
Usage: cli list permissions [OPTIONS]

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
$ cli list groups --help
Usage: cli list groups [OPTIONS]

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
$ cli list requests --help
Usage: cli list requests [OPTIONS]

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
$ cli request --help
Usage: cli request [OPTIONS] COMMAND [ARGS]...

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
                          ~/.config/cli/*.toml|*.yaml|*.yml|*.json|*.ini]
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
