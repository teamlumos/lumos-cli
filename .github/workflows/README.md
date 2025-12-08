# GitHub Actions Workflows

## Build Cross-Platform Binaries

The `build-binaries.yml` workflow automatically builds the Lumos CLI binary for multiple platforms.

### Platforms

- **Linux AMD64** - Built on `ubuntu-latest`
- **Linux ARM64** - Built using Docker with QEMU emulation on `ubuntu-latest`
- **macOS ARM64** - Built on `macos-latest` (Apple Silicon)
- **Windows** - Built on `windows-latest`

### Triggers

The workflow runs on:
- Pull requests to any branch
- Pushes to the `main` branch

### Artifacts

Each platform build produces:
- `lumos-{platform}.tar.gz` - The compressed binary archive
- `lumos-{platform}.tar.gz.sha256` - SHA256 checksum of the archive

Artifacts are stored for 90 days and can be downloaded from the GitHub Actions interface.

### Build Process

The workflow:
1. Checks out the code
2. Sets up Python 3.10.6
3. Installs Poetry and project dependencies
4. Runs PyInstaller to create a standalone binary
5. Packages the binary into a compressed archive
6. Generates a SHA256 checksum
7. Uploads the artifacts to GitHub

### Special Handling

- **Linux ARM64**: Uses Docker with QEMU to cross-compile for ARM64 architecture
- **Windows**: Uses PowerShell commands for file operations and hash generation
- **macOS/Linux**: Uses standard bash commands and utilities

### Usage

To download artifacts from a workflow run:
1. Navigate to the Actions tab in GitHub
2. Select the workflow run
3. Scroll to the Artifacts section
4. Download the platform-specific archive you need

### Notes

- The workflow uses the existing `package.sh` script's PyInstaller approach
- Dependencies are cached to speed up subsequent builds
- Builds fail independently (`fail-fast: false`) to ensure all platforms are attempted
