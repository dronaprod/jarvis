#!/bin/bash
# Build universal binary for Jarvis CLI
# Creates a universal binary supporting both x86_64 and arm64 architectures

set -e

echo "🔨 Building Universal Jarvis CLI binary..."
echo "📦 This will create a binary that works on both Intel and Apple Silicon Macs"
echo ""

# Check if we're on macOS
if [[ "$OSTYPE" != "darwin"* ]]; then
    echo "❌ Error: This build script is for macOS only"
    exit 1
fi

CURRENT_ARCH=$(uname -m)
echo "🖥️  Current architecture: $CURRENT_ARCH"

# Get the script directory and project root
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"
CLI_MAIN="$PROJECT_ROOT/cli/main.py"

# Create directories
mkdir -p "$PROJECT_ROOT/bin"
mkdir -p "$PROJECT_ROOT/dist-arch"

# Verify cli/main.py exists
if [ ! -f "$CLI_MAIN" ]; then
    echo "❌ Error: cli/main.py not found at $CLI_MAIN"
    echo "💡 Make sure cli/main.py exists in the project directory"
    exit 1
fi

# Function to build for a specific architecture
build_for_arch() {
    local arch=$1
    echo ""
    echo "🔨 Building for $arch..."
    
    # Clean previous builds
    rm -rf "$PROJECT_ROOT/build" "$PROJECT_ROOT/dist" "$PROJECT_ROOT"/*.spec
    
    # Build with PyInstaller
    # Change to project root so PyInstaller can properly detect all modules
    cd "$PROJECT_ROOT"
    arch -$arch python3 -m PyInstaller \
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
        "cli/main.py" 2>&1 | grep -E "(INFO|ERROR|WARNING|Building)" || true
    
    # Copy to architecture-specific directory
    if [ -f "$PROJECT_ROOT/dist/jarvis" ]; then
        cp "$PROJECT_ROOT/dist/jarvis" "$PROJECT_ROOT/dist-arch/jarvis-$arch"
        echo "✅ Built successfully for $arch"
    else
        echo "❌ Build failed for $arch"
        return 1
    fi
}

# Check if we can build for both architectures
if [[ "$CURRENT_ARCH" == "arm64" ]]; then
    echo "✅ Running on Apple Silicon - can build for both architectures"
    
    # Build for arm64 (native)
    build_for_arch arm64
    
    # Build for x86_64 (using Rosetta)
    echo ""
    echo "🔨 Building for x86_64 using Rosetta..."
    if arch -x86_64 python3 --version > /dev/null 2>&1; then
        build_for_arch x86_64
    else
        echo "⚠️  Cannot build for x86_64 - Rosetta or x86_64 Python not available"
        echo "💡 To build x86_64 binary, you need:"
        echo "   1. Rosetta 2 installed"
        echo "   2. Python installed for x86_64 architecture"
        echo ""
        echo "📦 Creating arm64-only binary..."
        cp "$PROJECT_ROOT/dist-arch/jarvis-arm64" "$PROJECT_ROOT/bin/jarvis"
        echo "✅ Binary created at $PROJECT_ROOT/bin/jarvis (arm64 only)"
        
        # Clean up all build artifacts before exiting
        echo ""
        echo "🧹 Cleaning up build artifacts..."
        rm -rf "$PROJECT_ROOT/build" "$PROJECT_ROOT/dist" "$PROJECT_ROOT/dist-arch" "$PROJECT_ROOT"/*.spec
        echo "✅ Cleaned up build, dist, and dist-arch directories"
        
        exit 0
    fi
    
    # Create universal binary using lipo
    if [ -f "$PROJECT_ROOT/dist-arch/jarvis-arm64" ] && [ -f "$PROJECT_ROOT/dist-arch/jarvis-x86_64" ]; then
        echo ""
        echo "🔗 Creating universal binary..."
        lipo -create \
            "$PROJECT_ROOT/dist-arch/jarvis-arm64" \
            "$PROJECT_ROOT/dist-arch/jarvis-x86_64" \
            -output "$PROJECT_ROOT/bin/jarvis"
        
        echo "✅ Universal binary created!"
        echo "📦 Binary location: $PROJECT_ROOT/bin/jarvis"
        echo "📏 Binary size: $(du -h "$PROJECT_ROOT/bin/jarvis" | cut -f1)"
        
        # Verify architectures
        echo ""
        echo "🏗️  Architectures in binary:"
        lipo -info "$PROJECT_ROOT/bin/jarvis"
        
        # Test
        echo ""
        echo "🧪 Testing binary..."
        "$PROJECT_ROOT/bin/jarvis" --help > /dev/null 2>&1 && echo "✅ Binary works correctly!" || echo "⚠️  Binary may have issues"
        
        # Clean up all build artifacts after successful build
        echo ""
        echo "🧹 Cleaning up build artifacts..."
        rm -rf "$PROJECT_ROOT/build" "$PROJECT_ROOT/dist" "$PROJECT_ROOT/dist-arch" "$PROJECT_ROOT"/*.spec
        echo "✅ Cleaned up build, dist, and dist-arch directories"
        
    else
        echo "❌ Failed to create universal binary - missing architecture builds"
        exit 1
    fi
    
elif [[ "$CURRENT_ARCH" == "x86_64" ]]; then
    echo "⚠️  Running on Intel Mac - can only build for x86_64"
    echo "💡 To create a universal binary, build on an Apple Silicon Mac"
    build_for_arch x86_64
    cp "$PROJECT_ROOT/dist-arch/jarvis-x86_64" "$PROJECT_ROOT/bin/jarvis"
    echo "✅ Binary created at $PROJECT_ROOT/bin/jarvis (x86_64 only)"
    
    # Clean up all build artifacts after successful build
    echo ""
    echo "🧹 Cleaning up build artifacts..."
    rm -rf "$PROJECT_ROOT/build" "$PROJECT_ROOT/dist" "$PROJECT_ROOT/dist-arch" "$PROJECT_ROOT"/*.spec
    echo "✅ Cleaned up build, dist, and dist-arch directories"
else
    echo "❌ Unknown architecture: $CURRENT_ARCH"
    exit 1
fi

echo ""
echo "🎉 Done! Binary is ready at: $PROJECT_ROOT/bin/jarvis"

