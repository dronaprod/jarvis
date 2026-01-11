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

# Get the script directory and project root
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"
CLI_MAIN="$PROJECT_ROOT/cli/main.py"

# Create bin directory if it doesn't exist
mkdir -p "$PROJECT_ROOT/bin"

# Install/upgrade PyInstaller if needed
echo "📥 Checking PyInstaller..."
if ! python3 -m PyInstaller --version > /dev/null 2>&1; then
    echo "📥 Installing PyInstaller..."
    python3 -m pip install --user --upgrade pyinstaller || python3 -m pip install --break-system-packages --upgrade pyinstaller
fi

# Clean previous builds
echo "🧹 Cleaning previous builds..."
rm -rf "$PROJECT_ROOT/build" "$PROJECT_ROOT/dist" "$PROJECT_ROOT"/*.spec
rm -f "$PROJECT_ROOT/bin/jarvis"

# Verify cli/main.py exists
if [ ! -f "$CLI_MAIN" ]; then
    echo "❌ Error: cli/main.py not found at $CLI_MAIN"
    echo "💡 Make sure cli/main.py exists in the project directory"
    exit 1
fi

# Build with PyInstaller
echo "🔨 Building binary with PyInstaller..."
# Change to project root so PyInstaller can properly detect all modules
cd "$PROJECT_ROOT"
python3 -m PyInstaller \
    --name jarvis \
    --onefile \
    --console \
    --clean \
    --noconfirm \
    --hidden-import cli.main \
    --hidden-import cli.parser \
    --hidden-import cli.commands \
    --hidden-import core.jarvis \
    --hidden-import core.ai.base \
    --hidden-import core.ai.gemini \
    --hidden-import core.ai.slm \
    --hidden-import core.ai.drona \
    --hidden-import core.monitoring.network \
    --hidden-import core.monitoring.process \
    --hidden-import core.security.scanner \
    --hidden-import core.voice.voice_mode \
    --hidden-import utils.config \
    --hidden-import utils.notifications \
    --hidden-import utils.system_info \
    --paths . \
    "cli/main.py"

# Copy binary to bin directory
echo "📦 Copying binary to bin/jarvis..."
cp "$PROJECT_ROOT/dist/jarvis" "$PROJECT_ROOT/bin/jarvis"

# Make it executable
chmod +x "$PROJECT_ROOT/bin/jarvis"

# Verify the binary
if [ -f "$PROJECT_ROOT/bin/jarvis" ]; then
    echo "✅ Build successful!"
    echo "📦 Binary location: $PROJECT_ROOT/bin/jarvis"
    echo "📏 Binary size: $(du -h "$PROJECT_ROOT/bin/jarvis" | cut -f1)"
    echo "🏗️  Architecture: $ARCH"
    echo ""
    echo "🧪 Testing binary..."
    "$PROJECT_ROOT/bin/jarvis" --help > /dev/null 2>&1 && echo "✅ Binary works correctly!" || echo "⚠️  Binary may have issues"
    
    # Clean up all build artifacts after successful build
    echo ""
    echo "🧹 Cleaning up build artifacts..."
    rm -rf "$PROJECT_ROOT/build" "$PROJECT_ROOT/dist" "$PROJECT_ROOT/dist-arch" "$PROJECT_ROOT"/*.spec
    echo "✅ Cleaned up build, dist, and dist-arch directories"
else
    echo "❌ Build failed - binary not found"
    exit 1
fi

echo ""
echo "🎉 Done! Binary is ready at: $PROJECT_ROOT/bin/jarvis"
echo ""
echo "💡 To build for both architectures:"
echo "   1. Run this script on an x86_64 Mac: ./build.sh"
echo "   2. Run this script on an arm64 Mac: ./build.sh"
echo "   3. Or use ./build-universal.sh to create a universal binary"

