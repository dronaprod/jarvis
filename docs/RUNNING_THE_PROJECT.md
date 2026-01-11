# 🚀 How to Run the Project

## Quick Start

### Method 1: Run as Python Module (Recommended)

```bash
# From the project root directory
python3 -m cli.main "your question here"
```

Or with options:
```bash
python3 -m cli.main "list files" -m gemini
python3 -m cli.main -monitor network
python3 -m cli.main -monitor process
python3 -m cli.main -scan -f /path/to/folder -m drona -b <bot_id>
python3 -m cli.main -v  # Voice mode
```

### Method 2: Direct Python Execution

```bash
# From the project root directory
python3 cli/main.py "your question here"
```

### Method 3: Install as Package (After Setup)

```bash
# Install the package
pip3 install -e .

# Then run from anywhere
jarvis "your question here"
jarvis -monitor network
jarvis -scan -f /path/to/folder -m drona
```

## 📋 Common Commands

### Interactive Mode
```bash
python3 -m cli.main
# Or
python3 cli/main.py
```
This starts an interactive session where you can type commands.

### Query Mode
```bash
python3 -m cli.main "what is the current directory?"
python3 -m cli.main "check CPU usage" -m gemini
python3 -m cli.main "analyze this folder" -m drona -b <bot_id>
```

### Configure AI Models
```bash
# Configure Gemini
python3 -m cli.main configure -m gemini --api-key <your-api-key> --set-default

# Configure SLM
python3 -m cli.main configure -m slm --url http://your-server:5000 --set-default

# Configure Drona
python3 -m cli.main configure -m drona --url http://your-server:5000 -b <bot-id> --set-default
```

### Network Monitoring
```bash
# Monitor network connections (may require sudo on macOS)
python3 -m cli.main -monitor network

# With specific AI model
python3 -m cli.main -monitor network -m gemini
```

### Process Monitoring
```bash
# Monitor processes for anomalies (may require sudo)
python3 -m cli.main -monitor process

# With specific AI model
python3 -m cli.main -monitor process -m drona -b <bot-id>
```

### Security Scanning
```bash
# Scan folder for sensitive files (requires Drona)
python3 -m cli.main -scan -f /path/to/folder -m drona -b <bot-id>
```

### Voice Mode
```bash
# Start voice command mode
python3 -m cli.main -v

# Say "jarvis" followed by your command
```

### With Images
```bash
# Query with an image
python3 -m cli.main "what's in this image?" -img /path/to/image.jpg -m gemini
```

## 🔧 Prerequisites

### Required Dependencies
```bash
pip3 install -r requirements.txt
```

### Optional Dependencies
```bash
# For voice mode
pip3 install SpeechRecognition pyaudio

# For monitoring (usually pre-installed)
pip3 install psutil
```

## 📝 Environment Setup

1. **Install Python 3.7+**
   ```bash
   python3 --version  # Should be 3.7 or higher
   ```

2. **Install Dependencies**
   ```bash
   cd /path/to/jarvis
   pip3 install -r requirements.txt
   ```

3. **Configure AI Model** (at least one)
   ```bash
   # Gemini
   python3 -m cli.main configure -m gemini --api-key <your-key>
   
   # Or SLM
   python3 -m cli.main configure -m slm --url http://your-server:5000
   
   # Or Drona
   python3 -m cli.main configure -m drona -b <bot-id>
   ```

## 🎯 Examples

### Basic Query
```bash
python3 -m cli.main "what files are in this directory?"
```

### System Analysis
```bash
python3 -m cli.main "check if my CPU usage is normal"
```

### Network Monitoring
```bash
# On macOS, may need sudo
sudo python3 -m cli.main -monitor network
```

### Security Scan
```bash
python3 -m cli.main -scan -f ~/Documents -m drona -b <bot-id>
```

### Voice Commands
```bash
python3 -m cli.main -v
# Then say: "jarvis list files in this directory"
```

## 🐛 Troubleshooting

### Import Errors
If you get import errors, make sure you're in the project root:
```bash
cd /path/to/jarvis
python3 -m cli.main
```

### Permission Errors (Monitoring)
On macOS, network and process monitoring may require elevated permissions:
```bash
sudo python3 -m cli.main -monitor network
```

### AI Connection Errors
Make sure you've configured at least one AI model:
```bash
python3 -m cli.main configure -m gemini --api-key <your-key>
```

### Module Not Found
If you see "ModuleNotFoundError", install dependencies:
```bash
pip3 install -r requirements.txt
```

## 📦 Installation Methods

### Development Installation
```bash
# Install in editable mode
pip3 install -e .

# Now you can run from anywhere
jarvis "your question"
```

### Production Installation
```bash
# Standard installation
pip3 install .

# Or from source
python3 setup.py install
```

## 🔍 Project Structure

```
jarvis/
├── core/           # Core functionality
│   ├── ai/         # AI providers
│   ├── monitoring/ # Network & process monitoring
│   ├── security/   # Security scanning
│   ├── voice/      # Voice commands
│   └── jarvis.py   # Main class
├── cli/            # Command-line interface
│   ├── main.py     # Entry point
│   ├── parser.py   # Argument parsing
│   └── commands.py # Command handlers
├── utils/          # Utilities
└── __main__.py     # Module entry point
```

## 💡 Tips

1. **Use `-m` flag to specify AI model**: `-m gemini`, `-m slm`, or `-m drona`
2. **Set default model**: Use `--set-default` when configuring
3. **Monitor requires permissions**: Use `sudo` on macOS for detailed monitoring
4. **Voice mode needs microphone**: Ensure microphone permissions are granted
5. **Scan requires Drona**: Security scanning only works with `-m drona`

---

**For more information, see the README.md file.**

