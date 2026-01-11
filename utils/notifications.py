"""
Cross-platform desktop notification system
Supports macOS, Linux, and Windows
"""

import platform
import subprocess
from typing import Optional


class NotificationManager:
    """Manages desktop notifications across different platforms"""
    
    def __init__(self, debug: bool = False):
        self.debug = debug
        self.system = platform.system()
    
    def send(self, title: str, message: str) -> bool:
        """
        Send a desktop notification
        
        Args:
            title: Notification title
            message: Notification message
            
        Returns:
            True if notification was sent successfully, False otherwise
        """
        try:
            # Escape special characters for safe display
            title = str(title).replace('"', "'").replace('\\', '').replace('\n', ' ')[:100]
            message = str(message).replace('"', "'").replace('\\', '').replace('\n', ' ')[:200]
            
            if self.system == "Darwin":  # macOS
                return self._send_macos(title, message)
            elif self.system == "Linux":
                return self._send_linux(title, message)
            elif self.system == "Windows":
                return self._send_windows(title, message)
            else:
                if self.debug:
                    print(f"⚠️  Unsupported platform: {self.system}")
                return False
        except Exception as e:
            if self.debug:
                print(f"⚠️  Notification error: {e}")
            return False
    
    def _send_macos(self, title: str, message: str) -> bool:
        """Send notification on macOS using osascript"""
        try:
            script = f'display notification "{message}" with title "{title}" sound name "Ping"'
            result = subprocess.run(
                ['osascript', '-e', script],
                capture_output=True,
                text=True,
                timeout=2
            )
            
            if self.debug:
                if result.returncode != 0:
                    print(f"⚠️  Notification error (code {result.returncode}): {result.stderr}")
                else:
                    print(f"✅ Notification sent: {title}")
            
            return result.returncode == 0
        except subprocess.TimeoutExpired:
            if self.debug:
                print("⚠️  Notification timeout")
            return False
        except FileNotFoundError:
            if self.debug:
                print("⚠️  osascript not found")
            return False
    
    def _send_linux(self, title: str, message: str) -> bool:
        """Send notification on Linux using notify-send"""
        try:
            result = subprocess.run(
                ['notify-send', title, message],
                capture_output=True,
                text=True,
                timeout=2
            )
            
            if self.debug:
                if result.returncode != 0:
                    print(f"⚠️  Notification error: {result.stderr}")
                else:
                    print(f"✅ Notification sent: {title}")
            
            return result.returncode == 0
        except subprocess.TimeoutExpired:
            if self.debug:
                print("⚠️  Notification timeout")
            return False
        except FileNotFoundError:
            if self.debug:
                print("⚠️  notify-send not found. Install: sudo apt install libnotify-bin")
            return False
    
    def _send_windows(self, title: str, message: str) -> bool:
        """Send notification on Windows using PowerShell"""
        try:
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
            result = subprocess.run(
                ['powershell', '-Command', ps_script],
                capture_output=True,
                text=True,
                timeout=2
            )
            
            if self.debug:
                if result.returncode != 0:
                    print(f"⚠️  Notification error: {result.stderr}")
                else:
                    print(f"✅ Notification sent: {title}")
            
            return result.returncode == 0
        except subprocess.TimeoutExpired:
            if self.debug:
                print("⚠️  Notification timeout")
            return False
        except FileNotFoundError:
            if self.debug:
                print("⚠️  PowerShell not found")
            return False

