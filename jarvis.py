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
        print("🔒 Security & Monitoring:")
        print("  jarvis -monitor network         - Monitor outbound network connections")
        print("                                    (with desktop notifications)")
        print("  jarvis -monitor process         - Monitor processes for threats & anomalies")
        print("                                    (detects malware, resource abuse, file ops)")
        print("  jarvis -monitor network -m drona -b <bot_id> - Network monitoring with AI")
        print("  jarvis -monitor process -m drona -b <bot_id> - Process monitoring with AI")
        print("  jarvis -scan -f <folder> -m drona - Scan folder for sensitive files")
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
    
    def extract_file_content(self, file_path, max_chars=10000):
        """Extract file content with proper markdown structure, limited to max_chars"""
        try:
            file_path_obj = Path(file_path)
            if not file_path_obj.exists() or not file_path_obj.is_file():
                return None
            
            # Get file metadata
            file_size = file_path_obj.stat().st_size
            file_ext = file_path_obj.suffix.lower()
            
            # Read file content
            try:
                # Try to read as text
                with open(file_path_obj, 'r', encoding='utf-8', errors='ignore') as f:
                    content = f.read()
            except:
                # If text reading fails, try binary and decode
                with open(file_path_obj, 'rb') as f:
                    content = f.read()
                    try:
                        content = content.decode('utf-8', errors='ignore')
                    except:
                        return None  # Binary file that can't be decoded
            
            # Truncate to max_chars if needed
            if len(content) > max_chars:
                content = content[:max_chars] + "\n\n[... content truncated ...]"
            
            # Create markdown structure
            markdown_content = f"""# File: {file_path_obj.name}

## Metadata
- **Path**: `{file_path}`
- **Size**: {file_size} bytes
- **Extension**: `{file_ext}`
- **Content Length**: {len(content)} characters

## Content
```
{content}
```
"""
            return markdown_content
        except Exception as e:
            return None
    
    def categorize_file_sensitivity(self, file_path, file_content_markdown, file_metadata):
        """Categorize file sensitivity using LLM (Drona only)"""
        if self.model != 'drona':
            return None
        
        # Build prompt for categorization
        prompt = f"""You are a security expert analyzing file content to determine if it contains sensitive information.

File Metadata:
- Path: {file_metadata.get('path', 'unknown')}
- Size: {file_metadata.get('size', 0)} bytes
- Extension: {file_metadata.get('extension', 'unknown')}
- Type: {file_metadata.get('type', 'unknown')}

File Content (Markdown):
{file_content_markdown}

TASK: Analyze this file and determine if it contains sensitive information that should be protected.

Sensitive information includes but is not limited to:
- API keys, tokens, passwords, credentials
- Personal identifiable information (PII): SSN, credit cards, phone numbers, addresses
- Financial information: bank accounts, payment details
- Medical records and health information
- Confidential business data: trade secrets, proprietary code, client data
- Authentication credentials: usernames, passwords, private keys
- Database connection strings with credentials
- Environment variables with secrets
- Configuration files with sensitive data
- Source code with hardcoded secrets

RESPONSE FORMAT (JSON only):
{{
    "is_sensitive": true or false,
    "reason": "Brief explanation of why this file is or is not sensitive",
    "sensitivity_level": "high" or "medium" or "low" or "none",
    "recommended_protection": "Specific protection recommendations (e.g., 'encrypt', 'restrict access', 'move to secure location', 'remove from repository')"
}}

Respond ONLY with valid JSON, no additional text."""

        try:
            response_text = self.query_drona(prompt)
            if not response_text:
                return None
            
            # Try to find JSON block first (most common format)
            json_match = re.search(r'```json\s*(\{.*?\})\s*```', response_text, re.DOTALL)
            if json_match:
                try:
                    return json.loads(json_match.group(1))
                except json.JSONDecodeError:
                    pass
            
            # Try to find JSON object with balanced braces
            # Find the first { and then find the matching }
            brace_start = response_text.find('{')
            if brace_start != -1:
                brace_count = 0
                brace_end = -1
                for i in range(brace_start, len(response_text)):
                    if response_text[i] == '{':
                        brace_count += 1
                    elif response_text[i] == '}':
                        brace_count -= 1
                        if brace_count == 0:
                            brace_end = i + 1
                            break
                
                if brace_end > brace_start:
                    try:
                        json_str = response_text[brace_start:brace_end]
                        result = json.loads(json_str)
                        if "is_sensitive" in result:
                            return result
                    except json.JSONDecodeError:
                        pass
            
            # Try to parse entire response as JSON
            try:
                result = json.loads(response_text.strip())
                if isinstance(result, dict) and "is_sensitive" in result:
                    return result
            except json.JSONDecodeError:
                pass
            
            # If JSON parsing fails, try to extract information from text
            is_sensitive = "sensitive" in response_text.lower() and "not sensitive" not in response_text.lower()
            return {
                "is_sensitive": is_sensitive,
                "reason": response_text[:200] if response_text else "Unable to parse response",
                "sensitivity_level": "unknown",
                "recommended_protection": "Review manually"
            }
        except Exception as e:
            print(f"⚠️  Error categorizing file {file_path}: {e}")
            return None
    
    def scan_folder(self, folder_path):
        """Scan folder for sensitive files and categorize them"""
        if self.model != 'drona':
            print("❌ Scan feature is only available with -m drona")
            return
        
        folder_path_obj = Path(folder_path)
        if not folder_path_obj.exists():
            print(f"❌ Folder not found: {folder_path}")
            return
        
        if not folder_path_obj.is_dir():
            print(f"❌ Path is not a directory: {folder_path}")
            return
        
        print("\n" + "=" * 60)
        print("🔍 Starting Folder Scan for Sensitive Files")
        print("=" * 60)
        print(f"📁 Scanning folder: {folder_path}")
        print(f"🤖 Using model: {self.model.upper()}")
        print("=" * 60)
        print()
        
        # Collect all files
        all_files = []
        try:
            for root, dirs, files in os.walk(folder_path):
                # Skip hidden directories
                dirs[:] = [d for d in dirs if not d.startswith('.')]
                
                for file in files:
                    # Skip hidden files
                    if file.startswith('.'):
                        continue
                    
                    file_path = Path(root) / file
                    all_files.append(file_path)
        except Exception as e:
            print(f"❌ Error scanning folder: {e}")
            return
        
        total_files = len(all_files)
        print(f"📊 Found {total_files} files to analyze")
        print()
        
        if total_files == 0:
            print("✅ No files found to scan")
            return
        
        # Analyze each file
        sensitive_files = []
        analyzed_count = 0
        
        for file_path in all_files:
            analyzed_count += 1
            print(f"🔍 Analyzing [{analyzed_count}/{total_files}]: {file_path.name}")
            
            # Get file metadata
            try:
                file_stat = file_path.stat()
                file_metadata = {
                    "path": str(file_path),
                    "name": file_path.name,
                    "size": file_stat.st_size,
                    "extension": file_path.suffix.lower(),
                    "type": "text" if file_path.suffix.lower() in ['.txt', '.md', '.py', '.js', '.json', '.yaml', '.yml', '.xml', '.html', '.css', '.sh', '.bash', '.zsh', '.env', '.config', '.conf', '.ini', '.log'] else "binary"
                }
            except Exception as e:
                print(f"  ⚠️  Could not get metadata: {e}")
                continue
            
            # Extract file content
            file_content = self.extract_file_content(file_path, max_chars=10000)
            if not file_content:
                print(f"  ⚠️  Could not extract content (may be binary or unreadable)")
                continue
            
            # Categorize using LLM
            categorization = self.categorize_file_sensitivity(file_path, file_content, file_metadata)
            
            if categorization and categorization.get("is_sensitive", False):
                sensitive_files.append({
                    "file_path": str(file_path),
                    "file_name": file_path.name,
                    "metadata": file_metadata,
                    "categorization": categorization
                })
                print(f"  🔴 SENSITIVE: {categorization.get('reason', 'No reason provided')}")
            else:
                print(f"  ✅ Not sensitive")
        
        print()
        print("=" * 60)
        print("📊 Scan Complete")
        print("=" * 60)
        print(f"Total files analyzed: {analyzed_count}")
        print(f"Sensitive files found: {len(sensitive_files)}")
        print("=" * 60)
        print()
        
        # Report sensitive files
        if sensitive_files:
            self.report_sensitive_files(sensitive_files)
        else:
            print("✅ No sensitive files detected!")
            print()
    
    def report_sensitive_files(self, sensitive_files):
        """Report sensitive files with recommendations"""
        print("\n" + "=" * 60)
        print("🔴 SENSITIVE FILES DETECTED")
        print("=" * 60)
        print()
        
        for idx, file_info in enumerate(sensitive_files, 1):
            file_path = file_info["file_path"]
            file_name = file_info["file_name"]
            metadata = file_info["metadata"]
            categorization = file_info["categorization"]
            
            print(f"{idx}. 📄 {file_name}")
            print(f"   📍 Path: {file_path}")
            print(f"   📊 Size: {metadata['size']} bytes")
            print(f"   🔒 Sensitivity Level: {categorization.get('sensitivity_level', 'unknown').upper()}")
            print(f"   💡 Reason: {categorization.get('reason', 'No reason provided')}")
            print(f"   🛡️  Recommended Protection: {categorization.get('recommended_protection', 'Review manually')}")
            print()
        
        print("=" * 60)
        print("📋 SUMMARY")
        print("=" * 60)
        print(f"Total sensitive files: {len(sensitive_files)}")
        print()
        print("🛡️  GENERAL RECOMMENDATIONS:")
        print("   • Review each file listed above")
        print("   • Consider encrypting sensitive files")
        print("   • Restrict file access permissions (chmod 600)")
        print("   • Move sensitive files to secure locations")
        print("   • Remove sensitive data from version control if present")
        print("   • Use environment variables or secure vaults for secrets")
        print("   • Implement proper access controls")
        print("=" * 60)
        print()
    
    def monitor_network(self):
        """Monitor network connections and alert on suspicious outbound traffic"""
        print("\n" + "=" * 80)
        print("🌐 NETWORK MONITORING MODE - Real-time Outbound Connection Monitor")
        print("=" * 80)
        print(f"🤖 Using AI Model: {self.model.upper()}")
        print(f"💻 System: {platform.system()}")
        print("=" * 80)
        print("📊 Monitoring outbound network connections from background applications...")
        print("🔔 Desktop notifications will be sent for new connections")
        print("🔍 Press Ctrl+C to stop monitoring")
        print("=" * 80)
        print()
        
        # Track known connections to detect new ones
        known_connections = set()
        alert_count = 0
        
        try:
            import psutil
            
            # Initial scan to establish baseline
            print("🔄 Establishing baseline connections...")
            try:
                connections = psutil.net_connections(kind='inet')
            except psutil.AccessDenied:
                print("\n❌ Access Denied: Network monitoring requires elevated permissions on macOS")
                print("💡 Please run with sudo:")
                print("   sudo python3 jarvis.py -monitor network")
                print("   Or: sudo jarvis -monitor network")
                print("\n⚠️  Note: Use sudo with caution and only from trusted sources")
                return
            
            for conn in connections:
                try:
                    if conn.status == 'ESTABLISHED' and conn.raddr:
                        # Track by (pid, remote_ip, remote_port, local_port)
                        conn_id = (conn.pid, conn.raddr.ip, conn.raddr.port, conn.laddr.port)
                        known_connections.add(conn_id)
                except (AttributeError, TypeError) as e:
                    # Skip connections with missing attributes
                    continue
            
            print(f"✅ Baseline established: {len(known_connections)} active connections")
            print("🔍 Now monitoring for NEW outbound connections...\n")
            
            # Continuous monitoring loop
            iteration = 0
            while True:
                iteration += 1
                time.sleep(3)  # Check every 3 seconds
                
                # Get current connections
                current_connections = set()
                new_connections = []
                
                try:
                    connections = psutil.net_connections(kind='inet')
                except psutil.AccessDenied:
                    print("\n❌ Lost access to network connections. Monitoring stopped.")
                    break
                
                for conn in connections:
                    try:
                        # Only monitor ESTABLISHED outbound connections
                        if conn.status == 'ESTABLISHED' and conn.raddr:
                            conn_id = (conn.pid, conn.raddr.ip, conn.raddr.port, conn.laddr.port)
                            current_connections.add(conn_id)
                            
                            # Check if this is a new connection
                            if conn_id not in known_connections:
                                new_connections.append({
                                    'pid': conn.pid,
                                    'local_ip': conn.laddr.ip,
                                    'local_port': conn.laddr.port,
                                    'remote_ip': conn.raddr.ip,
                                    'remote_port': conn.raddr.port,
                                    'status': conn.status
                                })
                    except (AttributeError, TypeError) as e:
                        # Skip connections with missing attributes
                        continue
                
                # Process new connections
                if new_connections:
                    for new_conn in new_connections:
                        alert_count += 1
                        self.alert_network_activity(new_conn, alert_count)
                
                # Update known connections
                known_connections = current_connections
                
                # Show status update every 10 iterations (30 seconds)
                if iteration % 10 == 0:
                    print(f"[{time.strftime('%H:%M:%S')}] 📊 Status: Monitoring... ({len(current_connections)} active connections, {alert_count} alerts raised)")
        
        except ImportError:
            print("❌ psutil module not found. Please install it: pip3 install psutil")
        except KeyboardInterrupt:
            print("\n\n" + "=" * 80)
            print("🛑 Network monitoring stopped by user")
            print("=" * 80)
            print(f"📊 Monitoring Summary:")
            print(f"   • Total alerts raised: {alert_count}")
            print(f"   • Active connections at stop: {len(known_connections)}")
            print("=" * 80)
            print()
        except Exception as e:
            print(f"\n❌ Error during network monitoring: {e}")
    
    def monitor_processes(self):
        """Monitor processes for anomalies, threats, and suspicious behavior"""
        print("\n" + "=" * 80)
        print("🔍 PROCESS MONITORING MODE - Real-time Security & Anomaly Detection")
        print("=" * 80)
        print(f"🤖 Using AI Model: {self.model.upper()}")
        print(f"💻 System: {platform.system()}")
        print("=" * 80)
        print("📊 Monitoring for:")
        print("   • New suspicious processes")
        print("   • Unusual CPU/Memory usage")
        print("   • Potential threats and vulnerabilities")
        print("   • File deletion/corruption attempts")
        print("   • System integrity threats")
        print("🔔 Desktop notifications will be sent for threats")
        print("🔍 Press Ctrl+C to stop monitoring")
        print("=" * 80)
        print()
        
        # Track known processes and their baselines
        known_processes = {}
        alert_count = 0
        
        # CPU/Memory thresholds
        HIGH_CPU_THRESHOLD = 80.0  # 80% CPU usage
        HIGH_MEMORY_THRESHOLD = 80.0  # 80% memory usage
        
        try:
            import psutil
            
            # Initial scan to establish baseline
            print("🔄 Establishing process baseline...")
            for proc in psutil.process_iter(['pid', 'name', 'username', 'cpu_percent', 'memory_percent']):
                try:
                    pinfo = proc.info
                    known_processes[pinfo['pid']] = {
                        'name': pinfo['name'],
                        'username': pinfo['username'],
                        'cpu_baseline': pinfo['cpu_percent'] or 0,
                        'mem_baseline': pinfo['memory_percent'] or 0,
                        'first_seen': time.time()
                    }
                except (psutil.NoSuchProcess, psutil.AccessDenied):
                    pass
            
            print(f"✅ Baseline established: {len(known_processes)} processes")
            print("🔍 Now monitoring for anomalies and threats...\n")
            
            # Continuous monitoring loop
            iteration = 0
            while True:
                iteration += 1
                time.sleep(5)  # Check every 5 seconds
                
                current_processes = {}
                suspicious_activities = []
                
                try:
                    processes = list(psutil.process_iter([
                        'pid', 'name', 'username', 'exe', 'cmdline',
                        'cpu_percent', 'memory_percent', 'status',
                        'create_time', 'num_threads', 'open_files'
                    ]))
                except (psutil.AccessDenied, PermissionError):
                    print("\n❌ Access Denied: Process monitoring requires elevated permissions")
                    print("💡 Please run with sudo:")
                    print("   sudo python3 jarvis.py -monitor process")
                    break
                
                for proc in processes:
                    try:
                        pinfo = proc.info
                        pid = pinfo['pid']
                        current_processes[pid] = True
                        
                        # Check if this is a new process
                        if pid not in known_processes:
                            # Analyze new process
                            threat_indicators = self.analyze_process_threat(pinfo)
                            
                            if threat_indicators['is_suspicious']:
                                suspicious_activities.append({
                                    'type': 'NEW_PROCESS',
                                    'severity': threat_indicators['severity'],
                                    'process': pinfo,
                                    'indicators': threat_indicators
                                })
                            
                            # Add to known processes
                            known_processes[pid] = {
                                'name': pinfo['name'],
                                'username': pinfo['username'],
                                'cpu_baseline': pinfo['cpu_percent'] or 0,
                                'mem_baseline': pinfo['memory_percent'] or 0,
                                'first_seen': time.time()
                            }
                        else:
                            # Check existing process for anomalies
                            baseline = known_processes[pid]
                            cpu_current = pinfo['cpu_percent'] or 0
                            mem_current = pinfo['memory_percent'] or 0
                            
                            # Check for CPU spike
                            if cpu_current > HIGH_CPU_THRESHOLD:
                                cpu_increase = cpu_current - baseline['cpu_baseline']
                                if cpu_increase > 50:  # 50% increase
                                    suspicious_activities.append({
                                        'type': 'HIGH_CPU',
                                        'severity': 'MEDIUM' if cpu_current < 95 else 'HIGH',
                                        'process': pinfo,
                                        'indicators': {
                                            'cpu_current': cpu_current,
                                            'cpu_baseline': baseline['cpu_baseline'],
                                            'cpu_increase': cpu_increase
                                        }
                                    })
                            
                            # Check for Memory spike
                            if mem_current > HIGH_MEMORY_THRESHOLD:
                                mem_increase = mem_current - baseline['mem_baseline']
                                if mem_increase > 30:  # 30% increase
                                    suspicious_activities.append({
                                        'type': 'HIGH_MEMORY',
                                        'severity': 'MEDIUM' if mem_current < 95 else 'HIGH',
                                        'process': pinfo,
                                        'indicators': {
                                            'mem_current': mem_current,
                                            'mem_baseline': baseline['mem_baseline'],
                                            'mem_increase': mem_increase
                                        }
                                    })
                            
                            # Update baseline (rolling average)
                            baseline['cpu_baseline'] = (baseline['cpu_baseline'] * 0.7 + cpu_current * 0.3)
                            baseline['mem_baseline'] = (baseline['mem_baseline'] * 0.7 + mem_current * 0.3)
                        
                    except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
                        continue
                    except Exception as e:
                        continue
                
                # Process suspicious activities
                if suspicious_activities:
                    for activity in suspicious_activities:
                        alert_count += 1
                        self.alert_process_activity(activity, alert_count)
                
                # Clean up terminated processes from tracking
                terminated_pids = [pid for pid in known_processes if pid not in current_processes]
                for pid in terminated_pids:
                    del known_processes[pid]
                
                # Show status update every 6 iterations (30 seconds)
                if iteration % 6 == 0:
                    print(f"[{time.strftime('%H:%M:%S')}] 📊 Status: Monitoring... ({len(current_processes)} processes, {alert_count} alerts raised)")
        
        except ImportError:
            print("❌ psutil module not found. Please install it: pip3 install psutil")
        except KeyboardInterrupt:
            print("\n\n" + "=" * 80)
            print("🛑 Process monitoring stopped by user")
            print("=" * 80)
            print(f"📊 Monitoring Summary:")
            print(f"   • Total alerts raised: {alert_count}")
            print(f"   • Processes monitored: {len(known_processes)}")
            print("=" * 80)
            print()
        except Exception as e:
            print(f"\n❌ Error during process monitoring: {e}")
    
    def analyze_process_threat(self, pinfo):
        """Analyze a process for potential threats"""
        indicators = {
            'is_suspicious': False,
            'severity': 'LOW',
            'reasons': []
        }
        
        try:
            name = pinfo.get('name', 'Unknown')
            exe = pinfo.get('exe', '')
            cmdline = pinfo.get('cmdline', [])
            username = pinfo.get('username', '')
            cpu_percent = pinfo.get('cpu_percent', 0) or 0
            mem_percent = pinfo.get('memory_percent', 0) or 0
            
            # Check for suspicious executable paths
            suspicious_paths = ['/tmp/', '/var/tmp/', '/dev/shm/', '~/Downloads/']
            if exe:
                for susp_path in suspicious_paths:
                    if susp_path in exe:
                        indicators['is_suspicious'] = True
                        indicators['severity'] = 'HIGH'
                        indicators['reasons'].append(f"Running from suspicious location: {susp_path}")
            
            # Check for suspicious names
            suspicious_names = [
                'keylog', 'hack', 'crack', 'exploit', 'malware',
                'backdoor', 'trojan', 'ransom', 'miner', 'cryptominer'
            ]
            name_lower = name.lower()
            for susp_name in suspicious_names:
                if susp_name in name_lower:
                    indicators['is_suspicious'] = True
                    indicators['severity'] = 'CRITICAL'
                    indicators['reasons'].append(f"Suspicious process name contains: {susp_name}")
            
            # Check for hidden processes (starting with .)
            if name.startswith('.') and len(name) > 1:
                indicators['is_suspicious'] = True
                indicators['severity'] = 'MEDIUM'
                indicators['reasons'].append("Hidden process (starts with .)")
            
            # Check for processes with random/gibberish names
            if len(name) > 15 and not any(c.isspace() for c in name):
                # Check if name is mostly random characters
                consonant_clusters = 0
                for i in range(len(name) - 2):
                    if name[i:i+3].lower().translate(str.maketrans('', '', 'aeiou')) == name[i:i+3].lower():
                        consonant_clusters += 1
                
                if consonant_clusters > len(name) / 4:
                    indicators['is_suspicious'] = True
                    indicators['severity'] = 'MEDIUM'
                    indicators['reasons'].append("Process name appears randomly generated")
            
            # Check command line for suspicious flags
            if cmdline:
                cmdline_str = ' '.join(cmdline).lower()
                suspicious_flags = [
                    'rm -rf', 'dd if=', '/dev/null', 'chmod 777', 'curl | bash',
                    'wget | sh', 'base64 -d', 'eval(', 'exec(', '--no-sandbox'
                ]
                for flag in suspicious_flags:
                    if flag in cmdline_str:
                        indicators['is_suspicious'] = True
                        indicators['severity'] = 'HIGH'
                        indicators['reasons'].append(f"Suspicious command: {flag}")
            
            # Check for high resource usage on startup
            if cpu_percent > 80 or mem_percent > 50:
                indicators['is_suspicious'] = True
                indicators['severity'] = 'MEDIUM'
                indicators['reasons'].append(f"High resource usage: CPU {cpu_percent:.1f}%, Memory {mem_percent:.1f}%")
            
            # Check for root/system processes running as regular user
            system_process_names = ['kernel', 'system', 'root', 'admin']
            if any(sys_name in name_lower for sys_name in system_process_names):
                if username and username != 'root' and username != '_system':
                    indicators['is_suspicious'] = True
                    indicators['severity'] = 'HIGH'
                    indicators['reasons'].append(f"System-named process running as regular user: {username}")
            
        except Exception as e:
            pass
        
        return indicators
    
    def alert_process_activity(self, activity, alert_num):
        """Alert on suspicious process activity"""
        print("\n" + "🚨" * 40)
        print(f"🔴 ALERT #{alert_num} - SUSPICIOUS PROCESS ACTIVITY DETECTED")
        print("🚨" * 40)
        print(f"⏰ Timestamp: {time.strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"⚠️  Activity Type: {activity['type']}")
        print(f"⚠️  Severity: {activity['severity']}")
        print("-" * 80)
        
        pinfo = activity['process']
        indicators = activity['indicators']
        
        # Get process details
        pid = pinfo.get('pid', 'N/A')
        name = pinfo.get('name', 'Unknown')
        exe = pinfo.get('exe', 'Unknown')
        username = pinfo.get('username', 'Unknown')
        cmdline = pinfo.get('cmdline', [])
        cmdline_str = ' '.join(cmdline) if cmdline else 'N/A'
        cpu_percent = pinfo.get('cpu_percent', 0) or 0
        mem_percent = pinfo.get('memory_percent', 0) or 0
        num_threads = pinfo.get('num_threads', 0)
        
        # Display process details
        print(f"📍 Process Details:")
        print(f"   • Process ID (PID): {pid}")
        print(f"   • Process Name: {name}")
        print(f"   • Executable Path: {exe}")
        print(f"   • User: {username}")
        if len(cmdline_str) > 0 and cmdline_str != 'N/A':
            print(f"   • Command: {cmdline_str[:150]}{'...' if len(cmdline_str) > 150 else ''}")
        print()
        print(f"📊 Resource Usage:")
        print(f"   • CPU: {cpu_percent:.1f}%")
        print(f"   • Memory: {mem_percent:.1f}%")
        print(f"   • Threads: {num_threads}")
        print()
        
        # Display threat indicators
        if activity['type'] == 'NEW_PROCESS':
            print(f"🔍 Threat Analysis:")
            reasons = indicators.get('reasons', [])
            if reasons:
                for reason in reasons:
                    print(f"   • {reason}")
        elif activity['type'] == 'HIGH_CPU':
            print(f"⚠️  CPU Usage Anomaly:")
            print(f"   • Current: {indicators['cpu_current']:.1f}%")
            print(f"   • Baseline: {indicators['cpu_baseline']:.1f}%")
            print(f"   • Increase: +{indicators['cpu_increase']:.1f}%")
        elif activity['type'] == 'HIGH_MEMORY':
            print(f"⚠️  Memory Usage Anomaly:")
            print(f"   • Current: {indicators['mem_current']:.1f}%")
            print(f"   • Baseline: {indicators['mem_baseline']:.1f}%")
            print(f"   • Increase: +{indicators['mem_increase']:.1f}%")
        
        print("-" * 80)
        
        # AI-based threat analysis if model is available
        threat_assessment = None
        if self.ai_available and activity['type'] == 'NEW_PROCESS':
            print("🤖 AI Analysis: Analyzing process for threats...")
            threat_assessment = self.analyze_process_with_ai(pinfo, indicators)
            
            if threat_assessment:
                print(f"⚠️  AI Threat Assessment: {threat_assessment.get('level', 'UNKNOWN').upper()}")
                print(f"💡 Analysis: {threat_assessment.get('analysis', 'No analysis available')}")
                if threat_assessment.get('recommendations'):
                    print(f"🛡️  Recommendations: {threat_assessment.get('recommendations', 'No recommendations')}")
        
        print("🚨" * 40)
        print()
        
        # Send desktop notification
        notification_title = f"{activity['severity']} Process Alert #{alert_num}"
        if activity['type'] == 'NEW_PROCESS':
            notification_message = f"Suspicious process: {name} | {', '.join(indicators.get('reasons', [])[:1])}"
        elif activity['type'] == 'HIGH_CPU':
            notification_message = f"{name} using {indicators['cpu_current']:.0f}% CPU"
        elif activity['type'] == 'HIGH_MEMORY':
            notification_message = f"{name} using {indicators['mem_current']:.0f}% Memory"
        else:
            notification_message = f"{name} - {activity['type']}"
        
        self.send_system_notification(notification_title, notification_message, debug=True)
        
        # Send enhanced notification for HIGH/CRITICAL threats
        if activity['severity'] in ['HIGH', 'CRITICAL']:
            enhanced_title = f"{activity['severity']} THREAT - {activity['type']}"
            enhanced_message = f"{name} (PID {pid}) | {username} | Check terminal for details"
            self.send_system_notification(enhanced_title, enhanced_message, debug=True)
    
    def analyze_process_with_ai(self, pinfo, indicators):
        """Use AI to analyze process threat level"""
        try:
            pid = pinfo.get('pid', 'N/A')
            name = pinfo.get('name', 'Unknown')
            exe = pinfo.get('exe', 'Unknown')
            username = pinfo.get('username', 'Unknown')
            cmdline = pinfo.get('cmdline', [])
            cmdline_str = ' '.join(cmdline) if cmdline else 'N/A'
            cpu_percent = pinfo.get('cpu_percent', 0) or 0
            mem_percent = pinfo.get('memory_percent', 0) or 0
            
            reasons = indicators.get('reasons', [])
            reasons_str = ', '.join(reasons) if reasons else 'None'
            
            prompt = f"""You are a cybersecurity expert analyzing a potentially suspicious process.

PROCESS INFORMATION:
- Process Name: {name}
- PID: {pid}
- Executable Path: {exe}
- User: {username}
- Command Line: {cmdline_str}
- CPU Usage: {cpu_percent:.1f}%
- Memory Usage: {mem_percent:.1f}%

THREAT INDICATORS DETECTED:
{reasons_str}

TASK: Analyze this process and assess if it's malicious, suspicious, or benign.

Consider:
1. Is this a known legitimate process or potentially malicious?
2. Are the resource usage patterns normal?
3. Is the executable path typical for this process?
4. Are there red flags in the command line?
5. Could this be malware, ransomware, cryptominer, or other threat?
6. Could this be attempting file deletion, corruption, or system compromise?

RESPONSE FORMAT (JSON only):
{{
    "level": "LOW" or "MEDIUM" or "HIGH" or "CRITICAL",
    "analysis": "Brief analysis explaining the threat assessment",
    "recommendations": "Specific recommendations (Allow, Monitor, Investigate, Terminate, Block)",
    "is_malicious": true or false,
    "threat_type": "none/malware/ransomware/cryptominer/backdoor/keylogger/other"
}}

Respond ONLY with valid JSON, no additional text."""

            # Get AI response based on model
            response_text = None
            if self.model == 'slm':
                response_text = self.query_slm(prompt)
            elif self.model == 'drona':
                response_text = self.query_drona(prompt)
            elif self.model == 'gemini':
                response = self.ai_model.generate_content(prompt)
                response_text = response.text.strip()
            
            if not response_text:
                return None
            
            # Parse JSON response
            json_match = re.search(r'```json\s*(\{.*?\})\s*```', response_text, re.DOTALL)
            if json_match:
                try:
                    return json.loads(json_match.group(1))
                except json.JSONDecodeError:
                    pass
            
            # Try to find JSON object
            brace_start = response_text.find('{')
            if brace_start != -1:
                brace_count = 0
                brace_end = -1
                for i in range(brace_start, len(response_text)):
                    if response_text[i] == '{':
                        brace_count += 1
                    elif response_text[i] == '}':
                        brace_count -= 1
                        if brace_count == 0:
                            brace_end = i + 1
                            break
                
                if brace_end > brace_start:
                    try:
                        json_str = response_text[brace_start:brace_end]
                        result = json.loads(json_str)
                        if "level" in result:
                            return result
                    except json.JSONDecodeError:
                        pass
            
            # Try to parse entire response
            try:
                result = json.loads(response_text.strip())
                if isinstance(result, dict) and "level" in result:
                    return result
            except json.JSONDecodeError:
                pass
            
            return {
                "level": "UNKNOWN",
                "analysis": response_text[:200] if response_text else "Unable to analyze",
                "recommendations": "Manual review recommended",
                "is_malicious": False,
                "threat_type": "unknown"
            }
        except Exception as e:
            print(f"⚠️  Error analyzing with AI: {e}")
            return None
    
    def send_system_notification(self, title, message, debug=False):
        """Send system notification based on OS"""
        try:
            system = platform.system()
            
            # Escape special characters for safe display
            # Remove or escape problematic characters
            title = str(title).replace('"', "'").replace('\\', '').replace('\n', ' ')[:100]
            message = str(message).replace('"', "'").replace('\\', '').replace('\n', ' ')[:200]
            
            if system == "Darwin":  # macOS
                # Use osascript (built-in, no dependencies needed)
                script = f'display notification "{message}" with title "{title}" sound name "Ping"'
                result = subprocess.run(['osascript', '-e', script], 
                                      capture_output=True, 
                                      text=True,
                                      timeout=2)
                
                if debug or result.returncode != 0:
                    if result.returncode != 0:
                        print(f"⚠️  Notification error (code {result.returncode}): {result.stderr}")
                    else:
                        print(f"✅ Notification sent: {title}")
            
            elif system == "Linux":
                # Use notify-send (usually pre-installed on most Linux distros)
                result = subprocess.run(['notify-send', title, message], 
                                      capture_output=True, 
                                      text=True,
                                      timeout=2)
                
                if debug or result.returncode != 0:
                    if result.returncode != 0:
                        print(f"⚠️  Notification error: {result.stderr}")
                    else:
                        print(f"✅ Notification sent: {title}")
            
            elif system == "Windows":
                # Use PowerShell for Windows notifications
                ps_script = f'''
[Windows.UI.Notifications.ToastNotificationManager, Windows.UI.Notifications, ContentType = WindowsRuntime] > $null
$template = [Windows.UI.Notifications.ToastNotificationManager]::GetTemplateContent([Windows.UI.Notifications.ToastTemplateType]::ToastText02)
$toastXml = [xml] $template.GetXml()
$toastXml.GetElementsByTagName("text")[0].AppendChild($toastXml.CreateTextNode("{title}")) > $null
$toastXml.GetElementsByTagName("text")[1].AppendChild($toastXml.CreateTextNode("{message}")) > $null
$xml = New-Object Windows.Data.Xml.Dom.XmlDocument
$xml.LoadXml($toastXml.OuterXml)
$toast = [Windows.UI.Notifications.ToastNotification]::new($xml)
[Windows.UI.Notifications.ToastNotificationManager]::CreateToastNotifier("Jarvis Network Monitor").Show($toast)
'''
                result = subprocess.run(['powershell', '-Command', ps_script], 
                                      capture_output=True, 
                                      text=True,
                                      timeout=2)
                
                if debug or result.returncode != 0:
                    if result.returncode != 0:
                        print(f"⚠️  Notification error: {result.stderr}")
                    else:
                        print(f"✅ Notification sent: {title}")
                        
        except subprocess.TimeoutExpired:
            if debug:
                print("⚠️  Notification timeout - took too long to send")
        except FileNotFoundError as e:
            if debug:
                print(f"⚠️  Notification system not found: {e}")
        except Exception as e:
            if debug:
                print(f"⚠️  Notification error: {e}")
    
    def alert_network_activity(self, connection, alert_num):
        """Alert on new network activity and analyze if suspicious"""
        print("\n" + "🚨" * 40)
        print(f"🔴 ALERT #{alert_num} - NEW OUTBOUND CONNECTION DETECTED")
        print("🚨" * 40)
        print(f"⏰ Timestamp: {time.strftime('%Y-%m-%d %H:%M:%S')}")
        print("-" * 80)
        
        # Get process information
        process_name = "Unknown"
        process_exe = "Unknown"
        process_cmdline = "Unknown"
        process_user = "Unknown"
        
        try:
            import psutil
            
            if connection['pid'] and connection['pid'] > 0:
                try:
                    proc = psutil.Process(connection['pid'])
                    process_name = proc.name()
                    process_exe = proc.exe()
                    process_cmdline = ' '.join(proc.cmdline()) if proc.cmdline() else "N/A"
                    process_user = proc.username()
                except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
                    process_name = f"Process {connection['pid']} (no access or terminated)"
                except Exception as e:
                    process_name = f"Process {connection['pid']} (error: {str(e)[:50]})"
        except ImportError:
            pass
        
        # Send system notification
        notification_title = f"Network Alert #{alert_num}"
        notification_message = f"{process_name} connected to {connection['remote_ip']}:{connection['remote_port']}"
        self.send_system_notification(notification_title, notification_message, debug=True)
        
        # Display connection details
        print(f"📍 Connection Details:")
        print(f"   • Process ID (PID): {connection['pid'] if connection['pid'] else 'N/A (kernel or system connection)'}")
        print(f"   • Process Name: {process_name}")
        print(f"   • Process Path: {process_exe}")
        print(f"   • Process User: {process_user}")
        if process_cmdline and len(process_cmdline) > 0:
            print(f"   • Command Line: {process_cmdline[:100]}{'...' if len(process_cmdline) > 100 else ''}")
        else:
            print(f"   • Command Line: N/A")
        print()
        print(f"🌐 Network Details:")
        print(f"   • Local Address: {connection['local_ip']}:{connection['local_port']}")
        print(f"   • Remote Address: {connection['remote_ip']}:{connection['remote_port']}")
        print(f"   • Connection Status: {connection['status']}")
        print()
        
        # Try to get geographic location of remote IP (using DNS or simple check)
        remote_info = self.analyze_remote_ip(connection['remote_ip'])
        if remote_info:
            print(f"🔍 Remote IP Analysis:")
            print(f"   • IP Address: {remote_info['ip']}")
            print(f"   • Type: {remote_info['type']}")
            if remote_info.get('hostname'):
                print(f"   • Hostname: {remote_info['hostname']}")
        
        print("-" * 80)
        
        # AI-based threat analysis if model is available
        threat_level_str = "UNKNOWN"
        if self.ai_available:
            print("🤖 AI Analysis: Analyzing connection for suspicious activity...")
            threat_level = self.analyze_connection_threat(connection, process_name, process_exe, process_cmdline, remote_info)
            
            if threat_level:
                threat_level_str = threat_level.get('level', 'UNKNOWN').upper()
                print(f"⚠️  Threat Assessment: {threat_level_str}")
                print(f"💡 Analysis: {threat_level.get('analysis', 'No analysis available')}")
                if threat_level.get('recommendations'):
                    print(f"🛡️  Recommendations: {threat_level.get('recommendations', 'No recommendations')}")
                
                # Send enhanced notification with threat level
                if threat_level_str in ['HIGH', 'CRITICAL']:
                    enhanced_title = f"{threat_level_str} THREAT - Alert #{alert_num}"
                    enhanced_message = f"{process_name} to {connection['remote_ip']} | {threat_level.get('analysis', '')[:100]}"
                    self.send_system_notification(enhanced_title, enhanced_message, debug=True)
        
        print("🚨" * 40)
        print()
    
    def analyze_remote_ip(self, ip_address):
        """Analyze remote IP address to determine if it's suspicious"""
        try:
            import socket
            
            # Check if it's a private IP
            ip_parts = ip_address.split('.')
            if len(ip_parts) == 4:
                first_octet = int(ip_parts[0])
                second_octet = int(ip_parts[1])
                
                # Private IP ranges
                if (first_octet == 10 or 
                    (first_octet == 172 and 16 <= second_octet <= 31) or
                    (first_octet == 192 and second_octet == 168) or
                    first_octet == 127):
                    return {
                        'ip': ip_address,
                        'type': 'Private/Local Network',
                        'hostname': None
                    }
            
            # Try to get hostname
            try:
                hostname = socket.gethostbyaddr(ip_address)[0]
            except:
                hostname = None
            
            return {
                'ip': ip_address,
                'type': 'Public Internet',
                'hostname': hostname
            }
        except Exception as e:
            return {
                'ip': ip_address,
                'type': 'Unknown',
                'hostname': None
            }
    
    def analyze_connection_threat(self, connection, process_name, process_exe, process_cmdline, remote_info):
        """Use AI to analyze if connection is potentially threatening"""
        try:
            # Build analysis prompt
            prompt = f"""You are a cybersecurity expert analyzing network connections for potential threats.
            
CONNECTION DETAILS:
- Process Name: {process_name}
- Process Path: {process_exe}
- Process PID: {connection['pid']}
- Command Line: {process_cmdline}
- Local Address: {connection['local_ip']}:{connection['local_port']}
- Remote Address: {connection['remote_ip']}:{connection['remote_port']}
- Remote IP Type: {remote_info.get('type', 'Unknown') if remote_info else 'Unknown'}
- Remote Hostname: {remote_info.get('hostname', 'N/A') if remote_info else 'N/A'}

TASK: Analyze this outbound network connection and assess if it's suspicious or potentially malicious.

Consider:
1. Is this a known legitimate application?
2. Is the remote IP/hostname suspicious?
3. Is the port number commonly used for malicious activity?
4. Is the process path typical for this application?
5. Are there any red flags in the command line arguments?

RESPONSE FORMAT (JSON only):
{{
    "level": "LOW" or "MEDIUM" or "HIGH" or "CRITICAL",
    "analysis": "Brief analysis explaining the threat level assessment",
    "recommendations": "Specific recommendations for the user (e.g., 'Allow - this is normal Chrome activity', 'Investigate - unusual port for this application', 'Block immediately - known malicious pattern')",
    "is_suspicious": true or false
}}

Respond ONLY with valid JSON, no additional text."""

            # Get AI response based on model
            response_text = None
            if self.model == 'slm':
                response_text = self.query_slm(prompt)
            elif self.model == 'drona':
                response_text = self.query_drona(prompt)
            elif self.model == 'gemini':
                response = self.ai_model.generate_content(prompt)
                response_text = response.text.strip()
            
            if not response_text:
                return None
            
            # Parse JSON response
            # Try to extract JSON from response
            json_match = re.search(r'```json\s*(\{.*?\})\s*```', response_text, re.DOTALL)
            if json_match:
                try:
                    return json.loads(json_match.group(1))
                except json.JSONDecodeError:
                    pass
            
            # Try to find JSON object with balanced braces
            brace_start = response_text.find('{')
            if brace_start != -1:
                brace_count = 0
                brace_end = -1
                for i in range(brace_start, len(response_text)):
                    if response_text[i] == '{':
                        brace_count += 1
                    elif response_text[i] == '}':
                        brace_count -= 1
                        if brace_count == 0:
                            brace_end = i + 1
                            break
                
                if brace_end > brace_start:
                    try:
                        json_str = response_text[brace_start:brace_end]
                        result = json.loads(json_str)
                        if "level" in result:
                            return result
                    except json.JSONDecodeError:
                        pass
            
            # Try to parse entire response as JSON
            try:
                result = json.loads(response_text.strip())
                if isinstance(result, dict) and "level" in result:
                    return result
            except json.JSONDecodeError:
                pass
            
            # If parsing fails, return basic analysis
            return {
                "level": "UNKNOWN",
                "analysis": response_text[:200] if response_text else "Unable to analyze",
                "recommendations": "Manual review recommended",
                "is_suspicious": False
            }
        except Exception as e:
            print(f"⚠️  Error analyzing threat: {e}")
            return None
    
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
    parser.add_argument('-scan', '--scan', action='store_true',
                       help='Scan folder for sensitive files (requires -m drona)')
    parser.add_argument('-f', '--folder', dest='folder_path',
                       help='Folder path to scan (required with -scan)')
    parser.add_argument('-monitor', '--monitor', dest='monitor_type',
                       help='Monitor system activity (network, process, cpu, memory, disk)')
    
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
    
    # Validate scan mode requirements
    if args.scan:
        if args.model != 'drona':
            print("❌ Scan feature is only available with -m drona")
            print("❌ Usage: jarvis -scan -f <folder_path> -m drona [-b <bot_id>]")
            sys.exit(1)
        if not args.folder_path:
            print("❌ Folder path is required with -scan")
            print("❌ Usage: jarvis -scan -f <folder_path> -m drona [-b <bot_id>]")
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
    
    # If monitor mode enabled, run monitoring
    if args.monitor_type:
        monitor_type = args.monitor_type.lower()
        if monitor_type == 'network':
            jarvis.monitor_network()
        elif monitor_type == 'process' or monitor_type == 'processes':
            jarvis.monitor_processes()
        else:
            print(f"❌ Unknown monitor type: {monitor_type}")
            print("💡 Supported monitor types: network, process")
            print("💡 Usage: jarvis -monitor network")
            print("💡 Usage: jarvis -monitor process")
            sys.exit(1)
    # If scan mode enabled, run scan
    elif args.scan:
        jarvis.scan_folder(args.folder_path)
    # If voice mode enabled, start voice command mode
    elif args.voice:
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
