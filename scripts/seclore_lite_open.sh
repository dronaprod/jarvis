#!/bin/bash

# Seclore Lite File Opener
# Quits TextEdit and opens file with Seclore Lite

FILE_PATH="$1"

if [ -z "$FILE_PATH" ]; then
    echo "Usage: $0 <file_path>"
    echo "Example: $0 test.txt"
    exit 1
fi

if [ ! -f "$FILE_PATH" ]; then
    echo "❌ Error: File '$FILE_PATH' does not exist"
    exit 1
fi

echo "🔒 Opening file with Seclore Lite: $FILE_PATH"

# Get absolute path
ABSOLUTE_PATH=$(realpath "$FILE_PATH")

# Quit TextEdit
echo "🔄 Quitting TextEdit..."
osascript -e 'quit app "TextEdit"'

# Open file with Seclore Lite
echo "🚀 Opening file with Seclore Lite..."
open -a "Seclore Lite" "$ABSOLUTE_PATH"

if [ $? -eq 0 ]; then
    echo "✅ File opened successfully with Seclore Lite!"
    
    # Wait a moment for the app to open
    sleep 2
    
    # Activate the Seclore Lite window
    echo "🔄 Activating Seclore Lite window..."
    osascript -e 'tell application "Seclore Lite" to activate'
    
    if [ $? -eq 0 ]; then
        echo "✅ Seclore Lite window activated!"
    else
        echo "⚠️ Could not activate Seclore Lite window (app may not be running)"
    fi
else
    echo "❌ Failed to open file with Seclore Lite"
    echo "💡 Make sure Seclore Lite is installed"
fi
