#!/bin/bash

# Jarvis User Installation Script (No sudo required)
echo "🚀 Installing Jarvis - Global Terminal AI Copilot (User Mode)..."

# Get the directory where this script is located
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"
JARVIS_SCRIPT="$PROJECT_ROOT/jarvis.py"

# Verify jarvis.py exists
if [ ! -f "$JARVIS_SCRIPT" ]; then
    echo "❌ Error: jarvis.py not found at $JARVIS_SCRIPT"
    echo "💡 Make sure jarvis.py is in the project root directory"
    exit 1
fi

# Create jarvis_files directory in user's local bin
JARVIS_FILES_DIR="$HOME/.local/bin/jarvis_files"
mkdir -p "$JARVIS_FILES_DIR"

# Copy jarvis.py to the new location (avoids Desktop permission issues)
echo "📁 Copying files to secure location..."
cp "$JARVIS_SCRIPT" "$JARVIS_FILES_DIR/jarvis.py"

# Remove extended attributes and make executable
xattr -c "$JARVIS_FILES_DIR/jarvis.py" 2>/dev/null || true
chmod +x "$JARVIS_FILES_DIR/jarvis.py"
chmod +x "$JARVIS_FILES_DIR/seclore_lite_open.sh" 2>/dev/null || true

# Update the script path to use the new location
JARVIS_SCRIPT="$JARVIS_FILES_DIR/jarvis.py"

# Check if Python 3 is available
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is required but not installed."
    exit 1
fi

# Install required Python packages
echo "📦 Installing required Python packages..."
pip3 install --break-system-packages google-generativeai==0.3.2 psutil==5.9.6 requests==2.31.0

# Create the jarvis command in user's home directory
echo "🔧 Setting up jarvis command in your home directory..."

# Create ~/.local/bin if it doesn't exist
mkdir -p ~/.local/bin

# Create a wrapper script
cat > ~/.local/bin/jarvis << EOF
#!/bin/bash
# Use jarvis from the user's local bin directory (avoids Desktop permission issues)
JARVIS_SCRIPT="\$HOME/.local/bin/jarvis_files/jarvis.py"
python3 "\$JARVIS_SCRIPT" "\$@"
EOF

# Make it executable
chmod +x ~/.local/bin/jarvis

# Add ~/.local/bin to PATH if not already there
if [[ ":$PATH:" != *":$HOME/.local/bin:"* ]]; then
    echo ""
    echo "🔧 Adding ~/.local/bin to your PATH..."
    
    # Detect shell and add to appropriate config file
    if [[ "$SHELL" == *"zsh"* ]]; then
        CONFIG_FILE="$HOME/.zshrc"
    elif [[ "$SHELL" == *"bash"* ]]; then
        CONFIG_FILE="$HOME/.bashrc"
    else
        CONFIG_FILE="$HOME/.profile"
    fi
    
    echo 'export PATH="$HOME/.local/bin:$PATH"' >> "$CONFIG_FILE"
    echo "✅ Added ~/.local/bin to $CONFIG_FILE"
    echo "🔄 Please run 'source $CONFIG_FILE' or restart your terminal"
fi

# Add jarvis alias to shell config
echo ""
echo "🔧 Adding jarvis alias to your shell configuration..."

# Detect shell and add alias to appropriate config file
if [[ "$SHELL" == *"zsh"* ]]; then
    CONFIG_FILE="$HOME/.zshrc"
elif [[ "$SHELL" == *"bash"* ]]; then
    CONFIG_FILE="$HOME/.bashrc"
else
    CONFIG_FILE="$HOME/.profile"
fi

# Add alias if not already present
if ! grep -q "alias jarvis=" "$CONFIG_FILE"; then
    echo "alias jarvis='~/.local/bin/jarvis'" >> "$CONFIG_FILE"
    echo "✅ Added jarvis alias to $CONFIG_FILE"
else
    echo "✅ Jarvis alias already exists in $CONFIG_FILE"
fi

# Test the installation
echo "🧪 Testing installation..."
if [ -f ~/.local/bin/jarvis ]; then
    echo "✅ Jarvis installed successfully!"
    echo ""
    echo "🎉 You can now use Jarvis from anywhere:"
    echo "   • Open any terminal"
    echo "   • Type 'jarvis' and press Enter"
    echo "   • Start chatting with your AI assistant!"
    echo ""
    echo "💡 Example usage:"
    echo "   jarvis                    # Start interactive mode"
    echo "   jarvis 'list files'       # Run a single command"
    echo ""
    echo "🔄 If 'jarvis' command is not found, run:"
    echo "   source $CONFIG_FILE"
    echo "   or restart your terminal"
    echo ""
else
    echo "❌ Installation failed."
    exit 1
fi

echo "🚀 Installation complete!"
