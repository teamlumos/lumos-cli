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

### Automatic Test (Recommended)
Wait for the next release and verify the workflow runs successfully in GitHub Actions.

### Manual Test (Optional)
1. Go to https://github.com/teamlumos/lumos-cli/actions/workflows/update-homebrew-formula.yml
2. Click "Run workflow"
3. Enter a version (e.g., `v2.1.2`)
4. Enable "Dry run"
5. Click "Run workflow"
6. Check the logs to verify it works

## Troubleshooting

If something goes wrong, see:
- [scripts/README.md](scripts/README.md) - Quick reference
- [docs/DX-769-homebrew-improvements.md](docs/DX-769-homebrew-improvements.md) - Detailed troubleshooting

## Manual Updates (Emergency Only)

If automation fails and you need to update manually:

```bash
export HOMEBREW_TAP_TOKEN=your_token_here
./scripts/update-homebrew-formula.sh 2.1.2
```

## Architecture

```
Release Published (v2.1.2)
    ↓
Build Workflow (builds binaries)
    ↓
Update Homebrew Formula Workflow
    ↓
1. Waits for artifacts
2. Downloads all platform binaries
3. Calculates SHA256 checksums
4. Updates Formula/lumos.rb
5. Commits to homebrew-tap
    ↓
Done! Users can: brew install teamlumos/tap/lumos
```

## Questions?

See the full documentation:
- [IMPLEMENTATION_SUMMARY.md](IMPLEMENTATION_SUMMARY.md) - Overview
- [docs/DX-769-homebrew-improvements.md](docs/DX-769-homebrew-improvements.md) - Complete guide
