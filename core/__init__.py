"""Core Jarvis functionality"""

# Optional import - module may not exist yet during migration
try:
    from core.jarvis import Jarvis
    __all__ = ['Jarvis']
except ImportError:
    __all__ = []

