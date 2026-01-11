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
    parser = create_parser()
    args = parser.parse_args()
    
    # Route to appropriate handler based on command
    if args.command == 'configure':
        handle_configure(args)
    elif hasattr(args, 'monitor_type') and args.monitor_type:
        handle_monitor(args)
    elif hasattr(args, 'scan') and args.scan:
        handle_scan(args)
    else:
        handle_query(args)


if __name__ == "__main__":
    main()

