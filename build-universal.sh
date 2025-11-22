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

# Create directories
mkdir -p bin
mkdir -p dist-arch

# Function to build for a specific architecture
build_for_arch() {
    local arch=$1
    echo ""
    echo "🔨 Building for $arch..."
    
    # Clean previous builds
    rm -rf build dist *.spec
    
    # Build with PyInstaller
    arch -$arch python3 -m PyInstaller \
        --name jarvis \
        --onefile \
        --console \
        --clean \
        --noconfirm \
        jarvis.py 2>&1 | grep -E "(INFO|ERROR|WARNING|Building)" || true
    
    # Copy to architecture-specific directory
    if [ -f "dist/jarvis" ]; then
        cp dist/jarvis "dist-arch/jarvis-$arch"
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
        cp dist-arch/jarvis-arm64 bin/jarvis
        echo "✅ Binary created at bin/jarvis (arm64 only)"
        exit 0
    fi
    
    # Create universal binary using lipo
    if [ -f "dist-arch/jarvis-arm64" ] && [ -f "dist-arch/jarvis-x86_64" ]; then
        echo ""
        echo "🔗 Creating universal binary..."
        lipo -create \
            dist-arch/jarvis-arm64 \
            dist-arch/jarvis-x86_64 \
            -output bin/jarvis
        
        echo "✅ Universal binary created!"
        echo "📦 Binary location: bin/jarvis"
        echo "📏 Binary size: $(du -h bin/jarvis | cut -f1)"
        
        # Verify architectures
        echo ""
        echo "🏗️  Architectures in binary:"
        lipo -info bin/jarvis
        
        # Test
        echo ""
        echo "🧪 Testing binary..."
        ./bin/jarvis --help > /dev/null 2>&1 && echo "✅ Binary works correctly!" || echo "⚠️  Binary may have issues"
        
    else
        echo "❌ Failed to create universal binary - missing architecture builds"
        exit 1
    fi
    
elif [[ "$CURRENT_ARCH" == "x86_64" ]]; then
    echo "⚠️  Running on Intel Mac - can only build for x86_64"
    echo "💡 To create a universal binary, build on an Apple Silicon Mac"
    build_for_arch x86_64
    cp dist-arch/jarvis-x86_64 bin/jarvis
    echo "✅ Binary created at bin/jarvis (x86_64 only)"
else
    echo "❌ Unknown architecture: $CURRENT_ARCH"
    exit 1
fi

echo ""
echo "🎉 Done! Binary is ready at: bin/jarvis"

