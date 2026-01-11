#!/bin/bash
# Script to prepare release archives for Homebrew formula

set -e

# Get the script directory and project root
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"

VERSION="${1:-1.0.0}"
RELEASE_DIR="$PROJECT_ROOT/releases/v${VERSION}"

echo "📦 Preparing release archives for Jarvis v${VERSION}..."

# Create release directory
mkdir -p "$RELEASE_DIR"

# Check if binaries exist
if [ ! -f "$PROJECT_ROOT/bin/jarvis" ]; then
    echo "❌ Error: bin/jarvis not found. Run ./build.sh first."
    exit 1
fi

# Get architecture
ARCH=$(uname -m)
if [[ "$ARCH" == "arm64" ]]; then
    ARCH_NAME="arm64"
elif [[ "$ARCH" == "x86_64" ]]; then
    ARCH_NAME="amd64"
else
    echo "❌ Unknown architecture: $ARCH"
    exit 1
fi

echo "🏗️  Current architecture: $ARCH_NAME"

# Create temporary directory for archive
TEMP_DIR=$(mktemp -d)
cp "$PROJECT_ROOT/bin/jarvis" "$TEMP_DIR/"

# Create tar.gz archive
ARCHIVE_NAME="jarvis-darwin-${ARCH_NAME}.tar.gz"
cd "$TEMP_DIR"
tar -czf "../${ARCHIVE_NAME}" jarvis
cd - > /dev/null

# Move archive to release directory
mv "${TEMP_DIR}/../${ARCHIVE_NAME}" "$RELEASE_DIR/"
rm -rf "$TEMP_DIR"

# Calculate SHA256
SHA256=$(shasum -a 256 "$RELEASE_DIR/$ARCHIVE_NAME" | cut -d' ' -f1)

echo ""
echo "✅ Archive created: $RELEASE_DIR/$ARCHIVE_NAME"
echo "📏 SHA256: $SHA256"
echo ""
echo "📋 Next steps:"
echo "1. Build for the other architecture (if needed)"
echo "2. Upload archives to GitHub Releases:"
echo "   https://github.com/dronaprod/jarvis/releases/new"
echo "3. Update Formula/jarvis.rb with SHA256 checksums"
echo "4. Commit and push the homebrew-jarvis repository"

