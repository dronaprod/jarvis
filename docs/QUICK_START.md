# 🚀 Quick Start Guide

## Installation

1. **Install dependencies:**
   ```bash
   pip3 install -r requirements.txt
   ```

2. **Configure an AI model** (choose one):
   ```bash
   # Option 1: Gemini
   python3 -m cli.main configure -m gemini --api-key <your-api-key> --set-default
   
   # Option 2: SLM
   python3 -m cli.main configure -m slm --url http://your-server:5000 --set-default
   
   # Option 3: Drona
   python3 -m cli.main configure -m drona -b <bot-id> --set-default
   ```

## Running the Project

### Method 1: Run as Module (Recommended)
```bash
# Interactive mode
python3 -m cli.main

# Query mode
python3 -m cli.main "your question here"

# Network monitoring
python3 -m cli.main -monitor network

# Process monitoring
python3 -m cli.main -monitor process

# Security scan
python3 -m cli.main -scan -f /path/to/folder -m drona -b <bot-id>

# Voice mode
python3 -m cli.main -v
```

### Method 2: Direct Execution
```bash
python3 cli/main.py "your question here"
```

### Method 3: Install and Run (After Setup)
```bash
# Install
pip3 install -e .

# Run from anywhere
jarvis "your question here"
```

## Common Examples

```bash
# Ask a question
python3 -m cli.main "what files are in this directory?"

# Check system health
python3 -m cli.main "is my CPU usage normal?"

# Monitor network (may need sudo on macOS)
sudo python3 -m cli.main -monitor network

# Monitor processes
python3 -m cli.main -monitor process

# Scan folder for sensitive files
python3 -m cli.main -scan -f ~/Documents -m drona -b <bot-id>

# Voice commands
python3 -m cli.main -v
# Then say: "jarvis list files"
```

## Help

```bash
python3 -m cli.main --help
python3 -m cli.main configure --help
```

For detailed documentation, see `docs/RUNNING_THE_PROJECT.md`

