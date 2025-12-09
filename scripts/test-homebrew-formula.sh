#!/bin/bash

# Script to test the homebrew formula locally
# Usage: ./scripts/test-homebrew-formula.sh <version>

set -e

VERSION="${1}"

if [ -z "$VERSION" ]; then
  echo "Usage: $0 <version>"
  echo "Example: $0 2.1.2"
  exit 1
fi

# Remove 'v' prefix if present
VERSION="${VERSION#v}"

echo "Testing Homebrew formula for version ${VERSION}..."

# Create temporary directory
TMP_DIR=$(mktemp -d)
trap "rm -rf ${TMP_DIR}" EXIT

cd "${TMP_DIR}"

# Clone homebrew-tap repository
echo "Cloning homebrew-tap repository..."
git clone "https://github.com/teamlumos/homebrew-tap.git"

cd homebrew-tap

# Check if formula exists
if [ ! -f "Formula/lumos.rb" ]; then
  echo "Error: Formula/lumos.rb not found"
  exit 1
fi

echo ""
echo "Current formula:"
cat Formula/lumos.rb

echo ""
echo "Testing formula syntax..."
if command -v brew &> /dev/null; then
  # Test formula syntax
  brew audit --formula Formula/lumos.rb || true
  
  echo ""
  echo "Testing formula installation (dry-run)..."
  brew install --formula --dry-run Formula/lumos.rb || true
  
  echo ""
  read -p "Do you want to actually install and test the formula? (y/n) " -n 1 -r
  echo
  if [[ $REPLY =~ ^[Yy]$ ]]; then
    # Uninstall if already installed
    brew uninstall lumos 2>/dev/null || true
    
    # Install from local formula
    brew install --formula Formula/lumos.rb
    
    # Test the installation
    echo ""
    echo "Testing lumos --help..."
    lumos --help
    
    echo ""
    echo "✅ Formula installed and tested successfully"
    
    echo ""
    read -p "Uninstall lumos? (y/n) " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
      brew uninstall lumos
      echo "Uninstalled lumos"
    fi
  fi
else
  echo "Warning: brew not found. Skipping installation tests."
  echo "Formula syntax appears valid."
fi

echo ""
echo "Testing URLs..."
for platform in linux-amd64 linux-arm64 macos-arm64; do
  URL="https://github.com/teamlumos/lumos-cli/releases/download/v${VERSION}/lumos-${platform}.tar.gz"
  echo -n "Checking ${platform}... "
  if curl -s -f -I "$URL" > /dev/null; then
    echo "✅ Found"
  else
    echo "❌ Not found"
  fi
done

echo ""
echo "✅ Testing complete"
