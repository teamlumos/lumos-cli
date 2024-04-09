poetry run pyinstaller lumos/__main__.py
cd ./dist/__main__
mv __main__ lumos
tar -czf lumos.tar.gz *
FILE_SHA=$(sha256sum lumos.tar.gz | cut -d ' ' -f1)
echo *******************
echo File SHA: $FILE_SHA
echo *******************
