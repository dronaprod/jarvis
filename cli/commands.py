"""
Command handlers for Jarvis CLI
"""

import sys
from typing import Any
# Imports will be done locally in functions


def handle_configure(args: Any) -> None:
    """Handle the configure command"""
    from utils.config import load_config, save_config
    
    # Map arguments
    model = args.model
    api_key = getattr(args, 'api_key', None)
    model_name = getattr(args, 'model_name', None)
    url = getattr(args, 'url', None)
    bot_id = getattr(args, 'bot_id', None)
    set_default = getattr(args, 'set_default', False)
    
    # Load existing config
    config = load_config()
    
    # Update config based on model
    if model == 'gemini':
        if api_key:
            config['gemini_api_key'] = api_key
        if model_name:
            config['gemini_model_name'] = model_name
    elif model == 'slm':
        if url:
            config['slm_url'] = url
    elif model == 'drona':
        if url:
            config['drona_url'] = url
        if bot_id:
            config['drona_bot_id'] = bot_id
    
    # Set default model if requested
    if set_default:
        config['default_model'] = model
        if bot_id:
            config['default_bot_id'] = bot_id
        print(f"✅ Set {model} as default model")
    
    # Save config
    save_config(config)
    print(f"✅ Configuration updated for {model}")


def handle_monitor(args: Any) -> None:
    """Handle the monitor command"""
    from core.jarvis import Jarvis
    
    model = getattr(args, 'model', 'gemini')
    bot_id = getattr(args, 'bot_id', None)
    monitor_type = getattr(args, 'monitor_type', None)
    
    jarvis = Jarvis(model=model, bot_id=bot_id)
    
    if monitor_type == 'network':
        jarvis.monitor_network()
    elif monitor_type in ['process', 'processes']:
        jarvis.monitor_processes()
    else:
        print(f"❌ Unknown monitor type: {monitor_type}")
        sys.exit(1)


def handle_scan(args: Any) -> None:
    """Handle the scan command"""
    from core.jarvis import Jarvis
    
    model = getattr(args, 'model', 'drona')
    bot_id = getattr(args, 'bot_id', None)
    folder_path = getattr(args, 'folder_path', None)
    
    if model != 'drona':
        print("❌ Scan feature is only available with -m drona")
        sys.exit(1)
    
    if not folder_path:
        print("❌ Folder path is required with -scan")
        sys.exit(1)
    
    jarvis = Jarvis(model=model, bot_id=bot_id)
    jarvis.scan_folder(folder_path)


def handle_query(args: Any) -> None:
    """Handle query commands"""
    from core.jarvis import Jarvis
    
    model = getattr(args, 'model', 'gemini')
    bot_id = getattr(args, 'bot_id', None)
    image_path = getattr(args, 'image_path', None)
    voice = getattr(args, 'voice', False)
    query = getattr(args, 'query', [])
    
    jarvis = Jarvis(model=model, bot_id=bot_id, image_path=image_path)
    
    if voice:
        jarvis.run_voice_mode()
    elif query:
        query_str = ' '.join(query)
        jarvis.process_query(query_str)
    else:
        jarvis.run()

