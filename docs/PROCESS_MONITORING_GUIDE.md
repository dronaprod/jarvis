# 🔍 Process Monitoring Guide

## Overview

Jarvis now includes comprehensive **process monitoring** that helps you detect malware, anomalies, vulnerabilities, unusual resource usage, file deletion attempts, and system threats in real-time.

## 🚀 Quick Start

```bash
# Basic process monitoring
sudo jarvis -monitor process

# With AI threat analysis (recommended)
sudo jarvis -monitor process -m drona -b <your-bot-id>

# With Gemini AI
sudo jarvis -monitor process -m gemini
```

## 🎯 What It Monitors

### 1. Suspicious New Processes
- Processes running from dangerous locations (`/tmp`, `/var/tmp`, `Downloads`)
- Hidden processes (names starting with `.`)
- Processes with malware-like names (keylog, hack, malware, ransom, miner, etc.)
- Processes with randomly generated names
- System-named processes running as regular users

### 2. Resource Abuse
- High CPU usage (>80%)
- High memory usage (>80%)
- Sudden spikes in resource consumption
- Cryptomining activity patterns

### 3. Dangerous Command Line Flags
- File deletion: `rm -rf`, `dd if=`
- Permission changes: `chmod 777`
- Remote code execution: `curl | bash`, `wget | sh`
- Encoding/obfuscation: `base64 -d`, `eval(`, `exec(`
- Unsafe flags: `--no-sandbox`

### 4. Behavioral Anomalies
- Processes with unusual resource patterns
- Rapid changes in CPU/memory usage
- Abnormal thread spawning
- Unexpected file access patterns

## 🔒 Threat Detection

### Malware Types Detected

**Cryptominers:**
- High CPU usage (often 90-100%)
- Hidden names or random strings
- Running from temporary directories
- Connecting to mining pools

**Ransomware:**
- Processes with "encrypt", "ransom" in name
- File deletion or modification commands
- High disk I/O with encryption patterns
- Suspicious file access

**Keyloggers:**
- Processes with "keylog", "logger" in name
- Monitoring keyboard/input devices
- Hidden processes
- Unusual input capture patterns

**Backdoors/Trojans:**
- Processes listening on unusual ports
- Hidden services
- System-level access by regular users
- Unusual network connections

**Spyware:**
- Processes accessing user data
- Hidden background processes
- Unusual file access patterns
- Screen capture or recording activity

## 📊 How It Works

### 1. Baseline Establishment
```
🔄 Establishing process baseline...
✅ Baseline established: 287 processes
```
- Scans all running processes
- Records normal CPU/memory usage for each
- Tracks process metadata

### 2. Continuous Monitoring
- Checks processes every 5 seconds
- Compares against baseline
- Detects new processes immediately
- Monitors resource usage changes

### 3. Threat Detection
When suspicious activity is detected:
- **Analyzes process details** (name, path, command, user)
- **Checks threat indicators** (location, name patterns, commands)
- **Evaluates resource usage** (CPU, memory, threads)
- **Sends desktop notification** with severity level
- **Uses AI for classification** (when AI model enabled)
- **Provides recommendations** (Allow, Monitor, Terminate, Block)

### 4. AI Threat Analysis
AI evaluates:
- Is this a known legitimate process?
- Are resource patterns normal?
- Is the executable path typical?
- Are there command line red flags?
- Could this be malware/ransomware/cryptominer?
- Is it attempting file corruption or system compromise?

## 🔔 Desktop Notifications

### Notification Types

**Basic Notifications** (All Suspicious Activity):
```
MEDIUM Process Alert #1
Chrome Helper using 95% CPU
```

**Enhanced Notifications** (HIGH/CRITICAL Threats):
```
CRITICAL THREAT - NEW_PROCESS
.miner (PID 12345) | user | Check terminal for details
```

### Severity Levels

- **LOW**: Minor anomalies, likely benign
- **MEDIUM**: Unusual but not necessarily malicious
- **HIGH**: Strong indicators of malicious activity
- **CRITICAL**: Confirmed threat patterns, immediate action needed

## 💡 Example Scenarios

### Scenario 1: Cryptominer Detection
```
🚨 ALERT #1 - SUSPICIOUS PROCESS ACTIVITY DETECTED
⏰ Timestamp: 2025-12-28 16:45:23
⚠️  Activity Type: NEW_PROCESS
⚠️  Severity: CRITICAL

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

🤖 AI Analysis:
⚠️  AI Threat Assessment: CRITICAL
💡 Analysis: This is highly likely a cryptominer malware...
🛡️  Recommendations: TERMINATE IMMEDIATELY - Kill process (sudo kill -9 98765)...
```

**Action:** Immediately terminate the process and remove the executable.

### Scenario 2: Ransomware Detection
```
🚨 ALERT #2 - SUSPICIOUS PROCESS ACTIVITY DETECTED
⚠️  Activity Type: NEW_PROCESS
⚠️  Severity: CRITICAL

📍 Process Details:
   • Process Name: encrypt_files
   • Command: python encrypt_files.py --target /Users --key abc123

🔍 Threat Analysis:
   • Suspicious process name contains: encrypt
   • Suspicious command: targeting user files
   • High risk command pattern detected

🤖 AI Analysis:
⚠️  AI Threat Assessment: CRITICAL
💡 Analysis: Potential ransomware attempting to encrypt user files...
🛡️  Recommendations: TERMINATE IMMEDIATELY and disconnect network...
```

**Action:** Kill process, disconnect network, restore from backup.

### Scenario 3: Resource Abuse
```
🚨 ALERT #3 - SUSPICIOUS PROCESS ACTIVITY DETECTED
⚠️  Activity Type: HIGH_CPU
⚠️  Severity: MEDIUM

📍 Process Details:
   • Process Name: chrome_helper
   • CPU: 98% (baseline: 5%)

⚠️  CPU Usage Anomaly:
   • Current: 98.0%
   • Baseline: 5.0%
   • Increase: +93.0%
```

**Action:** Investigate why helper process is using so much CPU.

## 🛠️ Usage Examples

### Basic Monitoring
```bash
sudo jarvis -monitor process
```
Shows all suspicious processes without AI analysis.

### With AI Analysis
```bash
sudo jarvis -monitor process -m drona -b <bot-id>
```
Full threat analysis with AI classification and recommendations.

### Background Monitoring
```bash
sudo jarvis -monitor process -m gemini > process_monitor.log 2>&1 &
```
Run in background and log all alerts to file.

## 🔧 Requirements

### System Requirements
- macOS, Linux, or Windows
- Python 3.7+
- psutil library (auto-installed)

### Permissions
- **macOS/Linux**: Requires `sudo` for full process visibility
- **Windows**: Run as Administrator

### Optional
- AI model configured (Gemini, SLM, or Drona)
- Internet connection (for AI analysis)

## 💡 Tips and Best Practices

### 1. Run with sudo
```bash
sudo jarvis -monitor process -m drona -b <bot-id>
```
Without sudo, you'll miss processes running as other users.

### 2. Use AI Analysis
Always use an AI model (especially Drona) for best threat detection:
```bash
sudo jarvis -monitor process -m drona -b <bot-id>
```

### 3. Monitor During Suspicious Activity
Run monitoring when:
- System is slow for no reason
- High CPU/memory usage unexpectedly
- After installing unknown software
- During security incidents
- After clicking suspicious links

### 4. Act on Alerts
For HIGH/CRITICAL threats:
1. Read the full alert in terminal
2. Note the PID and process name
3. Terminate immediately: `sudo kill -9 <PID>`
4. Remove the executable if in /tmp or Downloads
5. Run full system scan
6. Check for persistence (cron, LaunchAgents, startup items)

### 5. False Positives
Some legitimate processes may trigger alerts:
- Development tools compiling code
- Video encoding software
- Scientific computing applications
- Virtual machines

Use AI analysis to help distinguish legitimate from malicious.

## 🚨 Responding to Threats

### Immediate Actions
```bash
# Terminate malicious process
sudo kill -9 <PID>

# Remove malicious executable
sudo rm <path-to-executable>

# Check for related processes
ps aux | grep <process-name>

# Check what files it opened
sudo lsof -p <PID>
```

### Investigation
```bash
# Check process tree
pstree -p <PID>

# Check network connections
sudo lsof -i -P | grep <process-name>

# Check file modifications
sudo find /Users -mtime -1  # Files modified in last day
```

### Prevention
```bash
# Check startup items (macOS)
launchctl list
ls ~/Library/LaunchAgents/
ls /Library/LaunchAgents/
ls /Library/LaunchDaemons/

# Check cron jobs
crontab -l
sudo crontab -l
```

## 📈 Understanding Baselines

### How Baselines Work
1. **Initial Scan**: Records normal CPU/memory for each process
2. **Rolling Average**: Updates baseline as process behavior changes
3. **Anomaly Detection**: Flags significant deviations from baseline

### Baseline Formula
```
new_baseline = (old_baseline * 0.7) + (current_value * 0.3)
```
This gives more weight to historical behavior while adapting to changes.

### Threshold Triggers
- **CPU Spike**: >50% increase above baseline, current >80%
- **Memory Spike**: >30% increase above baseline, current >80%

## 🔍 Threat Indicator Details

### Path-Based Detection
**Suspicious Paths:**
- `/tmp/` - Temporary directory, common for malware
- `/var/tmp/` - Another temp location
- `/dev/shm/` - Shared memory, used by some malware
- `~/Downloads/` - User downloads, risky area

### Name-Based Detection
**Suspicious Names:**
- Contains: keylog, hack, crack, exploit, malware
- Contains: backdoor, trojan, ransom, miner, cryptominer
- Starts with: `.` (hidden processes)
- Random strings: High consonant clusters, no meaning

### Command-Based Detection
**Dangerous Commands:**
- `rm -rf` - Recursive deletion
- `dd if=` - Disk operations
- `chmod 777` - Dangerous permissions
- `curl | bash` - Remote code execution
- `base64 -d` - Decoding (often used to hide malware)

## 📊 Statistics

The monitoring summary shows:
```
📊 Monitoring Summary:
   • Total alerts raised: 5
   • Processes monitored: 287
```

- **Total alerts**: Number of suspicious activities detected
- **Processes monitored**: Currently tracked processes

## ❓ Troubleshooting

### No Alerts Showing
- Make sure you're running with `sudo`
- Try triggering test process (see below)
- Check if monitoring is actually running

### Too Many Alerts
- Use AI analysis to filter legitimate processes
- Focus on HIGH/CRITICAL severity
- Adjust thresholds in code if needed

### Permission Errors
```bash
# Make sure you're using sudo
sudo jarvis -monitor process
```

### Testing the Feature
```bash
# Create a test suspicious process
cat > /tmp/test_process.sh << 'EOF'
#!/bin/bash
while true; do
  echo "test"
  sleep 1
done
EOF
chmod +x /tmp/test_process.sh
/tmp/test_process.sh &

# Should trigger alert for /tmp/ location
# Kill it when done:
killall test_process.sh
rm /tmp/test_process.sh
```

## 🎯 Summary

Process monitoring provides:
- ✅ Real-time malware detection
- ✅ Cryptominer identification
- ✅ Ransomware early warning
- ✅ Resource abuse detection
- ✅ Behavioral anomaly detection
- ✅ AI-powered threat classification
- ✅ Desktop notifications for threats
- ✅ Actionable recommendations
- ✅ Continuous security monitoring

**Start monitoring now:**
```bash
sudo jarvis -monitor process -m drona -b <your-bot-id>
```

Stay safe! 🛡️

---

**Version**: 1.5.0  
**Feature Added**: December 28, 2025  
**Status**: ✅ Production Ready

