# Homebrew Distribution Scripts

This directory contains scripts to help manage the Homebrew formula for the Lumos CLI.

## Overview

The Lumos CLI uses Homebrew as one of its distribution mechanisms. The formula is hosted in the [teamlumos/homebrew-tap](https://github.com/teamlumos/homebrew-tap) repository.

## Automated Updates

The Homebrew formula is automatically updated when a new release is published via the [update-homebrew-formula.yml](../.github/workflows/update-homebrew-formula.yml) GitHub Actions workflow.

### How it works

1. When a new release is published (tagged with `v*`), the workflow is triggered
2. The workflow downloads all platform-specific release artifacts
3. SHA256 checksums are calculated for each artifact
4. The formula is updated with the new version and checksums
5. Changes are committed and pushed to the homebrew-tap repository

## Manual Updates

If you need to manually update the formula:

```bash
# Set your GitHub token (with repo access to homebrew-tap)
export HOMEBREW_TAP_TOKEN=your_token_here

# Run the update script
./scripts/update-homebrew-formula.sh 2.1.2
```

## Testing

To test the formula before or after an update:

```bash
./scripts/test-homebrew-formula.sh 2.1.2
```

This will:
- Clone the homebrew-tap repository
- Display the current formula
- Run `brew audit` to check formula syntax
- Optionally install and test the formula locally
- Verify that all release artifacts are accessible

## Multi-Platform Support

The formula supports the following platforms:

- **macOS**:
  - ARM64 (Apple Silicon)
  - Intel (via Rosetta 2, using ARM binary)
  
- **Linux**:
  - AMD64 (x86_64)
  - ARM64 (aarch64)

## Formula Template

The formula template is located at [.github/homebrew-templates/lumos.rb.template](../.github/homebrew-templates/lumos.rb.template).

This template uses placeholders that are replaced during the update process:
- `{{VERSION}}` - Version number (without 'v' prefix)
- `{{LINUX_AMD64_SHA256}}` - SHA256 checksum for Linux AMD64 binary
- `{{LINUX_ARM64_SHA256}}` - SHA256 checksum for Linux ARM64 binary
- `{{MACOS_ARM64_SHA256}}` - SHA256 checksum for macOS ARM64 binary

## Required Secrets

The following GitHub secrets are required for the automated workflow:

- `GH_BOT_CLIENT_ID` - GitHub App ID for lumos-automations
- `GH_BOT_PRIVATE_KEY` - GitHub App private key for lumos-automations

These are the same secrets used by the release workflow.

## Troubleshooting

### Workflow fails with "Resource not accessible by integration"

Make sure the lumos-automations GitHub App has access to the homebrew-tap repository with write permissions.

### Formula fails to install

1. Check that all release artifacts exist for the version
2. Verify SHA256 checksums match
3. Run the test script to diagnose issues

### Manual update needed

You can trigger the workflow manually from the GitHub Actions UI:
1. Go to Actions → Update Homebrew Formula
2. Click "Run workflow"
3. Enter the version (e.g., `v2.1.2`)
4. Choose whether to do a dry run

## Related Files

- [update-homebrew-formula.yml](../.github/workflows/update-homebrew-formula.yml) - GitHub Actions workflow
- [lumos.rb.template](../.github/homebrew-templates/lumos.rb.template) - Formula template
- [update-homebrew-formula.sh](./update-homebrew-formula.sh) - Manual update script
- [test-homebrew-formula.sh](./test-homebrew-formula.sh) - Testing script
