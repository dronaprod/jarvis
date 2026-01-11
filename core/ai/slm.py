"""
SLM (Self-hosted Language Model) provider
"""

import sys
from typing import Optional
import sys
from pathlib import Path

# Add parent directories to path for imports
_project_root = Path(__file__).parent.parent.parent
if str(_project_root) not in sys.path:
    sys.path.insert(0, str(_project_root))

from utils.config import load_config
from core.ai.base import AIProvider


class SLMProvider(AIProvider):
    """SLM server provider"""
    
    def __init__(self):
        self.slm_url = None
        self.ai_available = False
    
    def setup(self) -> bool:
        """Setup SLM connection"""
        try:
            config = load_config()
            self.slm_url = config.get('slm_url', 'http://35.174.147.167:5000')
            
            # Test the connection
            test_response = self.query("Hello")
            if test_response:
                self.ai_available = True
                print("✅ SLM AI connected successfully")
                return True
            else:
                raise Exception("SLM test failed")
                
        except Exception as e:
            print(f"❌ SLM connection failed: {e}")
            print("❌ Jarvis requires AI connection to work")
            print("❌ Please check your internet connection to SLM server")
            print("💡 Configure SLM server URL using:")
            print("   jarvis configure -m slm --url <server-url>")
            return False
    
    def query(self, prompt: str, **kwargs) -> Optional[str]:
        """Query SLM server"""
        try:
            import requests
            response = requests.post(
                f"{self.slm_url}/generate",
                json={"prompt": prompt},
                timeout=30
            )
            if response.status_code == 200:
                return response.json().get("response", "")
            else:
                print(f"❌ SLM server error: {response.status_code}")
                return None
        except ImportError:
            print(f"❌ requests module not found. Please install it: pip3 install requests")
            return None
        except Exception as e:
            print(f"❌ SLM query failed: {e}")
            return None
    
    def is_available(self) -> bool:
        """Check if SLM is available"""
        return self.ai_available

