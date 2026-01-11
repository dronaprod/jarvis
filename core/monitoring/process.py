"""
Process monitoring module
Monitors processes for anomalies, threats, and suspicious behavior
"""

import time
import platform
from typing import Dict, Any, Optional

try:
    import psutil
    PSUTIL_AVAILABLE = True
except ImportError:
    PSUTIL_AVAILABLE = False

from utils.notifications import NotificationManager


class ProcessMonitor:
    """Monitor processes for anomalies, threats, and suspicious behavior"""
    
    def __init__(self, model: str = 'gemini', ai_provider=None, notification_manager: Optional[NotificationManager] = None):
        """
        Initialize process monitor
        
        Args:
            model: AI model name for threat analysis
            ai_provider: AI provider instance for threat analysis
            notification_manager: Notification manager instance
        """
        self.model = model
        self.ai_provider = ai_provider
        self.notification_manager = notification_manager or NotificationManager(debug=True)
        self.running = False
        
        # CPU/Memory thresholds
        self.HIGH_CPU_THRESHOLD = 80.0  # 80% CPU usage
        self.HIGH_MEMORY_THRESHOLD = 80.0  # 80% memory usage
    
    def analyze_process_threat(self, pinfo: Dict[str, Any]) -> Dict[str, Any]:
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
            
        except Exception:
            pass
        
        return indicators
    
    def analyze_process_with_ai(self, pinfo: Dict[str, Any], indicators: Dict[str, Any]) -> Optional[Dict[str, Any]]:
        """Use AI to analyze process threat level"""
        if not self.ai_provider:
            return None
        
        try:
            import json
            import re
            
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
    
    def alert_process_activity(self, activity: Dict[str, Any], alert_num: int) -> None:
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
        if self.ai_provider and activity['type'] == 'NEW_PROCESS':
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
        
        self.notification_manager.send(notification_title, notification_message)
        
        # Send enhanced notification for HIGH/CRITICAL threats
        if activity['severity'] in ['HIGH', 'CRITICAL']:
            enhanced_title = f"{activity['severity']} THREAT - {activity['type']}"
            enhanced_message = f"{name} (PID {pid}) | {username} | Check terminal for details"
            self.notification_manager.send(enhanced_title, enhanced_message)
    
    def monitor(self) -> None:
        """Monitor processes for anomalies, threats, and suspicious behavior"""
        if not PSUTIL_AVAILABLE:
            print("❌ psutil module not found. Please install it: pip3 install psutil")
            return
        
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
        self.running = True
        
        try:
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
            while self.running:
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
                            if cpu_current > self.HIGH_CPU_THRESHOLD:
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
                            if mem_current > self.HIGH_MEMORY_THRESHOLD:
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
                    except Exception:
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
        finally:
            self.running = False
    
    def stop(self) -> None:
        """Stop monitoring"""
        self.running = False

