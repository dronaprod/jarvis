"""
Base AI provider interface
All AI providers should inherit from this class
"""

from abc import ABC, abstractmethod
from typing import Optional


class AIProvider(ABC):
    """Base class for AI providers"""
    
    @abstractmethod
    def setup(self) -> bool:
        """Setup the AI connection. Returns True if successful."""
        pass
    
    @abstractmethod
    def query(self, prompt: str, **kwargs) -> Optional[str]:
        """Query the AI with a prompt. Returns response text or None."""
        pass
    
    @abstractmethod
    def is_available(self) -> bool:
        """Check if AI is available and ready"""
        pass

