# Homebrew Distribution

The Lumos CLI uses Homebrew as one of its distribution mechanisms. The formula is hosted in the [teamlumos/homebrew-tap](https://github.com/teamlumos/homebrew-tap) repository.

## Automated Updates

The Homebrew formula is automatically updated as part of the [build.yml](../.github/workflows/build.yml) workflow when a new version tag is pushed.

### How it works

1. When a tag (e.g., `v2.1.2`) is pushed, the build workflow creates binaries and uploads them to the GitHub release
2. After all builds complete, the `update-homebrew` job runs
3. It fetches asset information including SHA256 digests from the GitHub release using `gh release view`
4. Updates the formula in homebrew-tap with new version and checksums
5. Commits and pushes changes using the lumos-automations GitHub App

## Multi-Platform Support

The formula supports the following platforms:

- **macOS**: ARM64 (Apple Silicon) and Intel (via Rosetta 2)
- **Linux**: AMD64 (x86_64) and ARM64 (aarch64)

## Formula Template

The formula template is located at [.github/homebrew-templates/lumos.rb.template](../.github/homebrew-templates/lumos.rb.template).

## Required Secrets

The workflow uses the lumos-automations GitHub App (same as the release workflow):

- `GH_BOT_CLIENT_ID` - GitHub App ID
- `GH_BOT_PRIVATE_KEY` - GitHub App private key

## Troubleshooting

If the homebrew update fails, check that:
1. All platform binaries were successfully uploaded to the GitHub release
2. The lumos-automations app has write access to the homebrew-tap repository
3. The release assets include the correct SHA256 digests
