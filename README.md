# 🤖 Jarvis AI Assistant

Your personal AI assistant for macOS, Linux, and Windows - Terminal Interface

> **📚 Full Documentation**: See [jarvis/docs/README.md](jarvis/docs/README.md) for complete documentation

## 🚀 Quick Start

### Installation

1. **Install dependencies:**
   ```bash
   pip3 install -r requirements.txt
   ```

2. **Configure an AI model** (at least one required):
   ```bash
   # Gemini
   python3 -m cli.main configure -m gemini --api-key <your-api-key> --set-default
   
   # SLM
   python3 -m cli.main configure -m slm --url http://your-server:5000 --set-default
   
   # Drona
   python3 -m cli.main configure -m drona -b <bot-id> --set-default
   ```

### Running the Project

**Method 1: Run as Module (Recommended)**
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

**Method 2: Direct Execution**
```bash
python3 cli/main.py "your question here"
```

**Method 3: Install as Package**
```bash
# Install
pip3 install -e .

# Run from anywhere
jarvis "your question here"
```

## 📁 Project Structure

```
.
├── core/          # Core functionality
│   ├── ai/        # AI providers (Gemini, SLM, Drona)
│   ├── monitoring/# Network & process monitoring
│   ├── security/  # Security scanning
│   ├── voice/     # Voice commands
│   └── jarvis.py  # Main orchestrator class
├── utils/         # Utilities (config, notifications, system_info)
├── cli/           # Command-line interface
├── scripts/       # Build and installation scripts
├── docs/          # Documentation
└── backup/        # Backup files (original jarvis.py)
```

## 📚 Documentation

- **[Running the Project](docs/RUNNING_THE_PROJECT.md)** - How to run and use Jarvis
- **[Quick Start](docs/QUICK_START.md)** - Quick reference guide
- **[Release Notes](docs/RELEASE_NOTES.md)** - Version history
- **[Project Structure](docs/PROJECT_STRUCTURE.md)** - Developer guide
- **[Migration Status](docs/MIGRATION_COMPLETE.md)** - Migration documentation

## 🔧 Scripts

All build and installation scripts are in `scripts/`:
- `build.sh` - Build binary
- `build-universal.sh` - Build universal binary
- `prepare-release.sh` - Prepare release
- `install_jarvis_user.sh` - User installation

## 🎯 Usage Examples

```bash
# Ask a question
python3 -m cli.main "what files are in this directory?"

# Monitor network (may need sudo on macOS)
sudo python3 -m cli.main -monitor network

# Monitor processes
python3 -m cli.main -monitor process

# Security scan
python3 -m cli.main -scan -f ~/Documents -m drona -b <bot-id>

# Voice mode
python3 -m cli.main -v

# Configure model
python3 -m cli.main configure -m drona -b <bot-id> --set-default
```

For complete usage instructions, see [docs/RUNNING_THE_PROJECT.md](docs/RUNNING_THE_PROJECT.md).

## 📦 Installation

See [docs/RUNNING_THE_PROJECT.md](docs/RUNNING_THE_PROJECT.md) for detailed installation and usage instructions.

---

**Version**: 1.5.1  
**License**: MIT

