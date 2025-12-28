#!/usr/bin/env python3
"""
Quick test script for desktop notifications
"""

import subprocess
import platform

def test_notification():
    """Test if notifications work"""
    system = platform.system()
    print(f"🖥️  System: {system}")
    print("🔔 Testing notification system...\n")
    
    if system == "Darwin":  # macOS
        print("📱 Sending macOS notification...")
        title = "Jarvis Test"
        message = "If you see this, notifications are working!"
        script = f'display notification "{message}" with title "{title}" sound name "Ping"'
        
        result = subprocess.run(['osascript', '-e', script], 
                              capture_output=True, 
                              text=True,
                              timeout=2)
        
        if result.returncode == 0:
            print("✅ Notification sent successfully!")
            print("\n💡 Check your notification center (top-right corner)")
            print("💡 If you don't see it, check System Settings:")
            print("   1. Open System Settings")
            print("   2. Go to Notifications")
            print("   3. Find 'Terminal' or 'Python' in the list")
            print("   4. Make sure notifications are enabled")
            print("   5. Set alert style to 'Alerts' or 'Banners'")
        else:
            print(f"❌ Error sending notification:")
            print(f"   Exit code: {result.returncode}")
            print(f"   Error: {result.stderr}")
            
    elif system == "Linux":
        print("📱 Sending Linux notification...")
        result = subprocess.run(['notify-send', 'Jarvis Test', 
                               'If you see this, notifications are working!'], 
                              capture_output=True, 
                              text=True,
                              timeout=2)
        
        if result.returncode == 0:
            print("✅ Notification sent successfully!")
        else:
            print(f"❌ Error: {result.stderr}")
            print("💡 Make sure notify-send is installed: sudo apt install libnotify-bin")
            
    elif system == "Windows":
        print("📱 Sending Windows notification...")
        print("💡 This uses PowerShell - may take a few seconds...")
        # Simple Windows notification
        result = subprocess.run([
            'powershell', 
            '-Command',
            'Add-Type -AssemblyName System.Windows.Forms; [System.Windows.Forms.MessageBox]::Show("If you see this, the notification system is partially working. Full toast notifications require Windows 10+", "Jarvis Test")'
        ], capture_output=True, text=True, timeout=5)
        
        if result.returncode == 0:
            print("✅ Test completed!")
        else:
            print(f"❌ Error: {result.stderr}")
    else:
        print(f"❌ Unknown system: {system}")

if __name__ == "__main__":
    test_notification()

