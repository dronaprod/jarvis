"""
Network monitoring module
Monitors outbound network connections and alerts on suspicious activity
"""

import time
import platform
from typing import Dict, Any, Optional, Callable

try:
    import psutil
    PSUTIL_AVAILABLE = True
except ImportError:
    PSUTIL_AVAILABLE = False

from utils.notifications import NotificationManager


class NetworkMonitor:
    """Monitor network connections for suspicious outbound traffic"""
    
    def __init__(self, model: str = 'gemini', ai_provider=None, notification_manager: Optional[NotificationManager] = None):
        """
        Initialize network monitor
        
        Args:
            model: AI model name for threat analysis
            ai_provider: AI provider instance for threat analysis
            notification_manager: Notification manager instance
        """
        self.model = model
        self.ai_provider = ai_provider
        self.notification_manager = notification_manager or NotificationManager(debug=True)
        self.running = False
    
    def analyze_remote_ip(self, ip_address: str) -> Dict[str, Any]:
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
    
    def analyze_connection_threat(self, connection: Dict[str, Any], process_name: str, 
                                   process_exe: str, process_cmdline: str, 
                                   remote_info: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Use AI to analyze if connection is potentially threatening"""
        if not self.ai_provider:
            return None
        
        try:
            import json
            import re
            
            from config.prompts import build_network_threat_prompt
            prompt = build_network_threat_prompt(
                connection, process_name, process_exe, process_cmdline, remote_info
            )

            # Get AI response
            response_text = self.ai_provider.query(prompt)
            
            if not response_text:
                return None
            
            # Parse JSON response
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
    
    def alert_network_activity(self, connection: Dict[str, Any], alert_num: int) -> None:
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
        
        if PSUTIL_AVAILABLE and connection['pid'] and connection['pid'] > 0:
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
        
        # Send system notification
        notification_title = f"Network Alert #{alert_num}"
        notification_message = f"{process_name} connected to {connection['remote_ip']}:{connection['remote_port']}"
        self.notification_manager.send(notification_title, notification_message)
        
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
        
        # Try to get geographic location of remote IP
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
        if self.ai_provider:
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
                    self.notification_manager.send(enhanced_title, enhanced_message)
        
        print("🚨" * 40)
        print()
    
    def monitor(self) -> None:
        """Monitor network connections and alert on suspicious outbound traffic"""
        if not PSUTIL_AVAILABLE:
            print("❌ psutil module not found. Please install it: pip3 install psutil")
            return
        
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
        self.running = True
        
        try:
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
                except (AttributeError, TypeError):
                    continue
            
            print(f"✅ Baseline established: {len(known_connections)} active connections")
            print("🔍 Now monitoring for NEW outbound connections...\n")
            
            # Continuous monitoring loop
            iteration = 0
            while self.running:
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
                    except (AttributeError, TypeError):
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
        finally:
            self.running = False
    
    def stop(self) -> None:
        """Stop monitoring"""
        self.running = False

