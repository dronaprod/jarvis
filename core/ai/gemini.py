"""
Google Gemini AI provider
"""

import sys
from pathlib import Path
from typing import Optional

# Add parent directories to path for imports
_project_root = Path(__file__).parent.parent.parent
if str(_project_root) not in sys.path:
    sys.path.insert(0, str(_project_root))

from utils.config import load_config
from core.ai.base import AIProvider


class GeminiProvider(AIProvider):
    """Google Gemini AI provider"""
    
    def __init__(self):
        self.ai_model = None
        self.ai_available = False
    
    def setup(self) -> bool:
        """Setup Gemini connection"""
        try:
            import google.generativeai as genai
            
            config = load_config()
            api_key = config.get('gemini_api_key')
            model_name = config.get('gemini_model_name', 'gemini-2.5-flash')
            
            if not api_key:
                print("❌ Gemini API key not configured")
                print("❌ Please configure it using:")
                print("   jarvis configure -m gemini --api-key <your-api-key> [-n <model-name>]")
                print("💡 Get your API key from: https://makersuite.google.com/app/apikey")
                return False
            
            genai.configure(api_key=api_key)
            self.ai_model = genai.GenerativeModel(model_name)
            
            # Test the connection
            test_response = self.ai_model.generate_content("Hello")
            if test_response and test_response.text:
                self.ai_available = True
                print("✅ Gemini AI connected successfully")
                return True
            else:
                raise Exception("Gemini test failed")
                
        except Exception as e:
            print(f"❌ Gemini connection failed: {e}")
            print("❌ Jarvis requires AI connection to work")
            print("❌ Please check your internet connection and API key")
            if "403" in str(e) or "API key" in str(e):
                print("💡 Your API key may be invalid. Configure a new one:")
                print("   jarvis configure -m gemini --api-key <your-api-key>")
            return False
    
    def query(self, prompt: str, image_data: Optional[str] = None, image_mime_type: Optional[str] = None, **kwargs) -> Optional[str]:
        """Query Gemini with a prompt"""
        try:
            if not self.ai_available or not self.ai_model:
                return None
            
            if image_data and image_mime_type:
                import PIL.Image
                import io
                import base64
                
                # Decode base64 image
                image_bytes = base64.b64decode(image_data)
                image = PIL.Image.open(io.BytesIO(image_bytes))
                
                # Generate with image
                response = self.ai_model.generate_content([prompt, image])
            else:
                response = self.ai_model.generate_content(prompt)
            
            if response and response.text:
                return response.text.strip()
            return None
        except Exception as e:
            print(f"❌ Gemini query failed: {e}")
            return None
    
    def is_available(self) -> bool:
        """Check if Gemini is available"""
        return self.ai_available

