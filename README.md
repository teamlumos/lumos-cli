# Use setup

It is reccommended that you create this alias:
`alias lumos='python -m lumos'`

Then you can run commands like:
`lumos request`
`lumos list apps --like sales`
`lumos list users --like Albus`
`lumos request --app-like github --permission-like dev --reason "Dev access"`
# Development setup

```shell
python -m venv ./venv
source venv/bin/activate
pip install -r requirements.txt
```
