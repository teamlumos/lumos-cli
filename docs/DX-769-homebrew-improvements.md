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
        ├─> 2. Build Workflow (triggered by tag)
        │   └─> Builds binaries for all platforms
        │   └─> Uploads artifacts to GitHub Release
        │
        └─> 3. Update Homebrew Formula Workflow (triggered by release published)
            └─> Downloads release artifacts
            └─> Calculates SHA256 checksums
            └─> Updates homebrew-tap formula
            └─> Commits and pushes to homebrew-tap
```

### Components

#### 1. GitHub Actions Workflow (`.github/workflows/update-homebrew-formula.yml`)

**Triggers:**
- Automatically when a release is published
- Manually via workflow dispatch with version input

**Steps:**
1. Checks out both lumos-cli and homebrew-tap repositories
2. Determines the version from the release or manual input
3. Waits for all release artifacts to be available (with timeout)
4. Downloads release artifacts for all platforms
5. Calculates SHA256 checksums
6. Updates the Homebrew formula with new version and checksums
7. Commits and pushes changes to homebrew-tap

**Key Features:**
- Waits up to 15 minutes for build artifacts to be available
- Supports dry-run mode for testing
- Uses GitHub bot authentication
- Automatic retry logic for artifact availability

#### 2. Homebrew Formula Template (`.github/homebrew-templates/lumos.rb.template`)

Multi-platform formula supporting:
- **macOS**:
  - Apple Silicon (ARM64) - native binary
  - Intel - uses ARM binary via Rosetta 2
- **Linux**:
  - x86_64 (AMD64)
  - ARM64 (aarch64)

The formula uses Homebrew's platform detection:
```ruby
on_macos do
  if Hardware::CPU.arm?
    # ARM64 binary
  else
    # Intel Mac uses ARM binary via Rosetta
  end
end

on_linux do
  if Hardware::CPU.intel?
    # x86_64 binary
  elsif Hardware::CPU.arm?
    # ARM64 binary
  end
end
```

#### 3. Helper Scripts

**`scripts/update-homebrew-formula.sh`**
- Manual update script for emergency fixes or testing
- Downloads artifacts and calculates checksums
- Updates formula and optionally pushes to remote
- Requires `HOMEBREW_TAP_TOKEN` environment variable

**`scripts/test-homebrew-formula.sh`**
- Tests formula syntax and installation
- Verifies release artifacts are accessible
- Can perform actual installation for end-to-end testing
- Useful for debugging formula issues

## Setup Requirements

### GitHub Secrets

The following secret must be configured in the lumos-cli repository:

| Secret Name | Description | Scope |
|------------|-------------|-------|
| `HOMEBREW_TAP_TOKEN` | GitHub Personal Access Token with `repo` scope for teamlumos/homebrew-tap | Used by the update workflow to push formula updates |

### Repository Permissions

The GitHub token needs:
- Read access to lumos-cli releases
- Write access to homebrew-tap repository

## Usage

### Automatic Updates

Homebrew formula updates happen automatically when:
1. A new release is published (via semantic-release or manual release creation)
2. The build workflow completes and uploads artifacts
3. The update workflow detects the release and updates the formula

No manual intervention required!

### Manual Updates

If you need to manually update the formula:

```bash
# Set your GitHub token
export HOMEBREW_TAP_TOKEN=ghp_your_token_here

# Run the update script
./scripts/update-homebrew-formula.sh 2.1.2
```

### Testing

Before or after a release, you can test the formula:

```bash
./scripts/test-homebrew-formula.sh 2.1.2
```

This is useful for:
- Verifying formula syntax
- Checking artifact availability
- Testing actual installation

### Manual Workflow Trigger

You can manually trigger the update workflow from GitHub Actions:

1. Go to Actions → Update Homebrew Formula
2. Click "Run workflow"
3. Enter version (e.g., `v2.1.2` or `2.1.2`)
4. Optionally enable dry-run mode
5. Click "Run workflow"

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

### Workflow Fails: "Timeout waiting for release artifacts"

**Cause:** Build workflow hasn't completed uploading artifacts yet

**Solutions:**
1. Wait for build workflow to complete
2. Manually re-run the update workflow
3. Check build workflow for failures

### Workflow Fails: "Resource not accessible by integration"

**Cause:** Missing or invalid `HOMEBREW_TAP_TOKEN` secret

**Solutions:**
1. Verify secret is set in repository settings
2. Check token has `repo` scope
3. Regenerate token if expired

### Formula Installation Fails

**Diagnosis:**
```bash
./scripts/test-homebrew-formula.sh <version>
```

**Common issues:**
1. Incorrect SHA256 checksums
   - Re-run update workflow
   - Manually verify checksums match artifacts
2. Missing artifacts
   - Check release has all required platform binaries
   - Verify artifact names match expected pattern
3. Formula syntax errors
   - Run `brew audit Formula/lumos.rb` locally
   - Check formula template for issues

### Manual Formula Update Needed

If automation fails and you need to manually update:

1. Clone homebrew-tap:
   ```bash
   git clone https://github.com/teamlumos/homebrew-tap.git
   cd homebrew-tap
   ```

2. Download artifacts and calculate checksums:
   ```bash
   VERSION=2.1.2
   curl -LO https://github.com/teamlumos/lumos-cli/releases/download/v${VERSION}/lumos-linux-amd64.tar.gz
   curl -LO https://github.com/teamlumos/lumos-cli/releases/download/v${VERSION}/lumos-linux-arm64.tar.gz
   curl -LO https://github.com/teamlumos/lumos-cli/releases/download/v${VERSION}/lumos-macos-arm64.tar.gz
   
   sha256sum lumos-*.tar.gz
   ```

3. Update `Formula/lumos.rb` with new version and checksums

4. Test and commit:
   ```bash
   brew audit Formula/lumos.rb
   git add Formula/lumos.rb
   git commit -m "chore: update lumos to v${VERSION}"
   git push
   ```

## Testing the Implementation

### Pre-Release Testing

1. Create a test release:
   ```bash
   # From GitHub Actions, manually trigger release workflow with dry-run
   ```

2. Verify workflow behavior:
   ```bash
   # From GitHub Actions, manually trigger update workflow with dry-run
   ```

3. Test formula locally:
   ```bash
   ./scripts/test-homebrew-formula.sh <version>
   ```

### Post-Release Testing

1. Verify workflow executed successfully
2. Check homebrew-tap repository for updated formula
3. Test installation on different platforms:
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

4. **Formula Verification**
   - Add automated testing in update workflow
   - Test formula installation in Docker/VM
   - Verify binary functionality

5. **Rollback Capability**
   - Keep previous formula versions
   - Easy rollback if issues found

## Related Files

- `.github/workflows/update-homebrew-formula.yml` - Main automation workflow
- `.github/workflows/build.yml` - Binary building workflow  
- `.github/workflows/release.yml` - Release creation workflow
- `.github/homebrew-templates/lumos.rb.template` - Formula template
- `scripts/update-homebrew-formula.sh` - Manual update script
- `scripts/test-homebrew-formula.sh` - Testing script
- `scripts/README.md` - Scripts documentation

## References

- [Homebrew Formula Cookbook](https://docs.brew.sh/Formula-Cookbook)
- [Homebrew on Linux](https://docs.brew.sh/Homebrew-on-Linux)
- [GitHub Actions: Triggering Workflows](https://docs.github.com/en/actions/using-workflows/triggering-a-workflow)
- [semantic-release](https://semantic-release.gitbook.io/)
