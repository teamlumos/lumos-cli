#!/bin/bash
old_version=$(cat version.txt)

if [ -z "$1" ]; then
    echo "Please provide a version number"
    exit 1
fi

# exit if old version is same as new version
if [ "$old_version" = "$1" ]; then
    echo "Old version is same as new version. Exiting..."
    exit 1
fi

escaped_old_version="version = \"$old_version\""
escaped_new_version="version = \"$1\""

sed -i '' "s/$escaped_old_version/$escaped_new_version/" "./pyproject.toml"
sed -i '' "s/$old_version/$1/" "./lumos/__init__.py"

echo $1 > version.txt

git commit -am "Update lumos from $old_version to $1"
