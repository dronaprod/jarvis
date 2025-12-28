# 🔔 Desktop Notification Feature

## Overview

Network monitoring now includes **desktop notifications** that alert you in real-time when new network connections are detected. This works across macOS, Linux, and Windows!

## ✨ Features

### Two-Tier Notification System

1. **Basic Notifications** (All Connections)
   - Sent for every new network connection detected
   - Shows process name and remote destination
   - Example: "Chrome connected to 142.250.185.78:443"

2. **Enhanced Notifications** (HIGH/CRITICAL Threats Only)
   - Sent when AI detects HIGH or CRITICAL threats
   - Includes threat level and brief analysis
   - Example: "⚠️ HIGH THREAT - suspicious_app → 203.0.113.42 | Process running from /tmp..."

## 🖥️ Cross-Platform Support

### macOS (Your System!)
- Uses **native Notification Center**
- Includes sound alert (Ping sound)
- No additional software needed
- Shows up in notification center with app icon

### Linux
- Uses `notify-send` command
- Pre-installed on most distributions (Ubuntu, Fedora, etc.)
- Shows up in system notification area

### Windows
- Uses PowerShell notifications
- Works on Windows 10 and later
- Shows as toast notifications

## 🚀 How It Works

### When Monitoring Starts
```bash
sudo jarvis -monitor network -m drona -b <bot-id>
```

You'll see:
```
🌐 NETWORK MONITORING MODE - Real-time Outbound Connection Monitor
================================================================================
🤖 Using AI Model: DRONA
💻 System: Darwin
================================================================================
📊 Monitoring outbound network connections from background applications...
🔔 Desktop notifications will be sent for new connections
🔍 Press Ctrl+C to stop monitoring
================================================================================
```

### When Connection Detected

**In Terminal:**
```
🚨🚨🚨🚨🚨🚨🚨🚨🚨🚨🚨🚨🚨🚨🚨🚨🚨🚨🚨🚨
🔴 ALERT #1 - NEW OUTBOUND CONNECTION DETECTED
🚨🚨🚨🚨🚨🚨🚨🚨🚨🚨🚨🚨🚨🚨🚨🚨🚨🚨🚨🚨
⏰ Timestamp: 2025-12-28 15:30:45
```

**In Notification Center (macOS):**
```
🚨 Network Alert #1
Chrome connected to 142.250.185.78:443
```

**If HIGH/CRITICAL Threat Detected:**
```
⚠️ HIGH THREAT - Alert #2
suspicious_app → 203.0.113.42 | Process running from /tmp directory...
```

## 💡 Benefits

### Stay Informed Without Watching Terminal
- Continue working on other tasks
- Get notified immediately when suspicious activity occurs
- Notifications stay in notification center for review

### Prioritized Alerts
- All connections trigger basic notifications
- HIGH/CRITICAL threats trigger enhanced notifications
- Focus on what matters most

### No Additional Setup Required
- Works out of the box on macOS
- Uses built-in system notification APIs
- No external dependencies needed

## 🔧 Technical Implementation

### Code Structure
```python
def send_system_notification(self, title, message):
    """Send system notification based on OS"""
    system = platform.system()
    
    if system == "Darwin":  # macOS
        # Use osascript (AppleScript)
        subprocess.run(['osascript', '-e', script])
    
    elif system == "Linux":
        # Use notify-send
        subprocess.run(['notify-send', title, message])
    
    elif system == "Windows":
        # Use PowerShell
        subprocess.run(['powershell', '-Command', ps_script])
```

### Notification Timing
1. **Basic notification**: Sent immediately when connection detected
2. **Enhanced notification**: Sent after AI analysis completes (only for HIGH/CRITICAL)

### Error Handling
- Graceful failure if notification system unavailable
- Won't interrupt monitoring if notifications fail
- Silently continues without notifications

## 🎯 Use Cases

### Security Monitoring
Run monitoring in background, get notified of suspicious connections:
```bash
sudo jarvis -monitor network -m drona -b <bot-id> &
```

### Development/Testing
See when your app makes network connections without watching terminal

### Incident Response
Get immediate alerts during security investigations

### Learning Tool
Understand what apps are connecting to the internet in real-time

## 📊 Example Scenarios

### Scenario 1: Normal Activity (LOW Threat)
**Notification:**
```
🚨 Network Alert #1
Chrome connected to google.com:443
```
**Action:** No action needed, notification is informational

### Scenario 2: Suspicious Activity (HIGH Threat)
**First Notification:**
```
🚨 Network Alert #2
unknown_process connected to 203.0.113.42:8080
```

**Enhanced Notification (after AI analysis):**
```
⚠️ HIGH THREAT - Alert #2
unknown_process → 203.0.113.42 | Process from /tmp, unknown domain, non-standard port
```
**Action:** Investigate immediately!

## 🔒 Privacy

### What Gets Sent in Notifications
- Process name
- Remote IP and port
- Threat level (if AI enabled)
- Brief analysis (for HIGH/CRITICAL threats only)

### What Doesn't Get Sent
- No data leaves your machine except for AI analysis
- Notifications are local to your system
- No telemetry or tracking

## ⚙️ Configuration

### Disable Notifications
If you don't want notifications, you can comment out the notification call in the code or just ignore them. The terminal output still shows everything.

### Customize Notifications
Edit the `send_system_notification()` method in `jarvis.py` to customize:
- Notification sound (macOS)
- Notification icon
- Notification duration
- Notification priority

## 🧪 Testing

### Test Notifications
```bash
# Start monitoring
sudo jarvis -monitor network -m gemini

# In another terminal, trigger a connection
curl https://google.com
```

You should see:
1. Terminal alert
2. Desktop notification
3. AI analysis (if enabled)
4. Enhanced notification if HIGH/CRITICAL

## 📝 Requirements

### macOS
- ✅ No additional requirements
- ✅ Built-in AppleScript support
- ✅ Works on macOS 10.8+

### Linux
- ✅ `notify-send` (pre-installed on most distros)
- ✅ D-Bus notification daemon

### Windows
- ✅ PowerShell (built-in Windows 10+)
- ✅ Windows.UI.Notifications API

## 🎉 Summary

Desktop notifications make network monitoring more practical and user-friendly:
- ✅ Real-time alerts without watching terminal
- ✅ Cross-platform support (macOS, Linux, Windows)
- ✅ Two-tier notification system (basic + enhanced)
- ✅ Works out of the box, no setup needed
- ✅ Prioritized alerts for HIGH/CRITICAL threats
- ✅ Sound alerts on macOS
- ✅ Graceful fallback if unavailable

**Try it now:**
```bash
sudo jarvis -monitor network -m drona -b <your-bot-id>
```

Then open a web browser or any app that makes network connections - you'll get notified! 🔔

---

**Version**: 1.5.0  
**Feature Added**: December 28, 2025  
**Status**: ✅ Production Ready

