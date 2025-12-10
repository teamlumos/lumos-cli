# DX-769: Homebrew Distribution Improvements

This document describes the implementation of automated Homebrew formula updates and multi-platform support for the Lumos CLI.

## Overview

This implementation addresses two key requirements from DX-769:
1. **Automate version bumps** in the homebrew-tap repository
2. **Multi-platform support** for macOS and Linux

## Architecture

### Release Flow

```
1. Semantic Release
   └─> Creates tag (e.g., v2.1.2)
   └─> Creates GitHub Release
        │
        └─> 2. Build Workflow (triggered by tag)
            ├─> Builds binaries for all platforms
            ├─> Uploads artifacts to GitHub Release
            │
            └─> 3. Update Homebrew Job (after builds complete)
                └─> Gets SHA256 digests from release
                └─> Updates homebrew-tap formula
                └─> Commits and pushes to homebrew-tap
```

### Components

#### 1. Update Homebrew Job (in `.github/workflows/build.yml`)

**Trigger:**
- Runs after the build job completes, only when a version tag is pushed

**Steps:**
1. Authenticates using lumos-automations GitHub App
2. Checks out homebrew-tap repository
3. Uses `gh release view` to get asset information including SHA256 digests
4. Updates the Homebrew formula with new version and checksums
5. Commits and pushes changes to homebrew-tap

**Key Features:**
- Simple and straightforward - no downloading or calculating checksums locally
- Gets digests directly from GitHub release metadata
- Uses GitHub App authentication (same as release workflow)
- Runs as part of the build workflow, ensuring builds complete first

#### 2. Homebrew Formula

The formula in the homebrew-tap repository supports multiple platforms:
- **macOS**: Apple Silicon (ARM64) and Intel (via Rosetta 2)
- **Linux**: x86_64 (AMD64) and ARM64 (aarch64)

The workflow updates the formula in-place using `sed` to modify:
- Version number
- Download URLs for each platform
- SHA256 checksums for each platform binary


## Setup Requirements

### GitHub Secrets

The following secrets must be configured in the lumos-cli repository:

| Secret Name | Description | Scope |
|------------|-------------|-------|
| `GH_BOT_CLIENT_ID` | GitHub App ID for lumos-automations | Used for authentication |
| `GH_BOT_PRIVATE_KEY` | GitHub App private key for lumos-automations | Used for authentication |

These are the same secrets used by the release workflow and provide access to the homebrew-tap repository.

### GitHub App Permissions

The lumos-automations GitHub App needs:
- Read access to lumos-cli releases
- Write access to homebrew-tap repository contents

## Usage

### Automatic Updates

Homebrew formula updates happen automatically when a version tag is pushed:
1. Tag triggers the build workflow
2. Build workflow creates binaries for all platforms and uploads to GitHub release
3. After builds complete, the `update-homebrew` job runs
4. Formula is updated and committed to homebrew-tap

No manual intervention required!

## Platform Support

### Supported Platforms

| Platform | Architecture | Binary Used |
|----------|-------------|-------------|
| macOS | Apple Silicon (ARM64) | lumos-macos-arm64.tar.gz |
| macOS | Intel (x86_64) | lumos-macos-arm64.tar.gz (via Rosetta 2) |
| Linux | x86_64 (AMD64) | lumos-linux-amd64.tar.gz |
| Linux | ARM64 (aarch64) | lumos-linux-arm64.tar.gz |

### Why Intel Macs Use ARM Binary

Intel Macs use the ARM64 binary via Rosetta 2 because:
1. Rosetta 2 provides excellent compatibility with minimal overhead
2. Reduces complexity by maintaining fewer binary variants
3. Apple has deprecated Intel support, so most users have ARM Macs
4. Homebrew on Intel Macs already has Rosetta 2 installed

If needed in the future, we can add native Intel binaries by:
1. Adding a build job for `macos-13` (Intel runner) in build.yml
2. Updating the formula template to detect Intel and use the Intel binary

## Troubleshooting

### Workflow Fails: "Resource not accessible by integration"

**Cause:** Missing or invalid GitHub App credentials

**Solutions:**
1. Verify `GH_BOT_CLIENT_ID` and `GH_BOT_PRIVATE_KEY` secrets are set
2. Check that lumos-automations app has access to homebrew-tap repository
3. Verify app has write permissions to repository contents

### Formula Installation Fails

**Common issues:**
1. Incorrect SHA256 checksums
   - Check the release assets have valid digests
   - Verify all platform binaries were uploaded successfully
2. Missing artifacts
   - Check release has all required platform binaries (linux-amd64, linux-arm64, macos-arm64)
   - Verify artifact names match expected pattern
3. Formula syntax errors
   - Check the formula in homebrew-tap repository
   - Run `brew audit Formula/lumos.rb` locally

### Manual Formula Update

If automation fails and you need to manually update:

1. Get the release information:
   ```bash
   gh release view v2.1.2 --repo teamlumos/lumos-cli --json assets
   ```

2. Clone homebrew-tap and update Formula/lumos.rb with the new version and SHA256 digests

3. Commit and push:
   ```bash
   git add Formula/lumos.rb
   git commit -m "chore: update lumos to v2.1.2"
   git push
   ```

## Testing the Implementation

### Post-Release Testing

1. Verify the build workflow executed successfully, including the `update-homebrew` job
2. Check homebrew-tap repository for updated formula
3. Test installation:
   ```bash
   brew uninstall lumos || true
   brew untap teamlumos/tap || true
   brew install teamlumos/tap/lumos
   lumos --help
   ```

## Future Enhancements

Potential improvements for consideration:

1. **Intel macOS Support**
   - Add native Intel builds if Rosetta performance is inadequate
   - Update formula to use native Intel binary when available

2. **Prerelease Formula**
   - Create separate `lumos-prerelease.rb` formula
   - Point to latest builds from main branch
   - Useful for beta testing

3. **Windows Support**
   - Investigate Chocolatey or Scoop for Windows distribution
   - Similar automation approach

## Related Files

- `.github/workflows/build.yml` - Builds binaries and updates homebrew formula
- `.github/workflows/release.yml` - Release creation workflow
- `scripts/README.md` - Homebrew distribution documentation

## References

- [Homebrew Formula Cookbook](https://docs.brew.sh/Formula-Cookbook)
- [Homebrew on Linux](https://docs.brew.sh/Homebrew-on-Linux)
- [GitHub Actions: Triggering Workflows](https://docs.github.com/en/actions/using-workflows/triggering-a-workflow)
- [semantic-release](https://semantic-release.gitbook.io/)
