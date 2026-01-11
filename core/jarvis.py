"""
Main Jarvis class - Orchestrates all functionality
Uses modular AI providers, utilities, and monitoring
"""

import sys
import os
import json
import re
import subprocess
import time
import base64
from pathlib import Path
from typing import Optional, Dict, Any

# Add project root to path for imports
_project_root = Path(__file__).parent.parent
if str(_project_root) not in sys.path:
    sys.path.insert(0, str(_project_root))

from core.ai.gemini import GeminiProvider
from core.ai.slm import SLMProvider
from core.ai.drona import DronaProvider
from core.monitoring.network import NetworkMonitor
from core.monitoring.process import ProcessMonitor
from core.security.scanner import SecurityScanner
from core.voice.voice_mode import VoiceMode
from utils.config import load_config
from utils.system_info import SystemInfo
from utils.notifications import NotificationManager


class Jarvis:
    """Main Jarvis AI Assistant class"""
    
    def __init__(self, model='gemini', bot_id=None, image_path=None):
        """Initialize Jarvis with specified AI model"""
        self.running = True
        self.model = model
        self.bot_id = bot_id
        self.image_path = image_path
        self.image_data = None
        self.image_mime_type = None
        
        # Initialize AI provider
        self.ai_provider = None
        
        # Load image if provided
        if image_path:
            self.load_image(image_path)
        
        # Setup AI connection
        self.setup_ai()
    
    def load_image(self, image_path: str) -> None:
        """Load and encode image file to base64"""
        try:
            image_file = Path(image_path)
            if not image_file.exists():
                print(f"⚠️ Warning: Image file not found: {image_path}")
                return
            
            # Read image file and encode to base64
            with open(image_file, 'rb') as f:
                image_bytes = f.read()
                self.image_data = base64.b64encode(image_bytes).decode('utf-8')
            
            # Detect MIME type based on file extension
            ext = image_file.suffix.lower()
            mime_types = {
                '.jpg': 'image/jpeg',
                '.jpeg': 'image/jpeg',
                '.png': 'image/png',
                '.gif': 'image/gif',
                '.webp': 'image/webp',
                '.bmp': 'image/bmp'
            }
            self.image_mime_type = mime_types.get(ext, 'image/jpeg')
            
            print(f"✅ Image loaded: {image_path}")
        except Exception as e:
            print(f"⚠️ Warning: Failed to load image: {e}")
            self.image_data = None
    
    def setup_ai(self) -> None:
        """Setup AI connection using the appropriate provider"""
        if self.model == 'slm':
            self.ai_provider = SLMProvider()
        elif self.model == 'gemini':
            self.ai_provider = GeminiProvider()
        elif self.model == 'drona':
            self.ai_provider = DronaProvider(bot_id=self.bot_id)
        else:
            print(f"❌ Unknown model: {self.model}")
            print("❌ Supported models: 'slm', 'gemini', 'drona'")
            sys.exit(1)
        
        # Setup the provider
        if not self.ai_provider.setup():
            sys.exit(1)
    
    def get_system_info(self) -> str:
        """Get current system information as formatted string"""
        return SystemInfo.get_system_info_string()
    
    def process_query(self, query: str) -> None:
        """Process a query - LLM decides whether to use single or multi-step flow"""
        print(f"🤔 You asked: {query}")
        print("🤖 Processing...")
        
        # Always use unified flow - LLM decides through its responses
        self.unified_query_processing(query)
    
    def parse_json_response(self, response_text: str) -> Optional[Dict]:
        """Parse JSON response from LLM, handling both JSON and plain text"""
        # Try to extract JSON from response
        json_match = re.search(r'\{[^{}]*"command"[^{}]*\}', response_text, re.DOTALL)
        if json_match:
            try:
                json_str = json_match.group(0)
                return json.loads(json_str)
            except json.JSONDecodeError:
                pass
        
        # Try to find JSON block
        json_match = re.search(r'```json\s*(\{.*?\})\s*```', response_text, re.DOTALL)
        if json_match:
            try:
                return json.loads(json_match.group(1))
            except json.JSONDecodeError:
                pass
        
        # Try to parse entire response as JSON
        try:
            return json.loads(response_text.strip())
        except json.JSONDecodeError:
            pass
        
        # No JSON found, return None to indicate plain text
        return None
    
    def unified_query_processing(self, query: str) -> None:
        """Unified query processing - LLM decides whether single or multi-step is needed"""
        try:
            # Get system info for context
            system_info = self.get_system_info()
            
            # Create unified prompt - LLM decides the approach
            prompt = self._build_query_prompt(query, system_info)
            
            # Process query with unified command execution flow
            self.execute_command_flow(query, prompt, system_info)
                
        except Exception as e:
            print(f"❌ Error processing query: {e}")
            print("❌ AI connection may be lost. Please restart Jarvis.")
    
    def _build_query_prompt(self, query: str, system_info: str) -> str:
        """Build the prompt for query processing"""
        from config.prompts import build_query_prompt
        return build_query_prompt(query, system_info)
    
    def execute_command_flow(self, initial_query: str, initial_prompt: str, system_info: str) -> None:
        """Execute command flow with intermediate/last command handling - Agentic iteration"""
        max_iterations = 10
        iteration = 0
        current_prompt = initial_prompt
        
        while iteration < max_iterations:
            iteration += 1
            
            # Show iteration progress for agentic flow
            if iteration > 1:
                print(f"\n🔄 Agentic iteration {iteration}/{max_iterations}...")
            
            # Get response from AI model
            if self.model == 'drona':
                response_text = self.ai_provider.query(current_prompt, image_data=self.image_data, test=False)
            elif self.model == 'gemini':
                response_text = self.ai_provider.query(current_prompt, image_data=self.image_data, image_mime_type=self.image_mime_type)
            else:  # slm
                response_text = self.ai_provider.query(current_prompt)
            
            if not response_text:
                raise Exception(f"{self.model} query failed")
            
            # Try to parse as JSON
            json_response = self.parse_json_response(response_text)
            if json_response:
                print(f"📋 AI Response (iteration {iteration}): {json_response}")
            
            if json_response and "command" in json_response:
                # Command execution needed
                command = json_response["command"]
                command_number = json_response.get("command_number", "last")
                
                # Safety check: If query needs analysis but LLM said "last", treat as "intermediate"
                analysis_keywords = ["is", "check", "analyze", "what", "why", "how", "show", "tell", "normal", "usage", "health", "status"]
                query_lower = initial_query.lower()
                needs_analysis = any(keyword in query_lower for keyword in analysis_keywords)
                
                if needs_analysis and command_number == "last" and iteration == 1:
                    print(f"⚠️  Query appears to need analysis, treating as intermediate...")
                    command_number = "intermediate"
                
                print(f"\n🚀 Executing command: {command}")
                if command_number == "intermediate":
                    print("🔄 This is an intermediate command - more iterations may follow...")
                    print(f"📋 Original query: {initial_query}")
                
                # Execute command and get results
                result = self.execute_command_silent(command)
                
                # Show result to user
                self.show_command_result(command, result)
                
                # Check if command was successful
                if result["success"]:
                    print("✅ Command executed successfully!")
                else:
                    print("❌ Command failed!")
                
                # If last command, stop flow
                if command_number == "last":
                    print("\n✅ Agentic flow complete!")
                    break
                
                # If intermediate, send output back to LLM and continue
                if command_number == "intermediate":
                    output_text = result["stdout"] if result["stdout"] else result["stderr"]
                    if not output_text:
                        output_text = "Command executed with no output"
                    
                    print(f"\n🔄 Analyzing output and determining next steps...")
                    print(f"📤 Sending command output back to LLM with original query...")
                    
                    # Update prompt for next iteration - ALWAYS include original query
                    from config.prompts import build_iteration_prompt
                    current_prompt = build_iteration_prompt(
                        initial_query, system_info, command, output_text, result["success"]
                    )
                    
                    continue
            else:
                # Plain text response - print directly
                print("\n" + "=" * 60)
                print("📝 Response:")
                print("=" * 60)
                print(response_text)
                print("=" * 60)
                print()
                break
        
        if iteration >= max_iterations:
            print("\n⚠️ Maximum iterations reached. Stopping flow.")
    
    def sanitize_command(self, command: str) -> str:
        """Convert interactive commands to non-interactive versions to prevent timeouts"""
        command_lower = command.lower().strip()
        
        # Convert top commands to non-interactive versions
        if command_lower.startswith('top ') and '-l' not in command_lower:
            if 'top -' in command_lower:
                command = command.replace('top ', 'top -l 1 ', 1)
            elif command_lower == 'top':
                command = 'top -l 1'
            else:
                command = command.replace('top ', 'top -l 1 ', 1)
        
        # Convert other potentially interactive commands
        if 'htop' in command_lower or 'btop' in command_lower:
            if 'htop' in command_lower:
                command = command.replace('htop', 'top -l 1', 1)
            if 'btop' in command_lower:
                command = command.replace('btop', 'top -l 1', 1)
        
        return command
    
    def execute_command_silent(self, command: str) -> Dict[str, Any]:
        """Execute command and return results without showing to user"""
        try:
            # Sanitize command to prevent interactive/timeout issues
            sanitized_command = self.sanitize_command(command)
            if sanitized_command != command:
                print(f"⚠️  Auto-converted interactive command: {command} → {sanitized_command}")
            
            result = subprocess.run(sanitized_command, shell=True, capture_output=True, text=True, timeout=30)
            return {
                "success": result.returncode == 0,
                "stdout": result.stdout,
                "stderr": result.stderr,
                "returncode": result.returncode
            }
        except subprocess.TimeoutExpired:
            return {
                "success": False,
                "stdout": "",
                "stderr": "Command timed out",
                "returncode": -1
            }
        except Exception as e:
            return {
                "success": False,
                "stdout": "",
                "stderr": str(e),
                "returncode": -1
            }
    
    def show_command_result(self, command: str, result: Dict[str, Any]) -> None:
        """Show command execution result to user"""
        print("\n" + "=" * 60)
        print("🚀 Command Executed:")
        print("=" * 60)
        print(f"Command: {command}")
        print("-" * 60)
        
        if result["success"]:
            print("✅ Command executed successfully!")
            if result["stdout"]:
                print("\nOutput:")
                print(result["stdout"])
        else:
            print("❌ Command failed!")
            if result["stderr"]:
                print("\nError:")
                print(result["stderr"])
        
        print("=" * 60)
    
    def clear_screen(self) -> None:
        """Clear the console screen"""
        os.system('clear' if os.name == 'posix' else 'cls')
    
    def print_header(self) -> None:
        """Print the header"""
        import platform
        print("=" * 60)
        print("🤖 JARVIS - Global Terminal AI Copilot")
        print("=" * 60)
        print(f"System: {platform.system()} {platform.release()}")
        print(f"Python: {sys.version.split()[0]}")
        print(f"Working Directory: {os.getcwd()}")
        print(f"AI Model: {self.model.upper()}")
        print("AI Status: ✅ Connected")
        print("=" * 60)
        print()
    
    def print_help(self) -> None:
        """Print help information"""
        print("📋 Available Commands:")
        print("  help, h     - Show this help")
        print("  test, t     - Test the system")
        print("  clear, c    - Clear screen")
        print("  pwd         - Show current directory")
        print("  ls          - List files in current directory")
        print("  quit, q     - Exit Jarvis")
        print("  <question>  - Ask Jarvis anything")
        print()
    
    def run(self) -> None:
        """Main run loop - Interactive mode"""
        self.clear_screen()
        self.print_header()
        self.print_help()
        
        while self.running:
            try:
                # Get user input
                user_input = input("Jarvis> ").strip()
                
                if not user_input:
                    continue
                
                # Process commands
                if user_input.lower() in ['quit', 'q', 'exit']:
                    print("👋 Goodbye!")
                    break
                elif user_input.lower() in ['help', 'h']:
                    self.print_help()
                elif user_input.lower() in ['test', 't']:
                    print("✅ All systems operational")
                elif user_input.lower() in ['clear', 'c']:
                    self.clear_screen()
                    self.print_header()
                    self.print_help()
                elif user_input.lower() == 'pwd':
                    print(f"Current directory: {os.getcwd()}")
                elif user_input.lower() == 'ls':
                    result = self.execute_command_silent('ls -la')
                    if result["stdout"]:
                        print(result["stdout"])
                else:
                    self.process_query(user_input)
                    
            except KeyboardInterrupt:
                print("\n👋 Goodbye!")
                break
            except EOFError:
                print("\n👋 Goodbye!")
                break
            except Exception as e:
                print(f"❌ Error: {e}")
                print()
    
    def monitor_network(self) -> None:
        """Monitor network connections using NetworkMonitor"""
        notification_manager = NotificationManager(debug=True)
        monitor = NetworkMonitor(
            model=self.model,
            ai_provider=self.ai_provider,
            notification_manager=notification_manager
        )
        monitor.monitor()
    
    def monitor_processes(self) -> None:
        """Monitor processes using ProcessMonitor"""
        notification_manager = NotificationManager(debug=True)
        monitor = ProcessMonitor(
            model=self.model,
            ai_provider=self.ai_provider,
            notification_manager=notification_manager
        )
        monitor.monitor()
    
    def scan_folder(self, folder_path: str) -> None:
        """Scan folder for sensitive files using SecurityScanner"""
        if self.model != 'drona':
            print("❌ Scan feature is only available with -m drona")
            return
        
        scanner = SecurityScanner(ai_provider=self.ai_provider)
        scanner.scan_folder(folder_path, model=self.model)
    
    def run_voice_mode(self) -> None:
        """Run voice command mode using VoiceMode"""
        voice_mode = VoiceMode(self)
        voice_mode.run()

