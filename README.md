# 🤖 Jarvis AI Assistant

Your personal AI assistant for macOS - Terminal Interface

## 🚀 Quick Start

### Installation (One-time)
```bash
bash install_jarvis_user.sh
source ~/.bashrc
```

### Usage
```bash
jarvis "your question"
jarvis              # Interactive mode
```

## 💬 Example Commands

```bash
# Basic usage
jarvis "list files"
jarvis "what's my disk space?"
jarvis "open finder here"
jarvis "check system health"
jarvis "show running processes"

# Use different AI models
jarvis "your question" -m gemini    # Use Gemini (default)
jarvis "your question" -m slm       # Use SLM server
jarvis "your question" -m drona -b <bot_id>  # Use Drona model

# Send images with queries
jarvis "what's in this image?" -img path/to/image.jpg
jarvis "analyze this screenshot" -m drona -b <bot_id> -img screenshot.png
```

## ⚡ Features

- ✅ Works in any terminal
- ✅ System health monitoring  
- ✅ Multi-turn conversations
- ✅ Direct command execution
- ✅ Natural language interface
- ✅ Multiple AI models: Gemini, SLM, and Drona
- ✅ Image support - send images with queries
- ✅ Machine context awareness (for Drona model)

## 📁 Files

- `jarvis.py` - Main application
- `install_jarvis_user.sh` - Installation script
- `requirements.txt` - Dependencies
- `~/.local/bin/jarvis` - Global command (after install)

## 🔧 Requirements

- Python 3.7+
- macOS
- Internet connection
- Dependencies auto-installed

### Supported Image Formats
- JPEG/JPG
- PNG
- GIF
- WebP
- BMP

## 🎯 Interactive Mode

```bash
jarvis                    # Interactive mode with Gemini (default)
jarvis -m slm             # Interactive mode with SLM
jarvis -m drona -b <bot_id>  # Interactive mode with Drona
```

Then type commands directly:
- `help` - Show help
- `test` - Test system
- `system` - System health check
- `cpu` - CPU usage
- `memory` - Memory usage
- `disk` - Disk usage
- Any question!

## 🔧 Configuration

### Configure Gemini
```bash
jarvis configure -m gemini --api-key <your-api-key> [-n <model-name>]
# Example: jarvis configure -m gemini -n 'gemini-2.5-flash' --api-key 'your-key'
# Get API key from: https://makersuite.google.com/app/apikey
```

### Configure SLM
```bash
jarvis configure -m slm --url <server-url>
# Example: jarvis configure -m slm --url http://35.174.147.167:5000
```

### Configure Drona
```bash
jarvis configure -m drona --url <server-url> [-b <bot-id>]
# Or configure bot ID only:
jarvis configure -m drona -b <bot-id>
```

Configuration is saved to `~/.jarvis/config.json`

## 🎉 Enjoy Jarvis!

Your AI-powered terminal assistant is ready!
# jarvis
