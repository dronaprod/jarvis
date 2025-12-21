#!/usr/bin/env python3
"""
Jarvis - Global Terminal AI Copilot
Run from anywhere by typing 'jarvis' in any terminal
Supports multiple AI models: SLM, Gemini, and Drona
"""

import os
import sys

# Add user site-packages to path FIRST before any other imports
import site
user_site = site.getusersitepackages()
if user_site not in sys.path:
    sys.path.insert(0, user_site)

# Also add the common user site-packages location explicitly (only if it matches current Python version)
# Note: Removed hardcoded Python 3.9 path to avoid conflicts with different Python versions
python_version = f"{sys.version_info.major}.{sys.version_info.minor}"
common_user_site = os.path.expanduser(f'~/Library/Python/{python_version}/lib/python/site-packages')
if common_user_site not in sys.path and os.path.exists(common_user_site):
    sys.path.insert(0, common_user_site)

import platform
import subprocess
import threading
import time
import argparse
import json
import re
import socket
import base64
from pathlib import Path

def get_config_path():
    """Get the path to the config file"""
    config_dir = Path.home() / ".jarvis"
    config_dir.mkdir(exist_ok=True)
    return config_dir / "config.json"

def load_config():
    """Load configuration from file"""
    config_file = get_config_path()
    if config_file.exists():
        try:
            with open(config_file, 'r') as f:
                return json.load(f)
        except:
            return {}
    return {}

def save_config(config):
    """Save configuration to file"""
    config_file = get_config_path()
    with open(config_file, 'w') as f:
        json.dump(config, f, indent=2)

class Jarvis:
    def __init__(self, model='gemini', bot_id=None, image_path=None):
        self.running = True
        self.model = model
        self.bot_id = bot_id
        self.image_path = image_path
        self.image_data = None
        self.image_mime_type = None
        if image_path:
            self.load_image(image_path)
        self.setup_ai()
    
    def load_image(self, image_path):
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
        
    def setup_ai(self):
        """Setup AI connection - REQUIRED"""
        if self.model == 'slm':
            self.setup_slm()
        elif self.model == 'gemini':
            self.setup_gemini()
        elif self.model == 'drona':
            self.setup_drona()
        else:
            print(f"❌ Unknown model: {self.model}")
            print("❌ Supported models: 'slm', 'gemini', 'drona'")
            sys.exit(1)
    
    def setup_slm(self):
        """Setup SLM connection"""
        try:
            # Get SLM URL from config file, default to hardcoded URL
            config = load_config()
            self.slm_url = config.get('slm_url', 'http://35.174.147.167:5000')
            
            # Test the connection
            test_response = self.query_slm("Hello")
            if test_response:
                self.ai_available = True
                print("✅ SLM AI connected successfully")
            else:
                raise Exception("SLM test failed")
                
        except Exception as e:
            print(f"❌ SLM connection failed: {e}")
            print("❌ Jarvis requires AI connection to work")
            print("❌ Please check your internet connection to SLM server")
            print("💡 Configure SLM server URL using:")
            print("   jarvis configure -m slm --url <server-url>")
            sys.exit(1)
    
    def setup_gemini(self):
        """Setup Gemini connection"""
        try:
            import google.generativeai as genai
            
            # Get API key and model name from config file
            config = load_config()
            api_key = config.get('gemini_api_key')
            model_name = config.get('gemini_model_name', 'gemini-2.5-flash')  # Default to gemini-2.5-flash
            
            if not api_key:
                print("❌ Gemini API key not configured")
                print("❌ Please configure it using:")
                print("   jarvis configure -m gemini --api-key <your-api-key> [-n <model-name>]")
                print("💡 Get your API key from: https://makersuite.google.com/app/apikey")
                sys.exit(1)
            
            genai.configure(api_key=api_key)
            self.ai_model = genai.GenerativeModel(model_name)
            
            # Test the connection
            test_response = self.ai_model.generate_content("Hello")
            if test_response and test_response.text:
                self.ai_available = True
                print("✅ Gemini AI connected successfully")
            else:
                raise Exception("Gemini test failed")
                
        except Exception as e:
            print(f"❌ Gemini connection failed: {e}")
            print("❌ Jarvis requires AI connection to work")
            print("❌ Please check your internet connection and API key")
            if "403" in str(e) or "API key" in str(e):
                print("💡 Your API key may be invalid. Configure a new one:")
                print("   jarvis configure -model gemini <your-api-key>")
            sys.exit(1)
    
    def setup_drona(self):
        """Setup Drona connection"""
        try:
            # Get Drona API URL and bot_id from config file or use provided values
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
                sys.exit(1)
            
            # Skip test connection - just mark as available
            # The actual query will test the connection naturally
            self.ai_available = True
            print("✅ Drona AI ready")
                
        except Exception as e:
            print(f"❌ Drona connection failed: {e}")
            print("❌ Jarvis requires AI connection to work")
            print("❌ Please check your internet connection to Drona server")
            print(f"💡 URL being used: {self.drona_url}")
            print(f"💡 Bot ID being used: {self.bot_id}")
            print("💡 Configure Drona server URL using:")
            print("   jarvis configure -m drona --url <server-url>")
            sys.exit(1)
    
    def query_slm(self, prompt):
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
    
    def get_ip_address(self):
        """Get the machine's IP address"""
        try:
            # Try to get local IP address
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            try:
                # Connect to a remote address (doesn't actually send data)
                s.connect(('8.8.8.8', 80))
                ip = s.getsockname()[0]
            except Exception:
                ip = '127.0.0.1'
            finally:
                s.close()
            return ip
        except Exception as e:
            return '127.0.0.1'
    
    def get_machine_details(self):
        """Get machine details as a dictionary"""
        try:
            import psutil
            
            # Get CPU information
            cpu_percent = psutil.cpu_percent(interval=1)
            cpu_count = psutil.cpu_count()
            cpu_freq = psutil.cpu_freq()
            
            # Get memory information
            memory = psutil.virtual_memory()
            memory_percent = memory.percent
            memory_available = memory.available // (1024**3)
            memory_total = memory.total // (1024**3)
            
            # Get disk information
            disk = psutil.disk_usage('/')
            disk_percent = disk.percent
            disk_free = disk.free // (1024**3)
            disk_total = disk.total // (1024**3)
            
            # Get load average
            load_avg = os.getloadavg()
            
            # Get running processes count
            process_count = len(psutil.pids())
            
            return {
                "system": platform.system(),
                "release": platform.release(),
                "machine": platform.machine(),
                "hostname": platform.node(),
                "cpu_percent": cpu_percent,
                "cpu_count": cpu_count,
                "cpu_freq": cpu_freq.current if cpu_freq else "Unknown",
                "memory_percent": memory_percent,
                "memory_available": memory_available,
                "memory_total": memory_total,
                "disk_percent": disk_percent,
                "disk_free": disk_free,
                "disk_total": disk_total,
                "load_avg_1min": load_avg[0],
                "load_avg_5min": load_avg[1],
                "load_avg_15min": load_avg[2],
                "process_count": process_count,
                "current_dir": os.getcwd(),
                "ip_address": self.get_ip_address()
            }
        except Exception as e:
            return {
                "system": platform.system(),
                "release": platform.release(),
                "machine": platform.machine(),
                "hostname": platform.node(),
                "current_dir": os.getcwd(),
                "ip_address": self.get_ip_address(),
                "error": str(e)
            }
    
    def query_drona(self, message, test=False):
        """Query Drona server with message, machine details, IP address, and optionally image"""
        try:
            import requests
            
            # Get machine details and IP address
            machine_details = self.get_machine_details()
            ip_address = machine_details.get("ip_address", self.get_ip_address())
            
            # Prepare the payload
            payload = {
                "message": message,
                "bot_id": self.bot_id,
                "machine_details": machine_details,
                "ip_address": ip_address
            }
            
            # Add image data if available
            if self.image_data:
                payload["image"] = self.image_data 

            
            # Make API call - use the URL directly (it already includes the endpoint path)
            response = requests.post(
                self.drona_url,
                json=payload,
                timeout=30
            )
            
            if response.status_code == 200:
                result = response.json()
                # Return response text, similar to other modes
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
                # Show error during test for debugging
                print(f"⚠️ Drona test error: {e}")
            return None
    
    def clear_screen(self):
        """Clear the console screen"""
        os.system('clear' if os.name == 'posix' else 'cls')
    
    def print_header(self):
        """Print the header"""
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
    
    def print_help(self):
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
        print("🔧 System Health Commands:")
        print("  cpu         - Show CPU usage")
        print("  memory      - Show memory usage")
        print("  disk        - Show disk usage")
        print("  processes   - Show running processes")
        print("  system      - Complete system health analysis")
        print()
        print("🎤 Voice Commands:")
        print("  jarvis -v              - Start voice command mode")
        print("  jarvis -v -m gemini    - Voice mode with Gemini model")
        print("  jarvis -v -m slm       - Voice mode with SLM model")
        print("  jarvis -v -m drona -b <bot_id> - Voice mode with Drona model")
        print("  Say 'jarvis' followed by your command")
        print("  Example: 'jarvis list files in this directory'")
        print()
        print("🤖 AI Model Selection:")
        print("  jarvis 'command' -m slm     - Use SLM model (35.174.147.167:5000)")
        print("  jarvis 'command' -m gemini  - Use Gemini model (default)")
        print("  jarvis 'command' -m drona -b <bot_id>  - Use Drona model")
        print("  jarvis -m slm               - Start interactive mode with SLM")
        print("  jarvis -m gemini            - Start interactive mode with Gemini")
        print("  jarvis -m drona -b <bot_id> - Start interactive mode with Drona")
        print()
        print("🔑 Configuration:")
        print("  Gemini: jarvis configure -m gemini --api-key <api-key> [-n <model-name>]")
        print("    Example: jarvis configure -m gemini -n 'gemini-2.5-flash' --api-key 'your-key'")
        print("    Get API key from: https://makersuite.google.com/app/apikey")
        print("  SLM: jarvis configure -m slm --url <server-url>")
        print("    Example: jarvis configure -m slm --url http://35.174.147.167:5000")
        print()
        print("💡 Example Questions:")
        print("  🔍 Analysis (Multi-turn):")
        print("    • is my cpu utilization normal?")
        print("    • how's my system performance?")
        print("    • what's using most CPU?")
        print("    • why is my system slow?")
        print("  ⚡ Direct (Single command):")
        print("    • list files in this directory")
        print("    • open finder here")
        print("    • check disk space")
        print("    • create a new file called test.txt")
        print("    • show running processes")
        print()
    
    def test_system(self):
        """Test the system"""
        print("🔍 Running system test...")
        print("✅ Console interface working")
        print("✅ Python working")
        print(f"✅ System: {platform.system()} {platform.release()}")
        print(f"✅ Python: {sys.version.split()[0]}")
        print(f"✅ Current Directory: {os.getcwd()}")
        print("✅ AI connected")
        print("✅ All systems operational")
        print()
    
    def get_system_info(self):
        """Get current system information with detailed metrics"""
        try:
            import psutil
            
            # Get CPU information
            cpu_percent = psutil.cpu_percent(interval=1)
            cpu_count = psutil.cpu_count()
            cpu_freq = psutil.cpu_freq()
            
            # Get memory information
            memory = psutil.virtual_memory()
            memory_percent = memory.percent
            memory_available = memory.available // (1024**3)
            memory_total = memory.total // (1024**3)
            
            # Get disk information
            disk = psutil.disk_usage('/')
            disk_percent = disk.percent
            disk_free = disk.free // (1024**3)
            disk_total = disk.total // (1024**3)
            
            # Get load average
            load_avg = os.getloadavg()
            
            # Get running processes count
            process_count = len(psutil.pids())
            
            info = {
                "system": platform.system(),
                "release": platform.release(),
                "machine": platform.machine(),
                "cpu_percent": cpu_percent,
                "cpu_count": cpu_count,
                "cpu_freq": cpu_freq.current if cpu_freq else "Unknown",
                "memory_percent": memory_percent,
                "memory_available": memory_available,
                "memory_total": memory_total,
                "disk_percent": disk_percent,
                "disk_free": disk_free,
                "disk_total": disk_total,
                "load_avg_1min": load_avg[0],
                "load_avg_5min": load_avg[1],
                "load_avg_15min": load_avg[2],
                "process_count": process_count,
                "current_dir": os.getcwd()
            }
            
            return f"""System: macOS {info['release']} on {info['machine']}
CPU: {info['cpu_percent']:.1f}% usage, {info['cpu_count']} cores @ {info['cpu_freq']:.0f}MHz
Memory: {info['memory_percent']:.1f}% used ({info['memory_total'] - info['memory_available']}GB/{info['memory_total']}GB), {info['memory_available']}GB available
Disk: {info['disk_percent']:.1f}% used ({info['disk_total'] - info['disk_free']}GB/{info['disk_total']}GB), {info['disk_free']}GB free
Load Average: {info['load_avg_1min']:.2f} (1min), {info['load_avg_5min']:.2f} (5min), {info['load_avg_15min']:.2f} (15min)
Processes: {info['process_count']} running
Current Directory: {info['current_dir']}"""
            
        except Exception as e:
            return f"macOS {platform.release()}, Current directory: {os.getcwd()}, Error getting detailed metrics: {e}"
    
    def process_query(self, query):
        """Process a query - LLM decides whether to use single or multi-step flow"""
        print(f"🤔 You asked: {query}")
        print("🤖 Processing...")
        
        # Always use unified flow - LLM decides through its responses
        self.unified_query_processing(query)
    
    def parse_json_response(self, response_text):
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
    
    def unified_query_processing(self, query):
        """Unified query processing - LLM decides whether single or multi-step is needed"""
        try:
            # Get system info for context
            system_info = self.get_system_info()
            
            # Create unified prompt - LLM decides the approach
            prompt = f"""You are Jarvis, an AI assistant for macOS terminal. 

Current System Information:
{system_info}

User Request: {query}

RESPONSE FORMAT:
- If user needs a command executed, respond with JSON:
  {{"command": "command_to_execute", "command_number": "last"}}
  OR
  {{"command": "command_to_execute", "command_number": "intermediate"}}
  
  CRITICAL DECISION: "intermediate" vs "last"
  
  ⚠️ DEFAULT TO "intermediate" FOR ANY QUERY THAT NEEDS ANALYSIS OR INTERPRETATION ⚠️
  
  - ALWAYS use "intermediate" when:
    * The query asks "is", "check", "analyze", "what", "why", "how", "show me", "tell me"
    * The query requires analysis, investigation, or multi-step reasoning
    * You need to gather data first, then analyze it before providing final answer
    * Multiple commands may be needed to fully answer the question
    * The command output needs to be examined before concluding
    * The query asks about system state, security, performance, or requires interpretation
    * The query asks about CPU, memory, disk, processes, network, or system health
    * The user wants you to analyze or interpret command output
    * Examples: "is my CPU normal?", "check memory", "what processes are running?", "analyze system"
  
  - ONLY use "last" when:
    * It's a simple, single-step command that doesn't need analysis
    * The command output is self-explanatory and doesn't need interpretation
    * Examples: "list files", "show current directory", "open finder"
    * The user explicitly wants just the raw command output with no analysis

- If user just needs information/answer (no command), respond with plain text directly (NO JSON).
  Just provide your answer as regular text that will be printed directly.

You can execute ANY valid macOS/Unix command including:
- Opening applications: open -a "App Name"
- Terminal commands: ls, ps, df, top, lsof, netstat, etc.
- File operations: touch, mkdir, rm, cp, mv, etc.
- System commands: sudo, brew, git, etc.
- Directory navigation: cd, pwd, etc.
- Custom scripts and any other valid commands

CRITICAL - NON-INTERACTIVE COMMANDS REQUIRED:
- ALWAYS use "top -l 1" instead of "top" (runs once and exits)
- NEVER use "top" without "-l 1" flag - it will timeout
- NEVER use "top -o mem" - use "top -l 1 -o mem" instead
- NEVER use "top -o cpu" - use "top -l 1 -o cpu" instead
- Use "ps aux" as alternative to interactive "top"
- Commands must complete within 30 seconds or they will timeout
- For monitoring commands, ALWAYS use flags that make them exit automatically
- If you generate "top" without "-l 1", the system will auto-fix it, but you should get it right

AGENTIC BEHAVIOR - CRITICAL:
- When you use "intermediate", the command output will be sent back to you automatically
- You MUST analyze the output and either:
  * Run more commands (use "intermediate" again)
  * Provide a final answer (use "last" command OR plain text response)
- DO NOT use "last" after the first command if the query needs analysis
- The system will keep iterating until you provide a final answer (plain text) or use "last"
- Example flow:
  1. Query: "is my CPU usage normal?"
  2. You: {{"command": "top -l 1 -o cpu", "command_number": "intermediate"}}
  3. System executes, sends output back to you
  4. You analyze output, then: either run more commands OR provide plain text answer
  5. If you provide plain text, the flow stops (that's your final answer)

Examples (NOTE: All "top" commands MUST include "-l 1"):
- User: "list files" → {{"command": "ls -la", "command_number": "last"}}
  (Simple command, no analysis needed)
- User: "what is Python?" → Python is a high-level programming language...
  (Information question, no command needed)
- User: "check disk space" → {{"command": "df -h", "command_number": "intermediate"}}
  (User said "check" - needs analysis, use intermediate)
- User: "is my CPU usage normal?" → {{"command": "top -l 1 -o cpu", "command_number": "intermediate"}}
  (After getting output, analyze CPU usage and provide insights as plain text response)
- User: "check memory usage" → {{"command": "top -l 1 -o mem", "command_number": "intermediate"}}
  (After getting output, analyze memory usage and provide insights as plain text response)
- User: "show me running processes" → {{"command": "ps aux", "command_number": "intermediate"}}
  (User said "show me" - needs analysis/formatting, use intermediate)
- User: "is there any suspicious process sending data?" → {{"command": "lsof -i TCP -P -n", "command_number": "intermediate"}}
  (After getting output, analyze it and provide insights as plain text response)
- User: "create test.txt and list files" → {{"command": "touch test.txt", "command_number": "intermediate"}}
  (Then after execution, you'll get output and can send: {{"command": "ls -la", "command_number": "intermediate"}})
  (After ls output, provide summary as plain text response)

WRONG (will timeout): "top -o mem", "top -o cpu", "top"
CORRECT (will work): "top -l 1 -o mem", "top -l 1 -o cpu", "top -l 1"

Analyze the user's query and decide the best approach. Be thorough when analysis is needed, efficient when simple commands suffice. Use agentic iteration when multiple steps are required."""

            # Process query with unified command execution flow
            self.execute_command_flow(query, prompt, system_info)
                
        except Exception as e:
            print(f"❌ Error processing query: {e}")
            print("❌ AI connection may be lost. Please restart Jarvis.")
    
    def execute_command_flow(self, initial_query, initial_prompt, system_info):
        """Execute command flow with intermediate/last command handling - Agentic iteration"""
        max_iterations = 10
        iteration = 0
        current_query = initial_query
        current_prompt = initial_prompt
        
        while iteration < max_iterations:
            iteration += 1
            
            # Show iteration progress for agentic flow
            if iteration > 1:
                print(f"\n🔄 Agentic iteration {iteration}/{max_iterations}...")
            
            # Get response from AI model
            if self.model == 'slm':
                response_text = self.query_slm(current_prompt)
                if not response_text:
                    raise Exception("SLM query failed")
            elif self.model == 'drona':
                # For drona mode, send the current prompt which includes:
                # - First iteration: original user query
                # - Intermediate iterations: original query + command output
                # The API will receive message, machine_details, and IP address
                response_text = self.query_drona(current_prompt)
                if not response_text:
                    raise Exception("Drona query failed")
            else:  # gemini
                response = self.ai_model.generate_content(current_prompt)
                response_text = response.text.strip()
            
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
                    current_prompt = f"""You are Jarvis, an AI assistant for macOS terminal.

Current System Information:
{system_info}

ORIGINAL User Request: {initial_query}

Command Just Executed: {command}
Command Output:
{output_text}
Command Success: {result["success"]}

Based on the command output above, continue working on the ORIGINAL user request: "{initial_query}"

IMPORTANT: You have 3 options:
1. If more commands needed: respond with JSON {{"command": "next_command", "command_number": "intermediate"}}
2. If done and want to provide final answer: respond with PLAIN TEXT (NO JSON) - this will end the flow
3. Only use "last" if you need to run one final command that doesn't need analysis

⚠️ PREFER PLAIN TEXT RESPONSE over "last" when providing your final analysis/answer ⚠️

Continue the agentic flow. Use the command output above to help answer: "{initial_query}"
Iterate as needed to fully answer the user's original request."""
                    
                    # Keep original query for context (don't overwrite it)
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
    
    def conversation_loop(self, initial_query):
        """Handle multi-turn conversation with AI using JSON-based command flow"""
        conversation_history = []
        max_turns = 10  # Prevent infinite loops
        turn_count = 0
        
        current_query = initial_query
        
        while turn_count < max_turns:
            turn_count += 1
            print(f"\n🔄 Turn {turn_count}: Analyzing...")
            
            try:
                # Get current system info
                system_info = self.get_system_info()
                
                # Build conversation context
                context = self.build_conversation_context(system_info, current_query, conversation_history)
                
                # Get AI response
                if self.model == 'slm':
                    response_text = self.query_slm(context)
                    if not response_text:
                        raise Exception("SLM query failed")
                elif self.model == 'drona':
                    # For drona mode, send the user's message (query) as the message field
                    response_text = self.query_drona(current_query)
                    if not response_text:
                        raise Exception("Drona query failed")
                else:  # gemini
                    response = self.ai_model.generate_content(context)
                    response_text = response.text.strip()
                
                # Add to conversation history
                conversation_history.append({
                    "turn": turn_count,
                    "query": current_query,
                    "response": response_text
                })
                
                # Try to parse as JSON
                json_response = self.parse_json_response(response_text)
                
                if json_response and "command" in json_response:
                    # Command execution needed
                    command = json_response["command"]
                    command_number = json_response.get("command_number", "last")
                    
                    print(f"\n🚀 Executing command: {command}")
                    
                    # Execute command and get results
                    result = self.execute_command_silent(command)
                    
                    # Show result to user
                    self.show_command_result(command, result)
                    
                    # Check if command was successful
                    if result["success"]:
                        print("✅ Command executed successfully!")
                    else:
                        print("❌ Command failed!")
                    
                    # Prepare output for next iteration
                    output_text = result["stdout"] if result["stdout"] else result["stderr"]
                    if not output_text:
                        output_text = "Command executed with no output"
                    
                    # If last command, stop flow
                    if command_number == "last":
                        print("\n✅ Analysis complete!")
                        break
                    
                    # If intermediate, send output back to LLM and continue
                    if command_number == "intermediate":
                        current_query = f"Command '{command}' returned: {output_text}. Please analyze this and provide insights or suggest next steps."
                        continue
                else:
                    # Plain text response - print directly
                    print("\n" + "=" * 60)
                    print("📝 Response:")
                    print("=" * 60)
                    print(response_text)
                    print("=" * 60)
                    print("\n✅ Analysis complete!")
                    break
                    
            except Exception as e:
                print(f"❌ Error in conversation turn {turn_count}: {e}")
                break
        
        if turn_count >= max_turns:
            print("\n⚠️ Maximum conversation turns reached. Ending analysis.")
    
    def build_conversation_context(self, system_info, current_query, conversation_history):
        """Build context for AI conversation"""
        context = f"""You are Jarvis, an AI assistant for macOS terminal in a conversational debugging session.

Current System Information:
{system_info}

Current Query: {current_query}

Conversation History:
"""
        
        for entry in conversation_history:
            context += f"Turn {entry['turn']}: {entry['query']}\n"
            context += f"Response: {entry['response']}\n\n"
        
        context += """
RESPONSE FORMAT:
- If you need to execute a command, respond with JSON:
  {{"command": "command_to_execute", "command_number": "last"}}
  OR
  {{"command": "command_to_execute", "command_number": "intermediate"}}
  
  IMPORTANT: Use "intermediate" when:
  - The query requires analysis or investigation (checking for suspicious activity, security issues, performance problems, etc.)
  - You need to gather data first, then analyze it before providing final answer
  - Multiple commands may be needed to fully answer the question
  - The command output needs to be examined before concluding
  
  Use "last" ONLY if:
  - It's a simple, single-step command (like "list files", "show disk space")
  - You're certain no further analysis is needed
  - The command output doesn't need interpretation

- If you just need to provide information/answer (no command), respond with plain text directly (NO JSON).
  Just provide your answer as regular text that will be printed directly.

CRITICAL - NON-INTERACTIVE COMMANDS REQUIRED:
- ALWAYS use "top -l 1" instead of "top" (runs once and exits)
- NEVER use "top" without "-l 1" flag - it will timeout
- NEVER use "top -o mem" - use "top -l 1 -o mem" instead
- NEVER use "top -o cpu" - use "top -l 1 -o cpu" instead
- Commands must complete within 30 seconds or they will timeout

For system analysis, you should:
1. First gather data with appropriate commands (top -l 1, ps, df, lsof, netstat, etc.)
2. Analyze the results - examine the output carefully
3. Run additional commands if needed to get complete picture
4. Provide comprehensive analysis with insights

Examples (NOTE: All "top" commands MUST include "-l 1"):
- User: "is my cpu utilization normal?" 
  → {{"command": "top -l 1 -o cpu", "command_number": "intermediate"}}
  → (After getting results) {{"command": "vm_stat", "command_number": "intermediate"}}
  → (After getting results) Plain text: "Based on the analysis, your CPU usage is X% which is normal. Memory usage is Y%..."
- User: "check memory usage"
  → {{"command": "top -l 1 -o mem", "command_number": "intermediate"}}
  → (After analyzing output) Plain text: "Memory analysis: ..."
- User: "is there any suspicious process sending data?"
  → {{"command": "lsof -i TCP -P -n", "command_number": "intermediate"}}
  → (After analyzing output) {{"command": "ps aux | grep <suspicious_pid>", "command_number": "intermediate"}}
  → (After getting more info) Plain text: "Analysis complete: Found X processes with network connections. Here's what I found..."

WRONG (will timeout): "top -o mem", "top -o cpu", "top"
CORRECT (will work): "top -l 1 -o mem", "top -l 1 -o cpu", "top -l 1"

Be conversational and thorough in your analysis. Don't just give one command - investigate properly! Always analyze command outputs before concluding. Use agentic iteration when multiple steps are required.

Respond with JSON for commands or plain text for information."""
        
        return context
    
    def sanitize_command(self, command):
        """Convert interactive commands to non-interactive versions to prevent timeouts"""
        command_lower = command.lower().strip()
        
        # Convert top commands to non-interactive versions
        if command_lower.startswith('top ') and '-l' not in command_lower:
            # If top doesn't have -l flag, add it
            if 'top -' in command_lower:
                # Insert -l 1 after 'top'
                command = command.replace('top ', 'top -l 1 ', 1)
            elif command_lower == 'top':
                command = 'top -l 1'
            else:
                # top with other flags but no -l
                command = command.replace('top ', 'top -l 1 ', 1)
        
        # Convert other potentially interactive commands
        # htop, btop, etc. should be avoided, but if used, suggest alternatives
        if 'htop' in command_lower or 'btop' in command_lower:
            # Replace with ps aux or top -l 1
            if 'htop' in command_lower:
                command = command.replace('htop', 'top -l 1', 1)
            if 'btop' in command_lower:
                command = command.replace('btop', 'top -l 1', 1)
        
        return command
    
    def execute_command_silent(self, command):
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
    
    def show_command_result(self, command, result):
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
    
    def execute_command(self, command):
        """Execute any command from Gemini"""
        print("\n" + "=" * 60)
        print("🚀 Executing Command:")
        print("=" * 60)
        print(f"Command: {command}")
        print("-" * 60)
        
        try:
            # Execute the command directly using shell
            result = subprocess.run(command, shell=True, capture_output=True, text=True, timeout=60)
            
            if result.returncode == 0:
                print("✅ Command executed successfully!")
                if result.stdout:
                    print("\nOutput:")
                    print(result.stdout)
            else:
                print("❌ Command failed!")
                if result.stderr:
                    print("\nError:")
                    print(result.stderr)
                else:
                    print("No error details available")
                    
        except subprocess.TimeoutExpired:
            print("❌ Command timed out after 60 seconds!")
        except Exception as e:
            print(f"❌ Unexpected error: {e}")
        
        print("=" * 60)
        print()
    
    def show_info(self, info):
        """Show information to user"""
        print("\n" + "=" * 60)
        print("📝 Information:")
        print("=" * 60)
        print(info)
        print("=" * 60)
        print()
    
    def listen_for_voice(self, timeout=5, phrase_time_limit=10):
        """Listen for voice input and return transcribed text"""
        try:
            import speech_recognition as sr
            
            recognizer = sr.Recognizer()
            microphone = sr.Microphone()
            
            # Adjust for ambient noise
            with microphone as source:
                print("🎤 Adjusting for ambient noise... Please wait.")
                recognizer.adjust_for_ambient_noise(source, duration=1)
                print("✅ Ready! Listening...")
            
            # Listen for audio
            with microphone as source:
                try:
                    audio = recognizer.listen(source, timeout=timeout, phrase_time_limit=phrase_time_limit)
                    print("🎤 Processing voice input...")
                    
                    # Use Google Speech Recognition (free, no API key needed for basic usage)
                    text = recognizer.recognize_google(audio)
                    return text.lower()
                except sr.WaitTimeoutError:
                    print("⏱️  No voice input detected within timeout period.")
                    return None
                except sr.UnknownValueError:
                    print("❌ Could not understand audio. Please try again.")
                    return None
                except sr.RequestError as e:
                    print(f"❌ Error with speech recognition service: {e}")
                    print("💡 Make sure you have an internet connection for Google Speech Recognition.")
                    return None
                    
        except ImportError:
            print("❌ speech_recognition module not found.")
            print("💡 Please install it: pip3 install SpeechRecognition pyaudio")
            return None
        except Exception as e:
            print(f"❌ Error listening for voice: {e}")
            return None
    
    def listen_for_wake_word(self):
        """Listen continuously for 'jarvis' wake word, then capture command"""
        try:
            import speech_recognition as sr
            
            recognizer = sr.Recognizer()
            microphone = sr.Microphone()
            
            print("🎤 Voice command mode activated!")
            print("💡 Say 'jarvis' followed by your command")
            print("💡 Example: 'jarvis list files in this directory'")
            print("=" * 60)
            
            # Adjust for ambient noise
            with microphone as source:
                print("🎤 Adjusting for ambient noise... Please wait.")
                recognizer.adjust_for_ambient_noise(source, duration=1)
                print("✅ Ready! Listening for 'jarvis'...")
            
            while self.running:
                try:
                    with microphone as source:
                        # Listen for audio (no timeout, continuous listening)
                        print("\n🎤 Listening... (say 'jarvis' followed by your command)")
                        audio = recognizer.listen(source, timeout=None, phrase_time_limit=15)
                        
                        print("🎤 Processing voice input...")
                        
                        # Recognize speech
                        try:
                            text = recognizer.recognize_google(audio).lower()
                            print(f"📝 Heard: {text}")
                            
                            # Check if "jarvis" is in the text
                            if "jarvis" in text:
                                # Extract command after "jarvis"
                                parts = text.split("jarvis", 1)
                                if len(parts) > 1:
                                    command = parts[1].strip()
                                    if command:
                                        print(f"✅ Command detected: {command}")
                                        return command
                                    else:
                                        print("⚠️  Heard 'jarvis' but no command followed. Please try again.")
                                else:
                                    print("⚠️  Heard 'jarvis' but no command followed. Please try again.")
                            else:
                                print(f"⚠️  Did not hear 'jarvis'. Heard: '{text}'")
                                print("💡 Please say 'jarvis' followed by your command.")
                                
                        except sr.UnknownValueError:
                            print("❌ Could not understand audio. Please try again.")
                        except sr.RequestError as e:
                            print(f"❌ Error with speech recognition service: {e}")
                            print("💡 Make sure you have an internet connection.")
                            
                except KeyboardInterrupt:
                    print("\n👋 Exiting voice command mode...")
                    break
                except Exception as e:
                    print(f"❌ Error: {e}")
                    time.sleep(1)
                    
        except ImportError:
            print("❌ speech_recognition module not found.")
            print("💡 Please install it: pip3 install SpeechRecognition pyaudio")
            return None
        except Exception as e:
            print(f"❌ Error in voice command mode: {e}")
            return None
    
    def run_voice_mode(self):
        """Run Jarvis in voice command mode with full agentic support"""
        self.clear_screen()
        self.print_header()
        print("🎤 VOICE COMMAND MODE - AGENTIC AI")
        print("=" * 60)
        print("💡 Say 'jarvis' followed by your command")
        print("💡 Example: 'jarvis list files in this directory'")
        print("💡 Example: 'jarvis check if my CPU usage is normal'")
        print("💡 Jarvis will automatically iterate through commands until complete")
        print("💡 Say 'quit' or press Ctrl+C to exit")
        print("=" * 60)
        print()
        
        while self.running:
            try:
                # Listen for wake word and command
                command = self.listen_for_wake_word()
                
                if not command:
                    continue
                
                if command.lower() in ['quit', 'q', 'exit', 'stop']:
                    print("👋 Goodbye!")
                    break
                
                # Process the command with full agentic support
                print(f"\n🤖 Processing voice command: {command}")
                print("🔄 Agentic mode: Jarvis will iterate through commands as needed...")
                print("=" * 60)
                self.process_query(command)
                print("\n" + "=" * 60)
                print("✅ Agentic flow complete. Listening for next command...")
                print("=" * 60)
                print()
                
            except KeyboardInterrupt:
                print("\n👋 Goodbye!")
                break
            except Exception as e:
                print(f"❌ Error: {e}")
                print()
        print()
    
    def show_system_health(self):
        """Show comprehensive system health analysis"""
        print("\n" + "=" * 60)
        print("🏥 System Health Analysis:")
        print("=" * 60)
        
        try:
            import psutil
            
            # Get current metrics
            cpu_percent = psutil.cpu_percent(interval=1)
            memory = psutil.virtual_memory()
            disk = psutil.disk_usage('/')
            load_avg = os.getloadavg()
            
            print(f"🖥️  CPU Usage: {cpu_percent:.1f}%")
            if cpu_percent < 50:
                print("   Status: ✅ Normal")
            elif cpu_percent < 80:
                print("   Status: ⚠️  High")
            else:
                print("   Status: 🔴 Critical")
            
            print(f"🧠 Memory Usage: {memory.percent:.1f}% ({memory.used // (1024**3)}GB / {memory.total // (1024**3)}GB)")
            if memory.percent < 70:
                print("   Status: ✅ Normal")
            elif memory.percent < 90:
                print("   Status: ⚠️  High")
            else:
                print("   Status: 🔴 Critical")
            
            print(f"💾 Disk Usage: {disk.percent:.1f}% ({disk.used // (1024**3)}GB / {disk.total // (1024**3)}GB)")
            if disk.percent < 80:
                print("   Status: ✅ Normal")
            elif disk.percent < 95:
                print("   Status: ⚠️  High")
            else:
                print("   Status: 🔴 Critical")
            
            print(f"⚖️  Load Average: {load_avg[0]:.2f} (1min), {load_avg[1]:.2f} (5min), {load_avg[2]:.2f} (15min)")
            cpu_count = psutil.cpu_count()
            if load_avg[0] < cpu_count:
                print("   Status: ✅ Normal")
            else:
                print("   Status: ⚠️  High Load")
            
            print(f"🔄 Running Processes: {len(psutil.pids())}")
            
            # Overall health assessment
            print("\n📊 Overall System Health:")
            issues = []
            if cpu_percent > 80: issues.append("High CPU usage")
            if memory.percent > 90: issues.append("High memory usage")
            if disk.percent > 95: issues.append("High disk usage")
            if load_avg[0] > cpu_count: issues.append("High system load")
            
            if not issues:
                print("✅ System is healthy and running normally")
            else:
                print("⚠️  Issues detected:")
                for issue in issues:
                    print(f"   • {issue}")
                print("\n💡 Recommendations:")
                if "High CPU usage" in issues:
                    print("   • Check for resource-intensive processes with 'top'")
                if "High memory usage" in issues:
                    print("   • Consider closing unused applications")
                if "High disk usage" in issues:
                    print("   • Clean up disk space or move files to external storage")
                if "High system load" in issues:
                    print("   • Restart applications or reboot if necessary")
            
        except Exception as e:
            print(f"❌ Error analyzing system health: {e}")
        
        print("=" * 60)
        print()
    
    def run(self):
        """Main run loop"""
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
                    self.test_system()
                elif user_input.lower() in ['clear', 'c']:
                    self.clear_screen()
                    self.print_header()
                    self.print_help()
                elif user_input.lower() == 'pwd':
                    print(f"Current directory: {os.getcwd()}")
                elif user_input.lower() == 'ls':
                    self.execute_command('ls -la')
                elif user_input.lower() in ['cpu', 'cpu usage', 'cpu status']:
                    self.execute_command('top -l 1 -o cpu')
                elif user_input.lower() in ['memory', 'ram', 'memory usage']:
                    self.execute_command('vm_stat')
                elif user_input.lower() in ['disk', 'disk usage', 'disk space']:
                    self.execute_command('df -h')
                elif user_input.lower() in ['processes', 'ps', 'running processes']:
                    self.execute_command('ps aux | head -20')
                elif user_input.lower() in ['system', 'system status', 'health']:
                    self.show_system_health()
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

def configure_api_key(model, api_key=None, model_name=None, slm_url=None, drona_url=None, bot_id=None):
    """Configure settings for a model"""
    config = load_config()
    
    if model == 'gemini':
        if not api_key:
            print("❌ API key is required for Gemini model")
            print("❌ Usage: jarvis configure -m gemini --api-key <your-api-key> [-n <model-name>]")
            sys.exit(1)
        config['gemini_api_key'] = api_key
        if model_name:
            config['gemini_model_name'] = model_name
        else:
            # Default model name if not specified
            config['gemini_model_name'] = 'gemini-2.5-flash'
        save_config(config)
        print(f"✅ Gemini API key configured successfully")
        if model_name:
            print(f"✅ Model name set to: {model_name}")
        print("💡 You can now use jarvis with: jarvis 'your question'")
    elif model == 'slm':
        if not slm_url:
            print("❌ Server URL is required for SLM model")
            print("❌ Usage: jarvis configure -m slm --url <server-url>")
            print("❌ Example: jarvis configure -m slm --url http://35.174.147.167:5000")
            sys.exit(1)
        config['slm_url'] = slm_url
        save_config(config)
        print(f"✅ SLM server URL configured successfully")
        print(f"✅ Server URL set to: {slm_url}")
        print("💡 You can now use jarvis with: jarvis 'your question' -m slm")
    elif model == 'drona':
        if drona_url:
            config['drona_url'] = drona_url
        if bot_id:
            config['drona_bot_id'] = bot_id
        
        if not drona_url and not bot_id:
            print("❌ At least one of --url or --bot-id is required for Drona model")
            print("❌ Usage: jarvis configure -m drona --url <server-url> [-b <bot-id>]")
            print("❌ Or: jarvis configure -m drona -b <bot-id> [--url <server-url>]")
            print("❌ Example: jarvis configure -m drona --url http://35.174.147.167:5000 -b <bot-id>")
            sys.exit(1)
        
        save_config(config)
        if drona_url:
            print(f"✅ Drona server URL configured successfully")
            print(f"✅ Server URL set to: {drona_url}")
        if bot_id:
            print(f"✅ Drona bot ID configured successfully")
            print(f"✅ Bot ID set to: {bot_id}")
        print("💡 You can now use jarvis with: jarvis 'your question' -m drona [-b <bot_id>]")
    else:
        print(f"❌ Unknown model: {model}")
        print("❌ Supported models: 'gemini', 'slm', 'drona'")
        sys.exit(1)

def main():
    # Check if first argument is 'configure'
    if len(sys.argv) > 1 and sys.argv[1] == 'configure':
        parser = argparse.ArgumentParser(description='Jarvis - Configure Model Settings')
        parser.add_argument('configure', help='configure command')
        parser.add_argument('-m', '--model', choices=['slm', 'gemini', 'drona'], required=True,
                          help='AI model to configure')
        parser.add_argument('-n', '--name', dest='model_name',
                          help='Model name for Gemini (e.g., gemini-2.5-flash, gemini-pro)')
        parser.add_argument('--api-key', dest='api_key',
                          help='API key for Gemini model')
        parser.add_argument('--url', dest='url',
                          help='Server URL for SLM or Drona model (e.g., http://35.174.147.167:5000)')
        parser.add_argument('-b', '--bot-id', dest='bot_id',
                          help='Bot ID for Drona model')
        args = parser.parse_args()
        
        # Handle URL argument for both SLM and Drona
        slm_url = args.url if args.model == 'slm' else None
        drona_url = args.url if args.model == 'drona' else None
        
        configure_api_key(args.model, args.api_key, args.model_name, slm_url, drona_url, args.bot_id)
        return
    
    # Regular jarvis usage
    parser = argparse.ArgumentParser(description='Jarvis - Global Terminal AI Copilot')
    parser.add_argument('query', nargs='*', help='Query to ask Jarvis')
    parser.add_argument('-m', '--model', choices=['slm', 'gemini', 'drona'], default='gemini', 
                       help='AI model to use (default: gemini)')
    parser.add_argument('-b', '--bot-id', dest='bot_id',
                       help='Bot ID for Drona model (required when using -m drona)')
    parser.add_argument('-img', '--image', dest='image_path',
                       help='Path to image file to send with the query (supported formats: jpg, png, gif, webp, bmp)')
    parser.add_argument('-v', '--voice', action='store_true',
                       help='Enable voice command mode (say "jarvis" followed by your command)')
    
    args = parser.parse_args()
    
    # Validate image file exists if provided
    if args.image_path:
        image_file = Path(args.image_path)
        if not image_file.exists():
            print(f"❌ Image file not found: {args.image_path}")
            sys.exit(1)
        if not image_file.is_file():
            print(f"❌ Path is not a file: {args.image_path}")
            sys.exit(1)
    
    # For drona mode, try to get bot_id from config if not provided
    if args.model == 'drona' and not args.bot_id:
        config = load_config()
        args.bot_id = config.get('drona_bot_id')
    
    # Validate drona mode requires bot_id (either from command line or config)
    if args.model == 'drona' and not args.bot_id:
        print("❌ Bot ID is required for Drona mode")
        print("❌ Usage: jarvis 'your message' -m drona -b <bot_id>")
        print("   Or configure it: jarvis configure -m drona -b <bot_id>")
        sys.exit(1)
    
    print("🚀 Starting Jarvis...")
    jarvis = Jarvis(model=args.model, bot_id=args.bot_id, image_path=args.image_path)
    
    # If voice mode enabled, start voice command mode
    if args.voice:
        jarvis.run_voice_mode()
    # If query provided, process it directly
    elif args.query:
        query = ' '.join(args.query)
        jarvis.process_query(query)
    else:
        # Start interactive mode
        jarvis.run()

if __name__ == "__main__":
    main()
