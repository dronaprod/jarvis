# Jarvis Scripts

This directory contains build and installation scripts for Jarvis.

## Scripts

- **`build.sh`** - Build binary for current architecture using modular structure
- **`build-universal.sh`** - Build universal binary (arm64 + x86_64) using modular structure
- **`prepare-release.sh`** - Prepare release archives
- **`install_jarvis_user.sh`** - Install jarvis for current user (modular structure)

## Usage

### Build Binary
```bash
cd "Desktop Copilot"
./scripts/build.sh
```

This builds a standalone binary from `cli/main.py` and includes all modular components (core, utils, cli).

### Build Universal Binary
```bash
cd "Desktop Copilot"
./scripts/build-universal.sh
```

Creates a universal binary that works on both Intel and Apple Silicon Macs.

### Prepare Release
```bash
cd "Desktop Copilot"
./scripts/prepare-release.sh [version]
```

Prepares release archives for distribution. Requires `bin/jarvis` to exist (run build script first).

### Install for User
```bash
cd "Desktop Copilot"
bash scripts/install_jarvis_user.sh
```

Installs jarvis in user's local directory (`~/.local/bin/jarvis`) using the modular structure. No sudo required.

## Project Structure

The scripts now work with the modular project structure:
- Entry point: `cli/main.py`
- Core functionality: `core/` directory
- Utilities: `utils/` directory
- CLI interface: `cli/` directory

