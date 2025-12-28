# 🌐 Network Monitoring Guide

## Overview

Jarvis now includes a powerful network monitoring feature that helps you detect and analyze outbound network connections from background applications in real-time. This guide will help you understand and use this feature effectively.

## Quick Start

### Basic Usage

```bash
# Start network monitoring (basic mode)
jarvis -monitor network
```

### With AI Threat Analysis

```bash
# With Gemini AI
jarvis -monitor network -m gemini

# With Drona AI (recommended for best analysis)
jarvis -monitor network -m drona -b <your-bot-id>

# With SLM AI
jarvis -monitor network -m slm
```

## How It Works

### 1. Baseline Establishment
When you start network monitoring, Jarvis first establishes a baseline of all currently active network connections. This helps it identify only NEW connections that are made after monitoring begins.

```
🔄 Establishing baseline connections...
✅ Baseline established: 45 active connections
🔍 Now monitoring for NEW outbound connections...
```

### 2. Continuous Monitoring
Jarvis checks for new connections every 3 seconds. This provides real-time detection without overwhelming your system.

### 3. Alert Generation
When a new outbound connection is detected, Jarvis generates a detailed alert showing:

- **Timestamp** - When the connection was detected
- **Process Information** - Which application made the connection
- **Network Details** - Where the connection is going
- **Remote IP Analysis** - Information about the destination
- **AI Threat Assessment** - Risk level and recommendations (when AI is enabled)

### 4. Status Updates
Every 30 seconds, Jarvis shows a status update:

```
[14:38:52] 📊 Status: Monitoring... (47 active connections, 1 alerts raised)
```

### 5. Exit and Summary
Press `Ctrl+C` to stop monitoring. Jarvis will show a summary:

```
================================================================================
🛑 Network monitoring stopped by user
================================================================================
📊 Monitoring Summary:
   • Total alerts raised: 5
   • Active connections at stop: 47
================================================================================
```

## Alert Details

### Process Information
Each alert shows detailed information about the process making the connection:

```
📍 Connection Details:
   • Process ID (PID): 12345
   • Process Name: Chrome
   • Process Path: /Applications/Google Chrome.app/Contents/MacOS/Google Chrome
   • Process User: username
   • Command Line: /Applications/Google Chrome.app/Contents/MacOS/Google Chrome --flag...
```

### Network Details
Shows where the connection is going:

```
🌐 Network Details:
   • Local Address: 192.168.1.100:54321
   • Remote Address: 142.250.185.78:443
   • Connection Status: ESTABLISHED
```

### Remote IP Analysis
Analyzes the destination IP address:

```
🔍 Remote IP Analysis:
   • IP Address: 142.250.185.78
   • Type: Public Internet
   • Hostname: lhr25s34-in-f14.1e100.net
```

### AI Threat Assessment
When using an AI model, Jarvis provides intelligent threat analysis:

```
🤖 AI Analysis: Analyzing connection for suspicious activity...
⚠️  Threat Assessment: LOW
💡 Analysis: This is a legitimate Google Chrome connection to Google's servers...
🛡️  Recommendations: Allow - this is normal Chrome browsing activity.
```

## Threat Levels

### LOW
Normal, expected connections from legitimate applications.
- **Example**: Chrome connecting to google.com on port 443
- **Action**: No action needed

### MEDIUM
Unusual but not necessarily malicious connections.
- **Example**: Application connecting to unknown domain on standard port
- **Action**: Monitor and investigate if repeated

### HIGH
Suspicious connections with red flags.
- **Example**: Application from /tmp connecting to unknown IP on unusual port
- **Action**: Investigate immediately, consider blocking

### CRITICAL
Connections with multiple indicators of malicious activity.
- **Example**: Unknown process attempting to connect to known malicious IP
- **Action**: Block immediately, terminate process, run security scan

## Use Cases

### 1. Security Auditing
Monitor your system during security reviews to understand what applications are making network connections.

```bash
jarvis -monitor network -m drona -b <bot-id>
```

### 2. Malware Detection
Detect malware or spyware attempting to communicate with command-and-control (C&C) servers.

### 3. Data Exfiltration Prevention
Identify applications attempting to upload sensitive data without authorization.

### 4. Compliance Monitoring
Audit network activity for compliance requirements or investigations.

### 5. Learning Tool
Understand which applications on your system make network connections and where they connect.

## Tips and Best Practices

### 1. Use AI Analysis
For best results, use an AI model (especially Drona) to get intelligent threat analysis:

```bash
jarvis -monitor network -m drona -b <bot-id>
```

### 2. Check Unknown Applications
Pay special attention to alerts from applications you don't recognize or that are running from unusual locations (like /tmp, /var/tmp, etc.).

### 3. Investigate HIGH/CRITICAL Alerts
Take immediate action on any connection marked as HIGH or CRITICAL threat level:
- Terminate the process: `kill <PID>`
- Investigate the executable
- Check for other suspicious files
- Run a security scan

### 4. Monitor During Sensitive Operations
Run network monitoring during:
- Software installations
- Opening suspicious files
- After system compromise
- During incident response

### 5. Understand Normal Patterns
Learn what normal connections look like for your applications so you can spot anomalies.

## Common Scenarios

### Scenario 1: Legitimate Application
```
Process: Chrome
Remote: google.com:443
Threat Level: LOW
Action: Allow - normal browsing activity
```

### Scenario 2: Suspicious Application
```
Process: unknown_app
Path: /tmp/unknown_app
Remote: unknown-domain.xyz:8080
Threat Level: HIGH
Action: Block - investigate immediately
```

### Scenario 3: Development Tools
```
Process: node
Remote: registry.npmjs.org:443
Threat Level: LOW
Action: Allow - normal package manager activity
```

## Troubleshooting

### No Alerts Appearing
- Make sure you're generating new network activity (open a browser, etc.)
- The baseline includes all current connections, so only NEW connections trigger alerts
- Some applications may reuse existing connections

### Permission Errors
- You may need elevated permissions to see all network connections
- Try running with `sudo` if needed (use with caution)

### Too Many Alerts
- Normal for systems with many active applications
- Use AI analysis to help filter legitimate vs. suspicious connections
- Focus on HIGH and CRITICAL threat levels

## Requirements

### System Requirements
- macOS (tested on macOS 10.13+)
- psutil library (automatically installed)

### Optional Requirements
- AI model configured for threat analysis (Gemini, SLM, or Drona)
- Internet connection (for AI analysis)

## Configuration

### Configure AI Model

**Gemini:**
```bash
jarvis configure -m gemini --api-key <your-api-key>
```

**Drona:**
```bash
jarvis configure -m drona -b <your-bot-id>
```

**SLM:**
```bash
jarvis configure -m slm --url <server-url>
```

## Security Considerations

### Privacy
Network monitoring sees all outbound connections from your system. This data is:
- Only displayed locally on your terminal
- Only sent to AI services for threat analysis (when AI is enabled)
- Not stored or logged anywhere

### AI Analysis
When using AI threat analysis:
- Connection details are sent to the AI service for analysis
- This includes process names, paths, and network addresses
- Use trusted AI services only
- Consider running without AI for maximum privacy

### Permissions
Network monitoring requires permission to read network connection information:
- May require elevated permissions on some systems
- Use caution when running with `sudo`

## Examples

### Example 1: Basic Monitoring
```bash
jarvis -monitor network
```
Simple monitoring without AI analysis. Shows connection details only.

### Example 2: With AI Analysis
```bash
jarvis -monitor network -m drona -b my_bot_id
```
Full monitoring with AI threat analysis and recommendations.

### Example 3: During Security Incident
```bash
# Start monitoring
jarvis -monitor network -m drona -b my_bot_id

# In another terminal, investigate suspicious process
ps aux | grep <process-name>
lsof -p <PID>
```

## Support

For issues or questions:
- Check the main README.md
- Review RELEASE_NOTES.md for known issues
- Report issues on GitHub

## Related Features

- **Security Scanning**: `jarvis -scan -f <folder> -m drona -b <bot-id>`
- **System Health**: `jarvis "check system health"`
- **Process Monitoring**: `jarvis "show running processes"`

---

**Version**: 1.5.0  
**Last Updated**: December 2024

