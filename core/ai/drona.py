"""
Drona API provider
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
from utils.system_info import SystemInfo
from core.ai.base import AIProvider


class DronaProvider(AIProvider):
    """Drona API provider"""
    
    def __init__(self, bot_id: Optional[str] = None):
        self.drona_url = None
        self.bot_id = bot_id
        self.ai_available = False
    
    def setup(self) -> bool:
        """Setup Drona connection"""
        try:
            config = load_config()
            self.drona_url = config.get('drona_url', 'https://api.vtorlabs.com/drona/v1/jarvis/chat')
            
            # Use provided bot_id or fall back to config
            if not self.bot_id:
                self.bot_id = config.get('drona_bot_id')
            
            if not self.bot_id:
                print("❌ Bot ID is required for Drona mode")
                print("❌ Please provide it using:")
                print("   jarvis 'your message' -m drona -b <bot_id>")
                print("   Or configure it: jarvis configure -m drona -b <bot_id>")
                return False
            
            # Skip test connection - just mark as available
            # The actual query will test the connection naturally
            self.ai_available = True
            print("✅ Drona AI ready")
            return True
                
        except Exception as e:
            print(f"❌ Drona connection failed: {e}")
            print("❌ Jarvis requires AI connection to work")
            print("❌ Please check your internet connection to Drona server")
            print(f"💡 URL being used: {self.drona_url}")
            print(f"💡 Bot ID being used: {self.bot_id}")
            print("💡 Configure Drona server URL using:")
            print("   jarvis configure -m drona --url <server-url>")
            return False
    
    def query(self, message: str, image_data: Optional[str] = None, test: bool = False, **kwargs) -> Optional[str]:
        """Query Drona server with message, machine details, IP address, and optionally image"""
        try:
            import requests
            
            # Get machine details and IP address
            machine_details = SystemInfo.get_machine_details()
            ip_address = SystemInfo.get_ip_address()
            
            # Prepare the payload
            payload = {
                "message": message,
                "bot_id": self.bot_id,
                "machine_details": machine_details,
                "ip_address": ip_address
            }
            
            # Add image data if available
            if image_data:
                payload["image"] = image_data
            
            # Make API call
            response = requests.post(
                self.drona_url,
                json=payload,
                timeout=30
            )
            
            if response.status_code == 200:
                result = response.json()
                return result.get("response", result.get("message", result.get("text", "")))
            else:
                if not test:
                    print(f"❌ Drona API server error: HTTP {response.status_code}")
                    try:
                        error_detail = response.json()
                        error_msg = error_detail.get("error", str(error_detail))
                        print(f"❌ Server error message: {error_msg}")
                        if response.status_code == 500:
                            print("💡 This appears to be a server-side issue. Please contact the API administrator.")
                    except:
                        print(f"❌ Error response: {response.text[:200]}")
                return None
        except ImportError:
            if not test:
                print(f"❌ requests module not found. Please install it: pip3 install requests")
            return None
        except Exception as e:
            if not test:
                print(f"❌ Drona query failed: {e}")
            elif test:
                print(f"⚠️ Drona test error: {e}")
            return None
    
    def is_available(self) -> bool:
        """Check if Drona is available"""
        return self.ai_available

