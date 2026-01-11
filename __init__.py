"""
Jarvis - Global Terminal AI Copilot

A professional AI assistant for macOS, Linux, and Windows with:
- Multi-model AI support (Gemini, SLM, Drona)
- Real-time network and process monitoring
- Security scanning and threat detection
- Voice commands
- Desktop notifications
"""

__version__ = "1.5.1"
__author__ = "Jarvis Team"
__license__ = "MIT"

# Optional imports - modules may not exist yet during migration
try:
    from core.jarvis import Jarvis
    __all__ = ['Jarvis', '__version__']
except ImportError:
    # During migration, core modules may not exist yet
    __all__ = ['__version__']

