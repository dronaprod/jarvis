#!/bin/bash
# Build script for Jarvis CLI binary
# Creates a standalone binary using PyInstaller for macOS

set -e

echo "🔨 Building Jarvis CLI binary..."

# Get current architecture
ARCH=$(uname -m)
echo "📦 Building for architecture: $ARCH"

# Check if we're on macOS
if [[ "$OSTYPE" != "darwin"* ]]; then
    echo "❌ Error: This build script is for macOS only"
    exit 1
fi

# Create bin directory if it doesn't exist
mkdir -p bin

# Install/upgrade PyInstaller if needed
echo "📥 Checking PyInstaller..."
if ! python3 -m PyInstaller --version > /dev/null 2>&1; then
    echo "📥 Installing PyInstaller..."
    python3 -m pip install --user --upgrade pyinstaller || python3 -m pip install --break-system-packages --upgrade pyinstaller
fi

# Clean previous builds
echo "🧹 Cleaning previous builds..."
rm -rf build dist *.spec
rm -f bin/jarvis

# Get the script directory and project root
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"
JARVIS_SCRIPT="$PROJECT_ROOT/jarvis.py"

# Verify jarvis.py exists
if [ ! -f "$JARVIS_SCRIPT" ]; then
    echo "❌ Error: jarvis.py not found at $JARVIS_SCRIPT"
    echo "💡 Make sure jarvis.py is in the project root directory"
    exit 1
fi

# Build with PyInstaller
echo "🔨 Building binary with PyInstaller..."
python3 -m PyInstaller \
    --name jarvis \
    --onefile \
    --console \
    --clean \
    --noconfirm \
    "$JARVIS_SCRIPT"

# Copy binary to bin directory
echo "📦 Copying binary to bin/jarvis..."
cp dist/jarvis bin/jarvis

# Make it executable
chmod +x bin/jarvis

# Clean up build artifacts (keep dist for verification)
echo "🧹 Cleaning up build artifacts..."
rm -rf build *.spec

# Verify the binary
if [ -f "bin/jarvis" ]; then
    echo "✅ Build successful!"
    echo "📦 Binary location: bin/jarvis"
    echo "📏 Binary size: $(du -h bin/jarvis | cut -f1)"
    echo "🏗️  Architecture: $ARCH"
    echo ""
    echo "🧪 Testing binary..."
    ./bin/jarvis --help > /dev/null 2>&1 && echo "✅ Binary works correctly!" || echo "⚠️  Binary may have issues"
else
    echo "❌ Build failed - binary not found"
    exit 1
fi

echo ""
echo "🎉 Done! Binary is ready at: bin/jarvis"
echo ""
echo "💡 To build for both architectures:"
echo "   1. Run this script on an x86_64 Mac: ./build.sh"
echo "   2. Run this script on an arm64 Mac: ./build.sh"
echo "   3. Or use lipo to create a universal binary (requires both builds)"

