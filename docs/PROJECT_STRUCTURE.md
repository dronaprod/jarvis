# 📁 Jarvis Project Structure

This document describes the professional structure of the Jarvis AI Assistant project.

## 🏗️ Directory Structure

```
jarvis/
├── jarvis/                    # Main package
│   ├── __init__.py           # Package initialization and exports
│   ├── __main__.py           # Entry point for `python -m jarvis`
│   │
│   ├── core/                 # Core functionality
│   │   ├── __init__.py
│   │   ├── jarvis.py        # Main Jarvis class
│   │   │
│   │   ├── ai/              # AI model integrations
│   │   │   ├── __init__.py
│   │   │   ├── base.py      # Base AI interface
│   │   │   ├── gemini.py    # Google Gemini integration
│   │   │   ├── slm.py       # SLM server integration
│   │   │   └── drona.py     # Drona API integration
│   │   │
│   │   ├── monitoring/      # Monitoring modules
│   │   │   ├── __init__.py
│   │   │   ├── network.py   # Network monitoring
│   │   │   └── process.py  # Process monitoring
│   │   │
│   │   └── security/       # Security features
│   │       ├── __init__.py
│   │       └── scanner.py  # Security file scanning
│   │
│   ├── utils/               # Utility modules
│   │   ├── __init__.py
│   │   ├── config.py        # Configuration management
│   │   ├── notifications.py # Desktop notifications
│   │   └── system_info.py   # System information
│   │
│   └── cli/                # Command-line interface
│       ├── __init__.py
│       ├── main.py         # Main CLI entry point
│       ├── parser.py       # Argument parsing
│       └── commands.py     # Command handlers
│
├── tests/                   # Test suite
│   ├── __init__.py
│   ├── test_core/
│   ├── test_utils/
│   └── test_cli/
│
├── docs/                    # Documentation
│   ├── NETWORK_MONITORING_GUIDE.md
│   ├── PROCESS_MONITORING_GUIDE.md
│   └── ...
│
├── scripts/                 # Build and utility scripts
│   ├── build.sh
│   ├── build-universal.sh
│   └── prepare-release.sh
│
├── setup.py                 # Package setup configuration
├── pyproject.toml          # Modern Python project config (optional)
├── requirements.txt        # Python dependencies
├── README.md              # Main documentation
├── RELEASE_NOTES.md       # Release changelog
└── PROJECT_STRUCTURE.md   # This file
```

## 📦 Package Organization

### Core Package (`jarvis/`)

The main package contains all application logic organized by functionality:

#### `core/` - Core Functionality
- **`jarvis.py`**: Main Jarvis class that orchestrates all features
- **`ai/`**: AI model integrations (Gemini, SLM, Drona)
- **`monitoring/`**: Real-time monitoring (network, processes)
- **`security/`**: Security scanning and threat detection

#### `utils/` - Utilities
- **`config.py`**: Configuration file management
- **`notifications.py`**: Cross-platform desktop notifications
- **`system_info.py`**: System information collection

#### `cli/` - Command-Line Interface
- **`main.py`**: Main entry point for CLI
- **`parser.py`**: Argument parsing and validation
- **`commands.py`**: Command handlers (configure, monitor, scan, etc.)

## 🔄 Migration from Monolithic Structure

The project has been restructured from a single `jarvis.py` file (2692 lines) into a modular package structure:

### Before (v1.5.0 and earlier):
```
jarvis.py  # Single 2692-line file
```

### After (v1.5.1+):
```
jarvis/
  ├── core/
  ├── utils/
  └── cli/
```

### Benefits:
1. **Maintainability**: Easier to find and modify specific features
2. **Testability**: Each module can be tested independently
3. **Scalability**: Easy to add new features without bloating files
4. **Code Reuse**: Utilities can be shared across modules
5. **Type Safety**: Easier to add type hints and validation
6. **Documentation**: Better organization for docstrings

## 🚀 Installation

### Development Installation
```bash
# Install in development mode
pip install -e .

# Or with development dependencies
pip install -e ".[dev]"
```

### Production Installation
```bash
# Install from source
pip install .

# Or from PyPI (when published)
pip install jarvis-ai
```

## 📝 Entry Points

The package can be run in multiple ways:

1. **CLI Command** (after installation):
   ```bash
   jarvis "your question"
   ```

2. **Python Module**:
   ```bash
   python -m jarvis "your question"
   ```

3. **Direct Script** (backward compatible):
   ```bash
   python jarvis.py "your question"
   ```

## 🧪 Testing

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=jarvis

# Run specific test module
pytest tests/test_core/
```

## 📚 Module Responsibilities

### Core Modules

- **`core.jarvis`**: Main application class, orchestrates all features
- **`core.ai.*`**: AI model integrations, each model in separate file
- **`core.monitoring.*`**: Monitoring features, separated by type
- **`core.security.*`**: Security scanning features

### Utility Modules

- **`utils.config`**: Handles `~/.jarvis/config.json` operations
- **`utils.notifications`**: Cross-platform notification system
- **`utils.system_info`**: System metrics and information

### CLI Modules

- **`cli.main`**: Entry point, routes to appropriate handlers
- **`cli.parser`**: Argument parsing and validation
- **`cli.commands`**: Command execution logic

## 🔧 Development Guidelines

### Adding New Features

1. **AI Models**: Add to `jarvis/core/ai/`
2. **Monitoring**: Add to `jarvis/core/monitoring/`
3. **Security**: Add to `jarvis/core/security/`
4. **Utilities**: Add to `jarvis/utils/`
5. **CLI Commands**: Add to `jarvis/cli/commands.py`

### Code Style

- Use type hints for function parameters and return values
- Add docstrings to all public functions and classes
- Follow PEP 8 style guide
- Use meaningful variable and function names

### Testing

- Write tests for new features in `tests/`
- Maintain test coverage above 80%
- Test on multiple platforms (macOS, Linux, Windows)

## 📦 Distribution

The package can be distributed as:
- **Source distribution**: `python setup.py sdist`
- **Wheel distribution**: `python setup.py bdist_wheel`
- **Binary distribution**: Using PyInstaller (existing scripts)

## 🔄 Backward Compatibility

The old `jarvis.py` file is maintained for backward compatibility but will be deprecated in future versions. New installations should use the package structure.

---

**Version**: 1.5.1  
**Last Updated**: December 2024

