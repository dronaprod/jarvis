# 🚀 Jarvis v1.5.0 - Release Notes

## Release Title
**Jarvis v1.5.0: Network Monitoring & Real-time Security Alerts**

---

## 🎉 What's New

### 🔍 Process Monitoring with AI Security Analysis (NEW!)
- **Real-time process monitoring** - Monitor all running processes for threats and anomalies
- **Malware detection** - Identifies cryptominers, ransomware, keyloggers, backdoors, trojans
- **Resource abuse detection** - Catches unusual CPU/memory usage patterns
- **Behavioral analysis** - Detects suspicious process behaviors and patterns
- **File operation monitoring** - Identifies file deletion/corruption attempts
- **Desktop notifications** - Instant alerts for suspicious processes (macOS, Linux, Windows)
- **AI threat classification** - Categorizes threats (malware/ransomware/cryptominer/etc.)
- **Comprehensive threat indicators** - Analyzes paths, names, commands, resources
- **Baseline learning** - Establishes normal behavior for each process
- **Actionable recommendations** - Specific guidance (Allow, Monitor, Terminate, Block)

### 🌐 Network Monitoring with AI Threat Analysis
- **Real-time monitoring** - Monitor outbound network connections from background applications
- **Desktop notifications** - Sends alerts to system notification center (macOS, Linux, Windows)
- **Enhanced notifications** - Special HIGH/CRITICAL threat alerts with detailed information
- **Cross-platform support** - Works on macOS (Notification Center), Linux (notify-send), Windows (PowerShell)
- **Instant alerts** - Get immediate alerts when new connections are detected
- **Detailed analysis** - View process information, network details, and remote IP analysis
- **AI-powered threat assessment** - Uses AI to analyze connections for suspicious activity
- **Threat levels** - Categorizes threats as LOW, MEDIUM, HIGH, or CRITICAL
- **Actionable recommendations** - Provides specific guidance (Allow, Investigate, Block)
- **Continuous monitoring** - Runs continuously until stopped with Ctrl+C
- **Baseline establishment** - Establishes baseline connections to detect only new activity

### 🔍 Security Scanning Feature (Drona Only)
- **Folder scanning** - Scan entire folders for sensitive files
- **AI-powered detection** - Uses Drona LLM to analyze file content for sensitive information
- **Comprehensive analysis** - Detects API keys, credentials, PII, financial data, and more
- **Detailed reporting** - Provides sensitivity levels, reasons, and protection recommendations
- **Markdown content extraction** - Extracts up to 10,000 characters per file with proper structure
- **Recursive scanning** - Automatically scans all subdirectories
- **Progress tracking** - Shows real-time progress during scan

### ✨ Secure API Key Management
- **No more hardcoded API keys** - All API keys are now stored securely in `~/.jarvis/config.json`
- **Configuration command** - Easy setup with `jarvis configure` command
- **Environment-based storage** - API keys never exposed in code or repositories

### 🎤 Voice Command Support
- **Hands-free operation** - Speak commands instead of typing
- **Wake word detection** - Say "jarvis" followed by your command
- **Full agentic AI support** - Voice commands use the same intelligent iteration as text commands
- **Continuous listening** - Keeps listening for multiple commands
- **Multi-model support** - Works with Gemini, SLM, and Drona models

### 🤖 Enhanced Agentic AI Iteration
- **Improved iteration flow** - Better handling of intermediate vs. last commands
- **Automatic command output analysis** - AI receives command outputs and continues iterating
- **Smart command detection** - Automatically converts analysis queries to use intermediate commands
- **Command sanitization** - Prevents interactive command timeouts (e.g., auto-converts `top` to `top -l 1`)
- **Original query preservation** - Always includes original user query in iteration prompts

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

### 🌐 Network Monitoring Feature

#### Real-Time Outbound Connection Monitoring
Jarvis now includes a powerful network monitoring feature that tracks outbound network connections from background applications in real-time and raises alerts when new connections are detected. When used with AI models (especially Drona), it provides intelligent threat analysis.

**What it monitors:**
- New outbound ESTABLISHED TCP/IP connections
- Process information (name, path, user, command line)
- Local and remote IP addresses and ports
- Connection status and timestamps
- Remote IP type (private vs. public)
- Hostname resolution for remote IPs

**Usage:**
```bash
# Basic monitoring
jarvis -monitor network

# With AI threat analysis (Gemini)
jarvis -monitor network -m gemini

# With AI threat analysis (Drona - recommended)
jarvis -monitor network -m drona -b <bot_id>

# With AI threat analysis (SLM)
jarvis -monitor network -m slm
```

**Example:**
```bash
jarvis -monitor network -m drona -b my_bot_id
```

**How it works:**
1. **Baseline Establishment**: Scans current network connections to establish a baseline
2. **Continuous Monitoring**: Checks for new connections every 3 seconds
3. **Connection Detection**: When a new outbound connection is detected:
   - Raises an alert with full connection details
   - Identifies the application/process making the connection
   - Shows local and remote IP addresses and ports
   - Analyzes the remote IP (private vs public, hostname lookup)
   - Uses AI to assess the threat level (when AI model is enabled)
   - Provides specific recommendations (Allow, Investigate, Block)
4. **Status Updates**: Shows monitoring status every 30 seconds
5. **Summary on Exit**: Displays total alerts and active connections when stopped

**Alert Information:**
Each alert includes:
- **Timestamp** of connection detection
- **Process Details:**
  - Process ID (PID)
  - Process name
  - Process executable path
  - Process owner/user
  - Full command line with arguments
- **Network Details:**
  - Local address and port
  - Remote address and port
  - Connection status
- **Remote IP Analysis:**
  - IP address type (Private/Local vs Public Internet)
  - Hostname (resolved via reverse DNS)
- **AI Threat Assessment** (when AI model enabled):
  - Threat level: LOW, MEDIUM, HIGH, or CRITICAL
  - Detailed analysis of why this threat level was assigned
  - Specific recommendations for the user

**AI Threat Analysis:**
When using an AI model, Jarvis analyzes each connection by considering:
- Is this a known legitimate application? (e.g., Chrome, Slack, VS Code)
- Is the remote IP/hostname suspicious? (known malicious, unusual location)
- Is the port number commonly used for malicious activity?
- Is the process path typical for this application?
- Are there red flags in the command line arguments?
- Does the connection pattern match known malware behavior?

**Use Cases:**
- ✅ Detect applications sending data in the background without your knowledge
- ✅ Identify potential data exfiltration attempts
- ✅ Monitor for suspicious outbound connections during security incidents
- ✅ Audit network activity for compliance or security investigations
- ✅ Learn which applications are making network connections
- ✅ Detect malware or spyware attempting to communicate with C&C servers
- ✅ Monitor for unauthorized data uploads
- ✅ Track when applications "phone home"

**Example Output:**
```
🌐 NETWORK MONITORING MODE - Real-time Outbound Connection Monitor
================================================================================
🤖 Using AI Model: DRONA
================================================================================
📊 Monitoring outbound network connections from background applications...
🔍 Press Ctrl+C to stop monitoring
================================================================================

🔄 Establishing baseline connections...
✅ Baseline established: 45 active connections
🔍 Now monitoring for NEW outbound connections...

🚨🚨🚨🚨🚨🚨🚨🚨🚨🚨🚨🚨🚨🚨🚨🚨🚨🚨🚨🚨🚨🚨🚨🚨🚨🚨🚨🚨🚨🚨🚨🚨🚨🚨🚨🚨🚨🚨🚨🚨
🔴 ALERT #1 - NEW OUTBOUND CONNECTION DETECTED
🚨🚨🚨🚨🚨🚨🚨🚨🚨🚨🚨🚨🚨🚨🚨🚨🚨🚨🚨🚨🚨🚨🚨🚨🚨🚨🚨🚨🚨🚨🚨🚨🚨🚨🚨🚨🚨🚨🚨🚨
⏰ Timestamp: 2025-12-28 14:35:22
--------------------------------------------------------------------------------
📍 Connection Details:
   • Process ID (PID): 12345
   • Process Name: suspicious_app
   • Process Path: /tmp/suspicious_app
   • Process User: username
   • Command Line: /tmp/suspicious_app --upload-data

🌐 Network Details:
   • Local Address: 192.168.1.100:54321
   • Remote Address: 203.0.113.42:8080
   • Connection Status: ESTABLISHED

🔍 Remote IP Analysis:
   • IP Address: 203.0.113.42
   • Type: Public Internet
   • Hostname: suspicious-domain.xyz

--------------------------------------------------------------------------------
🤖 AI Analysis: Analyzing connection for suspicious activity...
⚠️  Threat Assessment: HIGH
💡 Analysis: This connection is highly suspicious. The process is running from /tmp directory (common malware location), connecting to an unknown domain on non-standard port 8080, and the command line suggests data upload functionality. This pattern matches known data exfiltration behavior.
🛡️  Recommendations: BLOCK IMMEDIATELY - Terminate the process (kill 12345), investigate the executable, and check for other malicious files. Consider running a full security scan.
🚨🚨🚨🚨🚨🚨🚨🚨🚨🚨🚨🚨🚨🚨🚨🚨🚨🚨🚨🚨🚨🚨🚨🚨🚨🚨🚨🚨🚨🚨🚨🚨🚨🚨🚨🚨🚨🚨🚨🚨

[14:38:52] 📊 Status: Monitoring... (47 active connections, 1 alerts raised)

^C
================================================================================
🛑 Network monitoring stopped by user
================================================================================
📊 Monitoring Summary:
   • Total alerts raised: 1
   • Active connections at stop: 47
================================================================================
```

**Features:**
- ✅ Real-time monitoring with 3-second interval
- ✅ **Desktop notifications to system notification center**
- ✅ **Cross-platform notification support (macOS, Linux, Windows)**
- ✅ **Enhanced notifications for HIGH/CRITICAL threats**
- ✅ Intelligent baseline establishment to detect only NEW connections
- ✅ Detailed process and connection information
- ✅ AI-powered threat assessment with specific recommendations
- ✅ Remote IP analysis and hostname lookup
- ✅ Private vs. public IP classification
- ✅ Continuous monitoring until stopped
- ✅ Summary statistics on exit
- ✅ Works with all AI models (Gemini, SLM, Drona)
- ✅ Visual alerts with emoji indicators
- ✅ Timestamp tracking for all connections

**Technical Details:**
- Uses psutil library to access network connections
- Monitors ESTABLISHED connections only (filters out listening/pending)
- Tracks connections by (PID, remote_ip, remote_port, local_port) tuple
- Performs reverse DNS lookups for hostname resolution
- Detects private IP ranges (10.x.x.x, 172.16-31.x.x, 192.168.x.x, 127.x.x.x)
- JSON-based AI response parsing with multiple fallback strategies
- Error handling for process access and network operations
- **Cross-platform notification system:**
  - macOS: Uses `osascript` (AppleScript) for native notifications
  - Linux: Uses `notify-send` command (pre-installed on most distros)
  - Windows: Uses PowerShell for Windows 10+ toast notifications
  - Graceful fallback if notification system unavailable
  - Sound alerts included (macOS "Ping" sound)
  - Two-tier notification system: basic alerts + enhanced HIGH/CRITICAL alerts

**Requirements:**
- psutil library (automatically installed)
- Appropriate permissions to read network connections
- AI model configured for threat analysis (optional but recommended)

**Security Benefits:**
- Early detection of data exfiltration attempts
- Identification of malware command-and-control (C&C) communications
- Monitoring of unauthorized data uploads
- Detection of spyware "phoning home"
- Audit trail for security investigations
- Real-time visibility into background network activity

**Tips:**
- Use with Drona model for best AI threat analysis
- Monitor during sensitive operations for security auditing
- Check alerts for unknown or suspicious applications
- Investigate any connections with HIGH or CRITICAL threat levels
- Use Ctrl+C to stop and review summary statistics
- Run with elevated permissions if needed to see all processes

### 🔍 Security Scanning Feature

#### Folder Scanning for Sensitive Files
Jarvis now includes a powerful security scanning feature that uses AI to identify sensitive files in your folders. This feature is available exclusively with the Drona model.

**What it detects:**
- API keys, tokens, passwords, and credentials
- Personal identifiable information (PII): SSN, credit cards, phone numbers, addresses
- Financial information: bank accounts, payment details
- Medical records and health information
- Confidential business data: trade secrets, proprietary code, client data
- Authentication credentials: usernames, passwords, private keys
- Database connection strings with credentials
- Environment variables with secrets
- Configuration files with sensitive data
- Source code with hardcoded secrets

**Usage:**
```bash
# Basic scan
jarvis -scan -f <folder_path> -m drona -b <bot_id>

# With bot ID from config
jarvis -scan -f ~/Documents/myproject -m drona
```

**Example:**
```bash
jarvis -scan -f ~/Documents/myproject -m drona -b my_bot_id
```

**How it works:**
1. **File Collection**: Recursively scans all files in the specified folder (skips hidden files/directories)
2. **Content Extraction**: For each file:
   - Extracts up to 10,000 characters
   - Structures content in markdown format with metadata
   - Includes file path, size, extension, and content
3. **AI Analysis**: Sends each file to Drona LLM for sensitivity analysis
4. **Categorization**: LLM categorizes files as:
   - `is_sensitive`: true or false
   - `sensitivity_level`: high, medium, low, or none
   - `reason`: Explanation of why the file is sensitive
   - `recommended_protection`: Specific protection recommendations
5. **Reporting**: Generates comprehensive report with all sensitive files

**Output Format:**
```
🔍 Starting Folder Scan for Sensitive Files
============================================================
📁 Scanning folder: ~/Documents/myproject
🤖 Using model: DRONA
============================================================

📊 Found 25 files to analyze

🔍 Analyzing [1/25]: config.json
  🔴 SENSITIVE: Contains API keys and database credentials
🔍 Analyzing [2/25]: README.md
  ✅ Not sensitive
...

============================================================
📊 Scan Complete
============================================================
Total files analyzed: 25
Sensitive files found: 3
============================================================

🔴 SENSITIVE FILES DETECTED
============================================================

1. 📄 config.json
   📍 Path: ~/Documents/myproject/config.json
   📊 Size: 1024 bytes
   🔒 Sensitivity Level: HIGH
   💡 Reason: Contains API keys and database connection strings
   🛡️  Recommended Protection: Encrypt file, restrict access (chmod 600), remove from version control

...
```

**Features:**
- ✅ Recursive folder scanning (all subdirectories)
- ✅ Skips hidden files and directories (starts with `.`)
- ✅ Handles text and binary files gracefully
- ✅ Progress tracking with file count
- ✅ Detailed metadata for each file
- ✅ AI-powered sensitivity detection
- ✅ Multiple sensitivity levels (high/medium/low/none)
- ✅ Specific protection recommendations
- ✅ Comprehensive summary report

**Technical Details:**
- Content extraction limited to 10,000 characters per file
- Markdown structure includes file metadata and content
- Robust JSON parsing with multiple fallback strategies
- Handles binary files that can't be decoded
- Error handling for unreadable files

**Protection Recommendations:**
The scan provides specific recommendations such as:
- Encrypt sensitive files
- Restrict file access permissions (chmod 600)
- Move sensitive files to secure locations
- Remove sensitive data from version control
- Use environment variables or secure vaults for secrets
- Implement proper access controls

**Requirements:**
- Drona model (`-m drona`)
- Bot ID (from config or command line)
- Valid folder path

**Note:** This feature is only available with the Drona model. The scan analyzes file content using AI to provide intelligent sensitivity detection beyond simple pattern matching.

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

### 🎤 Voice Command Support

#### Hands-Free Voice Commands
Jarvis now supports voice commands, allowing you to interact hands-free by speaking commands instead of typing.

**Features:**
- Wake word detection - Say "jarvis" followed by your command
- Continuous listening mode - Keeps listening for multiple commands
- Full agentic AI support - Voice commands use the same intelligent iteration system as text commands
- Automatic command output analysis - AI iterates through commands until complete
- Works with all AI models - Gemini, SLM, and Drona

**Usage:**
```bash
# Start voice command mode
jarvis -v

# Voice mode with specific model
jarvis -v -m gemini
jarvis -v -m slm
jarvis -v -m drona -b <bot_id>
```

**How it works:**
1. Start voice mode with `jarvis -v`
2. Say "jarvis" followed by your command
3. Example: "jarvis list files in this directory"
4. Example: "jarvis check if my CPU usage is normal"
5. Jarvis processes your command with full agentic AI support
6. The system automatically iterates through commands until complete
7. Say "quit" or press Ctrl+C to exit

**Example Voice Commands:**
- "jarvis list files in this directory"
- "jarvis check if my CPU usage is normal"
- "jarvis show me running processes"
- "jarvis what's my disk space?"
- "jarvis check memory usage"

**Technical Details:**
- Uses Google Speech Recognition (requires internet connection)
- Automatically adjusts for ambient noise
- Supports phrase time limit of 15 seconds per command
- Wake word: "jarvis" (case-insensitive)
- Command extraction: Everything after "jarvis" is treated as the command

**Requirements:**
- Microphone access
- Internet connection (for Google Speech Recognition)
- SpeechRecognition library (auto-installed)
- PyAudio library (auto-installed)
- PortAudio (install via `brew install portaudio` on macOS)

**Installation:**
```bash
# Install dependencies
pip3 install SpeechRecognition pyaudio --user --break-system-packages

# On macOS, install PortAudio first
brew install portaudio
```

**Agentic Flow:**
Voice commands use the same agentic iteration system as text commands:
- Commands marked as "intermediate" trigger automatic iteration
- Command outputs are sent back to the AI for analysis
- The AI continues iterating until it has enough information
- Final answers are provided as plain text responses

**Enhanced Agentic AI Improvements:**
- Improved prompt engineering to ensure analysis queries use "intermediate" commands
- Safety checks automatically convert "last" to "intermediate" for analysis queries
- Original user query is always preserved and included in iteration prompts
- Command sanitization prevents timeouts by converting interactive commands to non-interactive versions
- Better iteration flow with clear progress indicators

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

# Scan folder for sensitive files (Drona only)
jarvis -scan -f <folder_path> -m drona -b <bot-id>
jarvis -scan -f ~/Documents/myproject -m drona

# Monitor network activity
jarvis -monitor network                    # Basic network monitoring
jarvis -monitor network -m drona -b <bot-id>  # With AI threat analysis

# Monitor processes for threats
jarvis -monitor process                    # Basic process monitoring
jarvis -monitor process -m drona -b <bot-id>  # With AI threat analysis

# Voice commands
jarvis -v                    # Voice mode with Gemini (default)
jarvis -v -m gemini          # Voice mode with Gemini
jarvis -v -m slm             # Voice mode with SLM
jarvis -v -m drona -b <bot-id>  # Voice mode with Drona
```

---

## ⚡ Features

### 🤖 AI-Powered Terminal Assistant
- **Natural language interface** - Ask questions in plain English
- **Multi-model support** - Choose between Gemini AI, SLM, or Drona
- **Intelligent command execution** - AI decides when to run commands vs. provide answers
- **Multi-turn conversations** - Context-aware interactions
- **Voice commands** - Speak commands hands-free with wake word detection
- **Agentic AI iteration** - Automatically iterates through commands until complete
- **Image analysis** - Send images with queries for visual analysis
- **Machine context** - Drona model receives system details and IP address automatically
- **Security scanning** - Scan folders for sensitive files with AI-powered detection (Drona only)

### 💻 System Management
- **System health monitoring** - CPU, memory, disk usage analysis
- **Process management** - View and analyze running processes
- **Network monitoring** - Real-time outbound connection monitoring with alerts
- **AI threat analysis** - Intelligent assessment of network connections
- **Comprehensive diagnostics** - Complete system health reports

### ⚡ Command Execution
- **Direct command execution** - AI can run macOS/Unix commands
- **Smart analysis** - AI analyzes command outputs and provides insights
- **Multi-step workflows** - Handles complex tasks requiring multiple commands
- **Safe execution** - Timeout protection and error handling

### 🎯 Interactive Mode
- **Interactive terminal interface** - Continuous conversation mode
- **Voice command mode** - Hands-free operation with wake word detection
- **Quick commands** - Shortcuts for common tasks (cpu, memory, disk, etc.)
- **Help system** - Built-in help and examples
- **Clean interface** - Organized output with clear formatting

### 🎤 Voice Command Mode
- **Wake word detection** - Say "jarvis" followed by your command
- **Continuous listening** - Keeps listening for multiple commands
- **Full agentic support** - Uses same intelligent iteration as text commands
- **Multi-model support** - Works with all AI models
- **Automatic analysis** - AI iterates through commands until complete

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
- SpeechRecognition (for voice commands)
- PyAudio (for voice commands)
- PortAudio (for PyAudio on macOS - install via `brew install portaudio`)

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

### v1.5.0 (Current)
- ✨ **Process monitoring** - Real-time security monitoring for threats and anomalies
- ✨ **Malware detection** - Identifies cryptominers, ransomware, keyloggers, backdoors
- ✨ **Resource abuse detection** - Monitors CPU/memory usage patterns
- ✨ **Behavioral analysis** - Detects suspicious process behaviors
- ✨ **AI threat classification** - Categorizes threat types with recommendations
- ✨ Network monitoring feature with real-time alerts
- ✨ **Desktop notification system** - Cross-platform alerts (macOS, Linux, Windows)
- ✨ **Enhanced notifications** for HIGH/CRITICAL threats
- ✨ AI-powered threat assessment for network connections and processes
- ✨ Detailed process and connection information display
- ✨ Remote IP analysis with hostname lookup
- ✨ Threat level categorization (LOW, MEDIUM, HIGH, CRITICAL)
- ✨ Baseline establishment for accurate anomaly detection
- ✨ Continuous monitoring (3s for network, 5s for processes)
- ✨ Summary statistics on exit
- 🔧 Private vs. public IP classification
- 🔧 Multi-model AI support for threat analysis
- 🔧 Sound alerts on macOS (Ping sound)
- 🔧 Graceful fallback if notifications unavailable
- 🔧 Multi-factor threat detection (paths, names, commands, resources)

### v1.4.0
- ✨ Security scanning feature for folder analysis (Drona only)
- ✨ AI-powered sensitive file detection
- ✨ Comprehensive sensitivity reporting with recommendations
- ✨ Markdown-structured content extraction (max 10,000 chars per file)
- ✨ Recursive folder scanning with progress tracking
- 🔧 Robust JSON parsing for LLM responses
- 📝 Detailed protection recommendations for sensitive files

### v1.3.0
- ✨ Voice command support with wake word detection
- ✨ Hands-free operation - speak commands instead of typing
- ✨ Enhanced agentic AI iteration for voice commands
- ✨ Automatic command output analysis and iteration
- ✨ Continuous listening mode for multiple commands
- 🔧 Improved prompt engineering for better agentic flow
- 🔧 Command sanitization to prevent interactive command timeouts
- 📦 Added SpeechRecognition and PyAudio dependencies

### v1.2.0
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
**Version**: 1.5.0  
**Release Date**: December 2024  
**License**: MIT

