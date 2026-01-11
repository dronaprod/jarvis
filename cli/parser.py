"""
Command-line argument parser for Jarvis
"""

import argparse
from utils.config import load_config


def create_parser() -> argparse.ArgumentParser:
    """
    Create and configure the argument parser for Jarvis
    
    Returns:
        Configured ArgumentParser instance
    """
    # Get default model from config
    config = load_config()
    default_model = config.get('default_model', 'gemini')
    
    # Main parser
    parser = argparse.ArgumentParser(
        description='Jarvis - Global Terminal AI Copilot',
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    
    # Subcommands (optional - only used when 'configure' is specified)
    subparsers = parser.add_subparsers(dest='command', help='Available commands')
    
    # Configure command
    configure_parser = subparsers.add_parser('configure', help='Configure AI model settings')
    configure_parser.add_argument(
        '-m', '--model',
        choices=['slm', 'gemini', 'drona'],
        required=True,
        help='AI model to configure'
    )
    configure_parser.add_argument(
        '-n', '--name',
        dest='model_name',
        help='Model name for Gemini (e.g., gemini-2.5-flash, gemini-pro)'
    )
    configure_parser.add_argument(
        '--api-key',
        dest='api_key',
        help='API key for Gemini model'
    )
    configure_parser.add_argument(
        '--url',
        dest='url',
        help='Server URL for SLM or Drona model'
    )
    configure_parser.add_argument(
        '-b', '--bot-id',
        dest='bot_id',
        help='Bot ID for Drona model'
    )
    configure_parser.add_argument(
        '--set-default',
        dest='set_default',
        action='store_true',
        help='Set this model as the default model'
    )
    
    # Query command (default - positional arguments)
    parser.add_argument(
        'query',
        nargs='*',
        help='Query to ask Jarvis'
    )
    parser.add_argument(
        '-m', '--model',
        choices=['slm', 'gemini', 'drona'],
        default=default_model,
        help=f'AI model to use (default: {default_model} from config, or gemini)'
    )
    parser.add_argument(
        '-b', '--bot-id',
        dest='bot_id',
        help='Bot ID for Drona model (required when using -m drona)'
    )
    parser.add_argument(
        '-img', '--image',
        dest='image_path',
        help='Path to image file to send with the query'
    )
    parser.add_argument(
        '-v', '--voice',
        action='store_true',
        help='Enable voice command mode'
    )
    parser.add_argument(
        '-scan', '--scan',
        action='store_true',
        help='Scan folder for sensitive files (requires -m drona)'
    )
    parser.add_argument(
        '-f', '--folder',
        dest='folder_path',
        help='Folder path to scan (required with -scan)'
    )
    parser.add_argument(
        '-monitor', '--monitor',
        dest='monitor_type',
        help='Monitor system activity (network, process, cpu, memory, disk)'
    )
    
    return parser

