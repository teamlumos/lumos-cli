# Setup

```shell
python -m venv ./venv
source venv/bin/activate
pip install -r requirements.txt
```

## Use setup

It is reccommended that you create this alias:
`alias lumos='python -m lumos'`

Then you can run commands like:
`lumos request`
`lumos list apps --like sales`
`lumos list users --like Albus`
`lumos request --app-like github --permission-like dev --reason "Dev access"`

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
