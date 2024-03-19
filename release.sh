poetry install
poetry run pyinstaller --onefile lumos/__main__.py
cp ./dist/__main__ ./dist/lumos

