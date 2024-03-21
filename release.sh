#!/bin/bash

escaped_old_version="version = \"$1\""
escaped_new_version="version = \"$2\""

sed -i '' "s/$escaped_old_version/$escaped_new_version/" "./pyproject.toml"
sed -i '' "s/$1/$2/" "./lumos/__init__.py"

git commit -am "Update lumos from $1 to $2"
git push

lumo_cli_directory=$(pwd)

poetry install
rm -rf build dist
poetry run pyinstaller --onefile lumos/__main__.py
cd ./dist
mv __main__ lumos
release_file=$(pwd)/lumos
sha=$(sha256sum lumos | cut -d ' ' -f1)

cd $lumo_cli_directory
cd ../lumos-cli-releases
echo Creating tag $2
git tag "$2"
git push --tags
echo Creating release $2
gh release create $2 --title "$2" --notes "$2" --latest lumos.tar.gz

echo Updating homebrew

cd $lumo_cli_directory
cd ../homebrew-tap/Formula
sed -i '' "s/$1/$2/" "./lumos.rb"
sed -i '' "s/sha256 \".*\"/sha256 \"$sha\"/" "./lumos.rb"
git commit -am "Update lumos from $1 to $2"
git push

cd $lumo_cli_directory

