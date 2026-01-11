"""
Main CLI entry point for Jarvis
This provides a bridge to the existing jarvis.py while maintaining the new structure
"""

import sys
import os
from pathlib import Path

# Add parent directory to path to import the original jarvis.py
# This allows backward compatibility during migration
_project_root = Path(__file__).parent.parent
if str(_project_root) not in sys.path:
    sys.path.insert(0, str(_project_root))

# Import the main function from the original jarvis.py
# This will be gradually replaced with modular imports
try:
    # Try to import from the modular structure first
    from core.jarvis import Jarvis
    from cli.parser import create_parser
    from cli.commands import handle_configure, handle_monitor, handle_scan, handle_query
    MODULAR_IMPORTS = True
except ImportError:
    # Fallback to original jarvis.py
    MODULAR_IMPORTS = False


def main():
    """
    Main entry point for Jarvis CLI
    Routes to appropriate handlers based on command-line arguments
    """
    # For now, delegate to the original jarvis.py main function
    # This maintains backward compatibility
    if MODULAR_IMPORTS:
        # Use new modular structure
        _main_modular()
    else:
        # Fallback to original implementation
        _main_legacy()


def _main_legacy():
    """Legacy main function - imports from original jarvis.py"""
    # Import the main function from the original jarvis.py
    import importlib.util
    jarvis_py_path = _project_root / "jarvis.py"
    
    if jarvis_py_path.exists():
        spec = importlib.util.spec_from_file_location("jarvis_legacy", jarvis_py_path)
        jarvis_legacy = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(jarvis_legacy)
        
        if hasattr(jarvis_legacy, 'main'):
            jarvis_legacy.main()
        else:
            print("❌ Error: Could not find main() function in jarvis.py")
            sys.exit(1)
    else:
        print("❌ Error: jarvis.py not found")
        sys.exit(1)


def _main_modular():
    """New modular main function - uses the new package structure"""
    # Check if first argument is 'configure' - if so, use full parser with subcommands
    # Otherwise, parse as query (without requiring subcommand)
    if len(sys.argv) > 1 and sys.argv[1] == 'configure':
        parser = create_parser()
        args = parser.parse_args()
        
        # Route to configure handler
        if args.command == 'configure':
            handle_configure(args)
            return
    else:
        # For queries and other commands, use a simpler parser without subparsers
        import argparse
        from utils.config import load_config
        
        config = load_config()
        default_model = config.get('default_model', 'gemini')
        
        parser = argparse.ArgumentParser(description='Jarvis - Global Terminal AI Copilot')
        parser.add_argument('query', nargs='*', help='Query to ask Jarvis')
        parser.add_argument('-m', '--model', choices=['slm', 'gemini', 'drona'], 
                           default=default_model, help=f'AI model to use (default: {default_model})')
        parser.add_argument('-b', '--bot-id', dest='bot_id', help='Bot ID for Drona model')
        parser.add_argument('-img', '--image', dest='image_path', help='Path to image file')
        parser.add_argument('-v', '--voice', action='store_true', help='Enable voice mode')
        parser.add_argument('-scan', '--scan', action='store_true', help='Scan folder for sensitive files')
        parser.add_argument('-f', '--folder', dest='folder_path', help='Folder path to scan (required with -scan)')
        parser.add_argument('-monitor', '--monitor', dest='monitor_type', 
                           help='Monitor system activity (network, process)')
        
        args = parser.parse_args()
    
    # Route to appropriate handler
    if hasattr(args, 'monitor_type') and args.monitor_type:
        handle_monitor(args)
    elif hasattr(args, 'scan') and args.scan:
        handle_scan(args)
    else:
        handle_query(args)


if __name__ == "__main__":
    main()

