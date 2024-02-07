# Use setup

It is reccommended that you create this alias:
`alias lumos='python -m lumos'`

Then you can run commands like:
`lumos request --app [APP] --permission [PERM]`

# Development setup

```shell
python -m venv ./venv
source venv/bin/activate
pip install -r requirements.txt
```

# Structure

`/lumos` - contains the overarching `lumos` command
`/request` - contains the command for requesting an app from appstore (e.g. `lumos request --app [APP] --permission [PERM]`)
