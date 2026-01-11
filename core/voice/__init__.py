"""Voice command functionality"""

try:
    from core.voice.voice_mode import VoiceMode
    __all__ = ['VoiceMode']
except ImportError:
    __all__ = []

