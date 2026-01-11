"""
System information utilities
Gets machine details, IP address, and system metrics
"""

import platform
import socket
from typing import Dict, Any, Optional

try:
    import psutil
    PSUTIL_AVAILABLE = True
except ImportError:
    PSUTIL_AVAILABLE = False


class SystemInfo:
    """Manages system information collection"""
    
    @staticmethod
    def get_ip_address() -> str:
        """Get the machine's IP address"""
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            try:
                s.connect(('8.8.8.8', 80))
                ip = s.getsockname()[0]
            except Exception:
                ip = '127.0.0.1'
            finally:
                s.close()
            return ip
        except Exception:
            return '127.0.0.1'
    
    @staticmethod
    def get_machine_details() -> Dict[str, Any]:
        """Get comprehensive machine details"""
        if not PSUTIL_AVAILABLE:
            return SystemInfo._get_basic_info()
        
        try:
            import os
            
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
                "ip_address": SystemInfo.get_ip_address()
            }
        except Exception as e:
            basic_info = SystemInfo._get_basic_info()
            basic_info["error"] = str(e)
            return basic_info
    
    @staticmethod
    def _get_basic_info() -> Dict[str, Any]:
        """Get basic system info without psutil"""
        import os
        return {
            "system": platform.system(),
            "release": platform.release(),
            "machine": platform.machine(),
            "hostname": platform.node(),
            "current_dir": os.getcwd(),
            "ip_address": SystemInfo.get_ip_address()
        }
    
    @staticmethod
    def get_system_info_string() -> str:
        """Get system information as formatted string"""
        try:
            import psutil
            import os
            
            cpu_percent = psutil.cpu_percent(interval=1)
            cpu_count = psutil.cpu_count()
            cpu_freq = psutil.cpu_freq()
            
            memory = psutil.virtual_memory()
            memory_percent = memory.percent
            memory_available = memory.available // (1024**3)
            memory_total = memory.total // (1024**3)
            
            disk = psutil.disk_usage('/')
            disk_percent = disk.percent
            disk_free = disk.free // (1024**3)
            disk_total = disk.total // (1024**3)
            
            load_avg = os.getloadavg()
            
            info = {
                'system': platform.system(),
                'release': platform.release(),
                'machine': platform.machine(),
                'cpu_percent': cpu_percent,
                'cpu_count': cpu_count,
                'cpu_freq': cpu_freq.current if cpu_freq else "Unknown",
                'memory_percent': memory_percent,
                'memory_available': memory_available,
                'memory_total': memory_total,
                'disk_percent': disk_percent,
                'disk_free': disk_free,
                'disk_total': disk_total,
                'load_avg_1min': load_avg[0],
                'load_avg_5min': load_avg[1],
                'load_avg_15min': load_avg[2],
                'process_count': len(psutil.pids()),
                'current_dir': os.getcwd()
            }
            
            return f"""System: {info['system']} {info['release']} on {info['machine']}
CPU: {info['cpu_percent']:.1f}% usage, {info['cpu_count']} cores @ {info['cpu_freq']:.0f}MHz
Memory: {info['memory_percent']:.1f}% used ({info['memory_total'] - info['memory_available']}GB/{info['memory_total']}GB), {info['memory_available']}GB available
Disk: {info['disk_percent']:.1f}% used ({info['disk_total'] - info['disk_free']}GB/{info['disk_total']}GB), {info['disk_free']}GB free
Load Average: {info['load_avg_1min']:.2f} (1min), {info['load_avg_5min']:.2f} (5min), {info['load_avg_15min']:.2f} (15min)
Processes: {info['process_count']} running
Current Directory: {info['current_dir']}"""
        except Exception as e:
            return f"{platform.system()} {platform.release()}, Current directory: {os.getcwd()}, Error getting detailed metrics: {e}"

