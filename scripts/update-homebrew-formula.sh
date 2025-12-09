#!/bin/bash

# Script to manually update the homebrew formula
# Usage: ./scripts/update-homebrew-formula.sh <version>

set -e

VERSION="${1}"

if [ -z "$VERSION" ]; then
  echo "Usage: $0 <version>"
  echo "Example: $0 2.1.2"
  exit 1
fi

# Remove 'v' prefix if present
VERSION="${VERSION#v}"

echo "Updating Homebrew formula to version ${VERSION}..."

# Check if HOMEBREW_TAP_TOKEN is set
if [ -z "$HOMEBREW_TAP_TOKEN" ]; then
  echo "Warning: HOMEBREW_TAP_TOKEN not set. You may need to authenticate manually."
fi

# Create temporary directory
TMP_DIR=$(mktemp -d)
trap "rm -rf ${TMP_DIR}" EXIT

cd "${TMP_DIR}"

# Clone homebrew-tap repository
echo "Cloning homebrew-tap repository..."
if [ -n "$HOMEBREW_TAP_TOKEN" ]; then
  git clone "https://${HOMEBREW_TAP_TOKEN}@github.com/teamlumos/homebrew-tap.git"
else
  git clone "https://github.com/teamlumos/homebrew-tap.git"
fi

cd homebrew-tap

# Download release artifacts
echo "Downloading release artifacts..."
mkdir -p release-artifacts
cd release-artifacts

for platform in linux-amd64 linux-arm64 macos-arm64; do
  echo "Downloading lumos-${platform}.tar.gz..."
  curl -L -o "lumos-${platform}.tar.gz" \
    "https://github.com/teamlumos/lumos-cli/releases/download/v${VERSION}/lumos-${platform}.tar.gz"
done

# Calculate checksums
echo "Calculating checksums..."
LINUX_AMD64_SHA256=$(sha256sum lumos-linux-amd64.tar.gz | awk '{print $1}')
LINUX_ARM64_SHA256=$(sha256sum lumos-linux-arm64.tar.gz | awk '{print $1}')
MACOS_ARM64_SHA256=$(sha256sum lumos-macos-arm64.tar.gz | awk '{print $1}')

echo "Checksums:"
echo "  linux-amd64: ${LINUX_AMD64_SHA256}"
echo "  linux-arm64: ${LINUX_ARM64_SHA256}"
echo "  macos-arm64: ${MACOS_ARM64_SHA256}"

cd ..

# Update formula
echo "Updating formula..."
cat > Formula/lumos.rb << EOF
class Lumos < Formula
  desc "Lumos command line interface"
  homepage "https://github.com/teamlumos/lumos-cli"
  version "${VERSION}"
  license "MIT"

  on_macos do
    if Hardware::CPU.arm?
      url "https://github.com/teamlumos/lumos-cli/releases/download/v${VERSION}/lumos-macos-arm64.tar.gz"
      sha256 "${MACOS_ARM64_SHA256}"
    else
      # Intel Mac support - use Rosetta to run ARM binary
      url "https://github.com/teamlumos/lumos-cli/releases/download/v${VERSION}/lumos-macos-arm64.tar.gz"
      sha256 "${MACOS_ARM64_SHA256}"
    end
  end

  on_linux do
    if Hardware::CPU.intel?
      url "https://github.com/teamlumos/lumos-cli/releases/download/v${VERSION}/lumos-linux-amd64.tar.gz"
      sha256 "${LINUX_AMD64_SHA256}"
    elsif Hardware::CPU.arm?
      url "https://github.com/teamlumos/lumos-cli/releases/download/v${VERSION}/lumos-linux-arm64.tar.gz"
      sha256 "${LINUX_ARM64_SHA256}"
    end
  end

  def install
    bin.install "lumos"
  end

  test do
    system "#{bin}/lumos", "--help"
  end
end
EOF

echo ""
echo "Updated formula:"
cat Formula/lumos.rb

# Commit and push
git config user.name "Homebrew Update Script"
git config user.email "dev@teamlumos.com"

git add Formula/lumos.rb

if git diff --staged --quiet; then
  echo "No changes to commit"
else
  git commit -m "chore: update lumos to v${VERSION}"
  
  echo ""
  read -p "Push changes to remote? (y/n) " -n 1 -r
  echo
  if [[ $REPLY =~ ^[Yy]$ ]]; then
    git push
    echo "✅ Successfully updated homebrew formula to v${VERSION}"
  else
    echo "Changes not pushed. You can push manually from ${TMP_DIR}/homebrew-tap"
    trap - EXIT  # Don't cleanup on exit so user can inspect
  fi
fi
