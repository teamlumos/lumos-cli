# Setup

```shell
python -m venv ./venv
source venv/bin/activate
pip install -r requirements.txt
```

## Use 

It is recommended that you create this alias:
`alias lumos='python -m lumos'`

Then you can run commands like:
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

## Development setup

To point towards local API server, add the following lines to `venv/bin/activate`:
```
API_URL=http://localhost:8000
export API_URL

API_KEY=<YOUR_DEVELOPMENT_API_KEY>
export API_KEY
```

and run with `DEV_MODE=true` in the command line, like:

```
DEV_MODE=true lumos whoami
```
You can add `alias lumosdev='DEV_MODE=true python -m lumos'` to your shell as well
