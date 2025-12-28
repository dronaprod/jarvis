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

# Scan folder for sensitive files (Drona only)
jarvis -scan -f <folder_path> -m drona -b <bot_id>
jarvis -scan -f ~/Documents/myproject -m drona

# Monitor network activity
jarvis -monitor network                    # Basic network monitoring
jarvis -monitor network -m drona -b <bot_id>  # With AI threat analysis

# Monitor processes for threats
jarvis -monitor process                    # Basic process monitoring
jarvis -monitor process -m drona -b <bot_id>  # With AI threat analysis

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
- ✅ Security scanning - scan folders for sensitive files (Drona only)
- ✅ Network monitoring - real-time outbound connection alerts with AI threat analysis
- ✅ Process monitoring - detect malware, anomalies, resource abuse, and system threats

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

## 🔍 Security Scanning (Drona Only)

Jarvis can scan folders to identify sensitive files that may contain:
- API keys, tokens, passwords, credentials
- Personal identifiable information (PII)
- Financial information
- Medical records
- Confidential business data
- Authentication credentials
- Database connection strings
- Environment variables with secrets

**Usage:**
```bash
jarvis -scan -f <folder_path> -m drona [-b <bot_id>]
```

**Example:**
```bash
jarvis -scan -f ~/Documents/myproject -m drona -b my_bot_id
```

**How it works:**
1. Scans all files in the specified folder (recursively)
2. Extracts file content (up to 10,000 characters per file) with markdown structure
3. Sends each file to Drona LLM for sensitivity analysis
4. Categorizes files as sensitive or not sensitive
5. Provides detailed report with:
   - List of sensitive files
   - Sensitivity level (high/medium/low)
   - Reason for classification
   - Recommended protection measures

**Features:**
- ✅ Recursive folder scanning
- ✅ Automatic content extraction with markdown formatting
- ✅ AI-powered sensitivity detection
- ✅ Detailed protection recommendations
- ✅ Progress tracking during scan
- ✅ Comprehensive report with actionable insights

**Output:**
The scan provides:
- Total files analyzed
- Number of sensitive files found
- Detailed list of each sensitive file with:
  - File path and name
  - File size
  - Sensitivity level
  - Reason for classification
  - Recommended protection actions
- General security recommendations

**Note:** This feature is only available with `-m drona` model.

## 🌐 Network Monitoring

Jarvis can monitor real-time outbound network connections from background applications and raise alerts when new connections are detected. When used with AI models (especially Drona), it can provide intelligent threat analysis.

**Usage:**
```bash
jarvis -monitor network                      # Basic monitoring
jarvis -monitor network -m gemini            # With Gemini threat analysis
jarvis -monitor network -m drona -b <bot_id> # With Drona threat analysis
```

**Example:**
```bash
jarvis -monitor network -m drona -b my_bot_id
```

**How it works:**
1. Establishes a baseline of current network connections
2. Continuously monitors for NEW outbound connections (every 3 seconds)
3. When a new connection is detected:
   - **Sends desktop notification** to your system notification center
   - Raises an alert with detailed connection information
   - Identifies the application/process making the connection
   - Shows local and remote IP addresses and ports
   - Analyzes the remote IP (private vs public, hostname)
   - Uses AI to assess the threat level (when AI model is enabled)
   - **Sends enhanced notification** for HIGH/CRITICAL threats
4. Provides actionable recommendations for each connection
5. Press Ctrl+C to stop monitoring and see summary

**Alert Information:**
Each alert provides:
- **Desktop Notification** sent to system notification center
- **Timestamp** of when the connection was detected
- **Process Information:**
  - Process ID (PID)
  - Process name
  - Process path (executable location)
  - Process user
  - Command line arguments
- **Network Details:**
  - Local address and port
  - Remote address and port
  - Connection status
- **Remote IP Analysis:**
  - IP address type (private/public)
  - Hostname (if available)
- **AI Threat Assessment** (when AI model is enabled):
  - Threat level: LOW, MEDIUM, HIGH, or CRITICAL
  - Detailed analysis explaining the assessment
  - Specific recommendations (Allow, Investigate, Block)
  - **Enhanced notification** for HIGH/CRITICAL threats

**AI-Powered Threat Analysis:**
When using an AI model (Gemini, SLM, or Drona), Jarvis analyzes each connection considering:
- Is this a known legitimate application?
- Is the remote IP/hostname suspicious?
- Is the port number commonly used for malicious activity?
- Is the process path typical for this application?
- Are there any red flags in the command line arguments?

**Use Cases:**
- ✅ Detect applications sending data in the background
- ✅ Identify potential data exfiltration attempts
- ✅ Monitor for suspicious outbound connections
- ✅ Audit network activity during security investigations
- ✅ Learn which applications are making network connections
- ✅ Detect malware or spyware attempting to communicate

**Features:**
- ✅ Real-time monitoring with low latency (3-second interval)
- ✅ **Desktop notifications** - Alerts sent to system notification center
- ✅ **Cross-platform notifications** - Works on macOS, Linux, and Windows
- ✅ **Enhanced alerts** for HIGH/CRITICAL threats
- ✅ Intelligent baseline establishment
- ✅ Detailed process and connection information
- ✅ AI-powered threat assessment
- ✅ Remote IP analysis and hostname lookup
- ✅ Continuous monitoring until stopped
- ✅ Summary statistics on exit
- ✅ Works with all AI models (Gemini, SLM, Drona)

**Desktop Notifications:**
Jarvis sends real-time notifications to your system notification center:
- **macOS**: Uses native notification center (no additional setup needed)
- **Linux**: Uses `notify-send` (pre-installed on most distributions)
- **Windows**: Uses PowerShell notifications (built-in)

**Notification Types:**
- **Basic Alert**: Sent for every new connection detected
  - Shows process name and remote destination
- **Enhanced Alert**: Sent for HIGH/CRITICAL threats (when AI is enabled)
  - Includes threat level and brief analysis
  - Uses warning icon/sound

**Requirements:**
- psutil library (automatically installed)
- Appropriate permissions to read network connections (requires `sudo` on macOS)
- AI model configured for threat analysis (optional but recommended)

**Example Output:**
```
🚨🚨🚨🚨🚨🚨🚨🚨🚨🚨🚨🚨🚨🚨🚨🚨🚨🚨🚨🚨🚨🚨🚨🚨🚨🚨🚨🚨🚨🚨🚨🚨🚨🚨🚨🚨🚨🚨🚨🚨
🔴 ALERT #1 - NEW OUTBOUND CONNECTION DETECTED
🚨🚨🚨🚨🚨🚨🚨🚨🚨🚨🚨🚨🚨🚨🚨🚨🚨🚨🚨🚨🚨🚨🚨🚨🚨🚨🚨🚨🚨🚨🚨🚨🚨🚨🚨🚨🚨🚨🚨🚨
⏰ Timestamp: 2025-12-28 14:35:22
--------------------------------------------------------------------------------
📍 Connection Details:
   • Process ID (PID): 1234
   • Process Name: Chrome
   • Process Path: /Applications/Google Chrome.app/Contents/MacOS/Google Chrome
   • Process User: username
   • Command Line: /Applications/Google Chrome.app/Contents/MacOS/Google Chrome --flag...

🌐 Network Details:
   • Local Address: 192.168.1.100:54321
   • Remote Address: 142.250.185.78:443
   • Connection Status: ESTABLISHED

🔍 Remote IP Analysis:
   • IP Address: 142.250.185.78
   • Type: Public Internet
   • Hostname: lhr25s34-in-f14.1e100.net

--------------------------------------------------------------------------------
🤖 AI Analysis: Analyzing connection for suspicious activity...
⚠️  Threat Assessment: LOW
💡 Analysis: This is a legitimate Google Chrome connection to Google's servers (1e100.net domain) on HTTPS port 443. The process path is standard for Chrome installation.
🛡️  Recommendations: Allow - this is normal Chrome browsing activity.
🚨🚨🚨🚨🚨🚨🚨🚨🚨🚨🚨🚨🚨🚨🚨🚨🚨🚨🚨🚨🚨🚨🚨🚨🚨🚨🚨🚨🚨🚨🚨🚨🚨🚨🚨🚨🚨🚨🚨🚨
```

**Tips:**
- Use with Drona model for best threat analysis
- Monitor during sensitive operations for security auditing
- Check alerts for unknown or suspicious applications
- Investigate any connections with HIGH or CRITICAL threat levels
- Use Ctrl+C to stop and review summary statistics

## 🔍 Process Monitoring

Jarvis can monitor running processes in real-time to detect anomalies, threats, vulnerabilities, unusual resource usage, and suspicious file operations. This comprehensive security monitoring helps identify malware, cryptominers, ransomware, and other threats.

**Usage:**
```bash
jarvis -monitor process                      # Basic monitoring
jarvis -monitor process -m gemini            # With Gemini threat analysis
jarvis -monitor process -m drona -b <bot_id> # With Drona threat analysis (recommended)
```

**Example:**
```bash
sudo jarvis -monitor process -m drona -b my_bot_id
```

**What It Monitors:**
1. **New Suspicious Processes**
   - Processes running from suspicious locations (/tmp, /var/tmp, Downloads)
   - Hidden processes (starting with .)
   - Processes with suspicious names (keylog, hack, malware, ransom, etc.)
   - Processes with randomly generated names
   - System-named processes running as regular users

2. **Resource Abuse**
   - High CPU usage (>80%)
   - High memory usage (>80%)
   - Sudden spikes in resource consumption
   - Cryptomining indicators

3. **Suspicious Command Line Flags**
   - File deletion commands (rm -rf)
   - Dangerous operations (dd if=, chmod 777)
   - Remote code execution (curl | bash, wget | sh)
   - Encoding/obfuscation (base64 -d, eval, exec)
   - Unsafe flags (--no-sandbox)

4. **Behavioral Anomalies**
   - Processes with unusual resource patterns
   - Rapid changes in CPU/memory usage
   - Processes accessing system files
   - Multiple threads spawned suddenly

**How it works:**
1. **Baseline Establishment**: Scans current processes and resource usage
2. **Continuous Monitoring**: Checks processes every 5 seconds
3. **Threat Detection**: When suspicious activity is detected:
   - **Sends desktop notification** with threat level
   - Shows detailed process information
   - Displays threat indicators and reasons
   - Analyzes resource usage patterns
   - Uses AI to assess threat level (when AI model is enabled)
   - **Sends enhanced notification** for HIGH/CRITICAL threats
4. **AI Analysis**: Evaluates if process is malware, ransomware, cryptominer, etc.
5. **Status Updates**: Shows monitoring status every 30 seconds
6. **Summary on Exit**: Displays total alerts when stopped

**Alert Information:**
Each alert includes:
- **Desktop Notification** sent to system notification center
- **Timestamp** of detection
- **Activity Type**: NEW_PROCESS, HIGH_CPU, HIGH_MEMORY
- **Severity Level**: LOW, MEDIUM, HIGH, CRITICAL
- **Process Details:**
  - Process ID (PID)
  - Process name
  - Executable path
  - User running the process
  - Full command line
- **Resource Usage:**
  - Current CPU percentage
  - Current memory percentage
  - Number of threads
- **Threat Indicators:**
  - Specific reasons why it's suspicious
  - Behavioral patterns detected
- **AI Threat Assessment** (when AI model enabled):
  - Threat level and confidence
  - Detailed analysis
  - Threat type identification (malware/ransomware/cryptominer/etc.)
  - Specific recommendations (Allow, Monitor, Investigate, Terminate)

**Threat Detection Examples:**

**Malware Detection:**
- Process: `.hidden_miner`
- Path: `/tmp/.hidden_miner`
- Indicators: Hidden process, suspicious location, high CPU (95%)
- AI Assessment: CRITICAL - Likely cryptominer

**Ransomware Detection:**
- Process: `encrypt_files`
- Command: `python encrypt_files.py --target /Users`
- Indicators: Suspicious name, file operation commands
- AI Assessment: CRITICAL - Potential ransomware

**Resource Abuse:**
- Process: `chrome_helper`
- CPU: 98% (baseline: 5%)
- Indicators: Massive CPU spike, unusual for helper process
- AI Assessment: HIGH - Investigate for malicious code

**Features:**
- ✅ Real-time monitoring with 5-second interval
- ✅ **Desktop notifications for all threats**
- ✅ **Enhanced notifications for HIGH/CRITICAL threats**
- ✅ **Cross-platform notifications** (macOS, Linux, Windows)
- ✅ Intelligent baseline establishment per process
- ✅ Rolling average for resource usage patterns
- ✅ Multi-factor threat detection (name, path, commands, resources)
- ✅ AI-powered threat classification
- ✅ Malware/ransomware/cryptominer detection
- ✅ Behavioral anomaly detection
- ✅ Continuous monitoring until stopped
- ✅ Summary statistics on exit
- ✅ Works with all AI models (Gemini, SLM, Drona)

**Use Cases:**
- ✅ Detect malware and viruses
- ✅ Identify ransomware before it encrypts files
- ✅ Find hidden cryptominers stealing resources
- ✅ Monitor for backdoors and trojans
- ✅ Detect keyloggers and spyware
- ✅ Identify resource abuse and DoS attempts
- ✅ Catch unauthorized file deletion attempts
- ✅ Detect system corruption attempts
- ✅ Monitor for privilege escalation
- ✅ Audit security during incident response

**Requirements:**
- psutil library (automatically installed)
- Elevated permissions (requires `sudo` on macOS/Linux)
- AI model configured for threat analysis (optional but highly recommended)

**Example Output:**
```
🔍 PROCESS MONITORING MODE - Real-time Security & Anomaly Detection
================================================================================
🤖 Using AI Model: DRONA
💻 System: Darwin
================================================================================
📊 Monitoring for:
   • New suspicious processes
   • Unusual CPU/Memory usage
   • Potential threats and vulnerabilities
   • File deletion/corruption attempts
   • System integrity threats
🔔 Desktop notifications will be sent for threats
🔍 Press Ctrl+C to stop monitoring
================================================================================

🔄 Establishing process baseline...
✅ Baseline established: 287 processes
🔍 Now monitoring for anomalies and threats...

🚨🚨🚨🚨🚨🚨🚨🚨🚨🚨🚨🚨🚨🚨🚨🚨🚨🚨🚨🚨🚨🚨🚨🚨🚨🚨🚨🚨🚨🚨🚨🚨🚨🚨🚨🚨🚨🚨🚨🚨
🔴 ALERT #1 - SUSPICIOUS PROCESS ACTIVITY DETECTED
🚨🚨🚨🚨🚨🚨🚨🚨🚨🚨🚨🚨🚨🚨🚨🚨🚨🚨🚨🚨🚨🚨🚨🚨🚨🚨🚨🚨🚨🚨🚨🚨🚨🚨🚨🚨🚨🚨🚨🚨
⏰ Timestamp: 2025-12-28 16:45:23
⚠️  Activity Type: NEW_PROCESS
⚠️  Severity: HIGH
--------------------------------------------------------------------------------
📍 Process Details:
   • Process ID (PID): 98765
   • Process Name: .miner
   • Executable Path: /tmp/.miner
   • User: username
   • Command: /tmp/.miner --pool crypto.pool.com --threads 8

📊 Resource Usage:
   • CPU: 95.3%
   • Memory: 42.1%
   • Threads: 8

🔍 Threat Analysis:
   • Running from suspicious location: /tmp/
   • Hidden process (starts with .)
   • High resource usage: CPU 95.3%, Memory 42.1%
   • Suspicious process name contains: miner
--------------------------------------------------------------------------------
🤖 AI Analysis: Analyzing process for threats...
⚠️  AI Threat Assessment: CRITICAL
💡 Analysis: This is highly likely a cryptominer malware. Running from /tmp with hidden name, consuming maximum CPU resources for mining cryptocurrency. The command line shows connection to mining pool. This is unauthorized resource theft.
🛡️  Recommendations: TERMINATE IMMEDIATELY - Kill process (sudo kill -9 98765), delete executable (sudo rm /tmp/.miner), run full system scan, check for persistence mechanisms (cron, LaunchAgents).
🚨🚨🚨🚨🚨🚨🚨🚨🚨🚨🚨🚨🚨🚨🚨🚨🚨🚨🚨🚨🚨🚨🚨🚨🚨🚨🚨🚨🚨🚨🚨🚨🚨🚨🚨🚨🚨🚨🚨🚨
```

**Tips:**
- Always run with sudo for complete process visibility
- Use with AI models (especially Drona) for best threat detection
- Monitor during suspicious system behavior
- Check alerts for processes you don't recognize
- Terminate any process marked as CRITICAL immediately
- Use kill -9 <PID> to terminate malicious processes
- Review command lines carefully for suspicious flags

## 🎉 Enjoy Jarvis!

Your AI-powered terminal assistant is ready!
# jarvis
