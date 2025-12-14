# 🚀 Jarvis v1.2.0 - Release Notes

## Release Title
**Jarvis v1.2.0: AI Terminal Assistant with Secure Configuration**

---

## 🎉 What's New

### ✨ Secure API Key Management
- **No more hardcoded API keys** - All API keys are now stored securely in `~/.jarvis/config.json`
- **Configuration command** - Easy setup with `jarvis configure` command
- **Environment-based storage** - API keys never exposed in code or repositories

### 🖼️ Image Support
- **Image queries** - Send images with your questions using `-img` or `--image` flag
- **Multiple formats** - Supports JPEG, PNG, GIF, WebP, and BMP
- **Base64 encoding** - Images automatically encoded and sent to AI models
- **Visual analysis** - Perfect for analyzing screenshots, diagrams, or photos

### 🤖 Drona Model Integration
- **Drona AI support** - New AI model option with bot-based configuration
- **Machine context** - Automatically sends machine details and IP address to Drona API
- **Bot ID configuration** - Configure bot ID via command line or config file
- **Enhanced context** - Drona receives system information for better responses

### 🔧 Model Configuration System
- **Gemini Configuration**: Configure API key and model name (default: gemini-2.5-flash)
- **SLM Configuration**: Configure server URL
- **Drona Configuration**: Configure server URL and bot ID
- **Persistent settings** - Configuration saved automatically and reused

### 📦 Homebrew Installation
- **One-command installation**: `brew install dronaprod/jarvis/jarvis`
- **Standalone binary** - No Python installation required
- **Automatic symlink creation** - Works seamlessly with existing aliases

### 🏗️ Binary Distribution
- **Pre-compiled binaries** for macOS (arm64 and x86_64)
- **21MB standalone executable** - All dependencies included
- **Ready for distribution** - GitHub Releases ready

---

## 📋 Detailed Changes

### 🖼️ Image Support

#### Image Query Feature
Jarvis now supports sending images with queries for visual analysis. This is particularly useful for:
- Analyzing screenshots
- Reading diagrams or charts
- Describing photos
- Troubleshooting visual issues

**Usage:**
```bash
jarvis "what's in this image?" -img path/to/image.jpg
jarvis "analyze this screenshot" -m drona -b <bot-id> -img screenshot.png
```

**Supported Formats:**
- JPEG/JPG
- PNG
- GIF
- WebP
- BMP

**Technical Details:**
- Images are automatically encoded to base64
- MIME type is detected from file extension
- Image data is included in API requests when available
- Works with all AI models (Gemini, SLM, Drona)

### 🤖 Drona Model Integration

#### New AI Model Option
Drona is a new AI model option that provides enhanced context awareness by automatically sending machine details and IP address information.

**Features:**
- Bot-based configuration with unique bot IDs
- Automatic machine context transmission
- IP address detection and inclusion
- System details (CPU, memory, disk, processes, etc.) sent automatically
- Configurable API endpoint

**Usage:**
```bash
# With bot ID from command line
jarvis "your question" -m drona -b <bot-id>

# With bot ID from config
jarvis "your question" -m drona

# Interactive mode
jarvis -m drona -b <bot-id>
```

**Machine Context Sent:**
- System information (OS, release, machine type)
- CPU usage and frequency
- Memory usage and availability
- Disk usage and free space
- Load averages
- Running process count
- Current working directory
- IP address

**Configuration:**
```bash
# Configure bot ID
jarvis configure -m drona -b <bot-id>

# Configure API URL (optional, has default)
jarvis configure -m drona --url <server-url>

# Configure both
jarvis configure -m drona --url <server-url> -b <bot-id>
```

### 🔑 Configuration System

#### New `configure` Command

**Gemini Configuration:**
```bash
jarvis configure -m gemini --api-key <your-api-key> [-n <model-name>]
```

**Examples:**
```bash
# With model name
jarvis configure -m gemini -n 'gemini-2.5-flash' --api-key "your-api-key"

# Without model name (defaults to gemini-2.5-flash)
jarvis configure -m gemini --api-key "your-api-key"

# Different model
jarvis configure -m gemini -n 'gemini-pro' --api-key "your-api-key"
```

**SLM Configuration:**
```bash
jarvis configure -m slm --url <server-url>
```

**Example:**
```bash
jarvis configure -m slm --url http://35.174.147.167:5000
```

**Drona Configuration:**
```bash
jarvis configure -m drona --url <server-url> [-b <bot-id>]
jarvis configure -m drona -b <bot-id> [--url <server-url>]
```

**Examples:**
```bash
# Configure both URL and bot ID
jarvis configure -m drona --url https://api.vtorlabs.com/drona/v1/jarvis/chat -b your-bot-id

# Configure bot ID only (uses default URL)
jarvis configure -m drona -b your-bot-id

# Configure URL only (bot ID must be provided at runtime)
jarvis configure -m drona --url https://api.vtorlabs.com/drona/v1/jarvis/chat
```

#### Configuration File Location
- **Path**: `~/.jarvis/config.json`
- **Format**: JSON
- **Permissions**: User-readable only

**Example config.json:**
```json
{
  "gemini_api_key": "your-api-key",
  "gemini_model_name": "gemini-2.5-flash",
  "slm_url": "http://35.174.147.167:5000",
  "drona_url": "https://api.vtorlabs.com/drona/v1/jarvis/chat",
  "drona_bot_id": "your-bot-id"
}
```

### 🍺 Homebrew Installation

#### Installation
```bash
# Add tap and install
brew tap dronaprod/jarvis
brew install jarvis

# Or install directly
brew install dronaprod/jarvis/jarvis
```

#### Features
- ✅ Automatic binary installation
- ✅ Symlink creation at `~/.local/bin/jarvis` for compatibility
- ✅ Works with existing shell aliases
- ✅ Easy updates with `brew upgrade jarvis`

### 📦 Binary Distribution

#### Build System
- **Build script**: `./build.sh` - Creates binary for current architecture
- **Universal build**: `./build-universal.sh` - Creates universal binary (arm64 + x86_64)
- **Release preparation**: `./prepare-release.sh` - Creates release archives

#### Binary Details
- **Size**: ~21MB
- **Architecture**: arm64 (Apple Silicon) and x86_64 (Intel)
- **Dependencies**: All bundled (no external dependencies)
- **Python version**: Built with Python 3.13
- **Packaging**: PyInstaller 6.16.0

---

## 🚀 Quick Start Guide

### 1. Installation

**Option A: Homebrew (Recommended)**
```bash
brew install dronaprod/jarvis/jarvis
```

**Option B: Direct Binary**
```bash
# Download binary from GitHub Releases
# Make executable and add to PATH
```

**Option C: Python Script**
```bash
bash install_jarvis_user.sh
source ~/.bashrc
```

### 2. Configuration

**Configure Gemini:**
```bash
# Get API key from: https://makersuite.google.com/app/apikey
jarvis configure -m gemini --api-key "your-api-key"
```

**Configure SLM (optional):**
```bash
jarvis configure -m slm --url "http://your-slm-server:5000"
```

**Configure Drona (optional):**
```bash
jarvis configure -m drona -b "your-bot-id"
jarvis configure -m drona --url "https://api.vtorlabs.com/drona/v1/jarvis/chat" -b "your-bot-id"
```

### 3. Usage

```bash
# Quick question
jarvis "what is an API?"

# Interactive mode
jarvis

# Use specific model
jarvis "your question" -m gemini
jarvis "your question" -m slm
jarvis "your question" -m drona -b <bot-id>

# Send image with query
jarvis "what's in this image?" -img path/to/image.jpg
jarvis "analyze this screenshot" -m drona -b <bot-id> -img screenshot.png
```

---

## ⚡ Features

### 🤖 AI-Powered Terminal Assistant
- **Natural language interface** - Ask questions in plain English
- **Multi-model support** - Choose between Gemini AI, SLM, or Drona
- **Intelligent command execution** - AI decides when to run commands vs. provide answers
- **Multi-turn conversations** - Context-aware interactions
- **Image analysis** - Send images with queries for visual analysis
- **Machine context** - Drona model receives system details and IP address automatically

### 💻 System Management
- **System health monitoring** - CPU, memory, disk usage analysis
- **Process management** - View and analyze running processes
- **Network monitoring** - Check network connections and activity
- **Comprehensive diagnostics** - Complete system health reports

### ⚡ Command Execution
- **Direct command execution** - AI can run macOS/Unix commands
- **Smart analysis** - AI analyzes command outputs and provides insights
- **Multi-step workflows** - Handles complex tasks requiring multiple commands
- **Safe execution** - Timeout protection and error handling

### 🎯 Interactive Mode
- **Interactive terminal interface** - Continuous conversation mode
- **Quick commands** - Shortcuts for common tasks (cpu, memory, disk, etc.)
- **Help system** - Built-in help and examples
- **Clean interface** - Organized output with clear formatting

---

## 🔒 Security Improvements

### API Key Management
- ✅ **No hardcoded keys** - Removed all hardcoded API keys from source code
- ✅ **Secure storage** - API keys stored in user's home directory
- ✅ **Git-safe** - Configuration file excluded from version control
- ✅ **User permissions** - Config file readable only by owner

### Best Practices
- 🔐 Never commit API keys to repositories
- 🔐 Keep `~/.jarvis/config.json` secure
- 🔐 Use environment variables for CI/CD if needed
- 🔐 Rotate API keys regularly

---

## 📝 Breaking Changes

### API Key Configuration Required
- **Previous versions**: Had hardcoded API key (now disabled by Google)
- **v1.0.0**: Requires manual configuration using `jarvis configure` command
- **Migration**: Run `jarvis configure -m gemini --api-key <your-key>` after installation

### Configuration File Location
- **New location**: `~/.jarvis/config.json`
- **Old behavior**: No configuration file existed
- **Migration**: Automatic - first run will prompt for configuration

---

## 🐛 Known Issues

- Binary is currently built for arm64 only (universal binary available via `build-universal.sh`)
- Requires internet connection for AI functionality
- Some advanced features may require system permissions
- SLM server URL defaults to `http://35.174.147.167:5000` if not configured
- Drona model requires bot ID (either from config or command line)
- Image support requires valid image file paths

---

## 📦 Installation Requirements

### System Requirements
- **macOS** 10.13 or later
- **Architecture**: arm64 (Apple Silicon) or x86_64 (Intel)
- **Internet connection** (for AI model access)
- **No Python installation needed** (for binary version)

### Dependencies (for Python version)
- Python 3.7+
- google-generativeai
- psutil
- requests

---

## 🔄 Upgrade Instructions

### From Previous Versions

1. **Install new version:**
   ```bash
   brew upgrade jarvis
   # or reinstall binary
   ```

2. **Configure API key:**
   ```bash
   jarvis configure -m gemini --api-key <your-api-key>
   ```

3. **Test installation:**
   ```bash
   jarvis "test"
   ```

---

## 📚 Documentation

- **README.md** - Quick start guide
- **Homebrew Formula** - `homebrew-jarvis/Formula/jarvis.rb`
- **Build Scripts** - `build.sh`, `build-universal.sh`, `prepare-release.sh`

---

## 🙏 Credits

Built with:
- Python 3.13
- Google Gemini AI
- PyInstaller
- psutil, requests, and other open-source libraries

---

## 🔗 Links

- **GitHub Repository**: https://github.com/dronaprod/jarvis
- **Homebrew Tap**: https://github.com/dronaprod/homebrew-jarvis
- **Gemini API Key**: https://makersuite.google.com/app/apikey
- **Issues**: https://github.com/dronaprod/jarvis/issues

---

## 📊 Version History

### v1.2.0 (Current)
- ✨ Secure API key configuration system
- ✨ Model configuration for Gemini, SLM, and Drona
- ✨ Drona AI model integration with machine context
- ✨ Image support for visual analysis queries
- ✨ Automatic machine details and IP address transmission (Drona)
- ✨ Standalone binary distribution
- 📦 PyInstaller-based packaging
- 🐛 Fixed compatibility with shell aliases
- 🔧 Default Gemini model set to gemini-2.5-flash

### v1.1.0
- ✨ Secure API key configuration system
- ✨ Model configuration for Gemini and SLM
- ✨ Standalone binary distribution
- 📦 PyInstaller-based packaging
- 🐛 Fixed compatibility with shell aliases
- 🔧 Default Gemini model set to gemini-2.5-flash

---

**Download**: Available via Homebrew or GitHub Releases  
**Version**: 1.2.0  
**Release Date**: November 2024  
**License**: MIT

