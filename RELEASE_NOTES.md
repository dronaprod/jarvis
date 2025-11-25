# 🚀 Jarvis v1.0.0 - Release Notes

## Release Title
**Jarvis v1.0.0: AI Terminal Assistant with Secure Configuration**

---

## 🎉 What's New

### ✨ Secure API Key Management
- **No more hardcoded API keys** - All API keys are now stored securely in `~/.jarvis/config.json`
- **Configuration command** - Easy setup with `jarvis configure` command
- **Environment-based storage** - API keys never exposed in code or repositories

### 🔧 Model Configuration System
- **Gemini Configuration**: Configure API key and model name
- **SLM Configuration**: Configure server URL
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

#### Configuration File Location
- **Path**: `~/.jarvis/config.json`
- **Format**: JSON
- **Permissions**: User-readable only

**Example config.json:**
```json
{
  "gemini_api_key": "your-api-key",
  "gemini_model_name": "gemini-2.5-flash",
  "slm_url": "http://35.174.147.167:5000"
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

### 3. Usage

```bash
# Quick question
jarvis "what is an API?"

# Interactive mode
jarvis

# Use specific model
jarvis "your question" -m gemini
jarvis "your question" -m slm
```

---

## ⚡ Features

### 🤖 AI-Powered Terminal Assistant
- **Natural language interface** - Ask questions in plain English
- **Multi-model support** - Choose between Gemini AI or SLM
- **Intelligent command execution** - AI decides when to run commands vs. provide answers
- **Multi-turn conversations** - Context-aware interactions

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

### v1.0.0 (Current)
- ✨ Secure API key configuration system
- ✨ Model configuration for Gemini and SLM
- ✨ Homebrew formula and installation
- ✨ Standalone binary distribution
- 🔒 Removed hardcoded API keys
- 📦 PyInstaller-based packaging
- 🐛 Fixed compatibility with shell aliases

---

**Download**: Available via Homebrew or GitHub Releases  
**Version**: 1.0.0  
**Release Date**: November 2024  
**License**: MIT

