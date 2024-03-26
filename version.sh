#!/bin/bash
escaped_old_version="version = \"$1\""
escaped_new_version="version = \"$2\""

sed -i '' "s/$escaped_old_version/$escaped_new_version/" "./pyproject.toml"
sed -i '' "s/$1/$2/" "./lumos/__init__.py"

git commit -am "Update lumos from $1 to $2"
git push
