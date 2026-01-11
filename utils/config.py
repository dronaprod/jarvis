"""
Configuration management for Jarvis
Handles loading and saving configuration from ~/.jarvis/config.json
"""

import json
from pathlib import Path
from typing import Dict, Any


def get_config_path() -> Path:
    """Get the path to the config file"""
    config_dir = Path.home() / ".jarvis"
    config_dir.mkdir(exist_ok=True)
    return config_dir / "config.json"


def load_config() -> Dict[str, Any]:
    """Load configuration from file"""
    config_file = get_config_path()
    if config_file.exists():
        try:
            with open(config_file, 'r') as f:
                return json.load(f)
        except (json.JSONDecodeError, IOError):
            return {}
    return {}


def save_config(config: Dict[str, Any]) -> None:
    """Save configuration to file"""
    config_file = get_config_path()
    with open(config_file, 'w') as f:
        json.dump(config, f, indent=2)

