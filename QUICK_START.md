# Quick Start: Homebrew Automation Setup

This guide will help you verify the automated Homebrew formula updates for the Lumos CLI.

## Prerequisites

✅ All code is already in place and ready to use!
✅ GitHub App authentication is already configured (same as release workflow)

## Verification

### Check Existing Setup

The workflow uses the lumos-automations GitHub App with these secrets:
- `GH_BOT_CLIENT_ID` 
- `GH_BOT_PRIVATE_KEY`

These should already be configured if the release workflow is working.

### Verify App Permissions

Ensure the lumos-automations app has:
- ✅ Read access to lumos-cli repository
- ✅ Write access to homebrew-tap repository

## That's It! 🎉

The automation is now active and will:
- ✅ Automatically update the Homebrew formula on each release
- ✅ Support macOS (Intel & Apple Silicon) and Linux (AMD64 & ARM64)
- ✅ Calculate and update SHA256 checksums
- ✅ Commit and push changes to homebrew-tap using the lumos-automations app

## Testing

Wait for the next version tag to be pushed and verify:
1. The build workflow runs successfully
2. The `update-homebrew` job completes after builds
3. The formula is updated in homebrew-tap repository

## Troubleshooting

If something goes wrong, see:
- [scripts/README.md](scripts/README.md) - Quick reference
- [docs/DX-769-homebrew-improvements.md](docs/DX-769-homebrew-improvements.md) - Detailed troubleshooting

## Architecture

```
Tag Pushed (v2.1.2)
    ↓
Build Workflow
    ↓
Build Job: Creates binaries for all platforms
    ↓
Update Homebrew Job (after builds complete)
    ↓
1. Gets SHA256 digests from GitHub release
2. Updates Formula/lumos.rb
3. Commits to homebrew-tap
    ↓
Done! Users can: brew install teamlumos/tap/lumos
```

## Questions?

See the full documentation:
- [IMPLEMENTATION_SUMMARY.md](IMPLEMENTATION_SUMMARY.md) - Overview
- [docs/DX-769-homebrew-improvements.md](docs/DX-769-homebrew-improvements.md) - Complete guide
