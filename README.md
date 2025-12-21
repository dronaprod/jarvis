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

# Voice commands
jarvis -v                    # Voice mode with Gemini (default)
jarvis -v -m gemini         # Voice mode with Gemini
jarvis -v -m slm             # Voice mode with SLM
jarvis -v -m drona -b <bot_id>  # Voice mode with Drona
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
- ✅ Voice commands - speak commands hands-free

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

### Voice Command Requirements
- Microphone access (for voice mode)
- SpeechRecognition library
- PyAudio library
- PortAudio (install via `brew install portaudio` on macOS)

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

## 🎤 Voice Command Mode

Jarvis supports hands-free voice commands! Simply say "jarvis" followed by your command.

**Usage:**
```bash
jarvis -v                    # Voice mode with Gemini (default)
jarvis -v -m gemini          # Voice mode with Gemini
jarvis -v -m slm              # Voice mode with SLM
jarvis -v -m drona -b <bot_id>  # Voice mode with Drona
```

**How it works:**
1. Start voice mode with `jarvis -v`
2. Say "jarvis" followed by your command
3. Example: "jarvis list files in this directory"
4. Example: "jarvis check if my CPU usage is normal"
5. Jarvis will process your command with full agentic AI support
6. Say "quit" or press Ctrl+C to exit

**Features:**
- ✅ Wake word detection ("jarvis")
- ✅ Full agentic AI iteration support
- ✅ Works with all AI models (Gemini, SLM, Drona)
- ✅ Automatic command output analysis
- ✅ Continuous listening mode

**Requirements:**
- Microphone access
- Internet connection (for Google Speech Recognition)
- SpeechRecognition and PyAudio libraries (auto-installed)

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
