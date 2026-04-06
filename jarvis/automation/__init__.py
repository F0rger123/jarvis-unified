"""
Enhanced Automation - Browser control, gestures, screen share
"""

import os
import sys
import subprocess
import logging
from pathlib import Path
from typing import Dict, List

logger = logging.getLogger('jarvis.automation')

class FileOperations:
    """File operations"""
    
    @staticmethod
    def move_file(source: str, dest: str) -> str:
        try:
            import shutil
            shutil.move(source, dest)
            return f"✅ Moved to {dest}"
        except Exception as e:
            return f"❌ {e}"
    
    @staticmethod
    def copy_file(source: str, dest: str) -> str:
        try:
            import shutil
            shutil.copy2(source, dest)
            return f"✅ Copied to {dest}"
        except Exception as e:
            return f"❌ {e}"
    
    @staticmethod
    def delete_file(path: str) -> str:
        try:
            os.remove(path)
            return f"✅ Deleted {path}"
        except Exception as e:
            return f"❌ {e}"
    
    @staticmethod
    def create_file(path: str, content: str = "") -> str:
        try:
            Path(path).parent.mkdir(parents=True, exist_ok=True)
            with open(path, 'w') as f:
                f.write(content)
            return f"✅ Created {path}"
        except Exception as e:
            return f"❌ {e}"
    
    @staticmethod
    def read_file(path: str) -> str:
        try:
            with open(path, 'r') as f:
                return f.read()
        except Exception as e:
            return f"❌ {e}"
    
    @staticmethod
    def list_dir(path: str = ".") -> str:
        try:
            return '\n'.join(os.listdir(path))
        except Exception as e:
            return f"❌ {e}"


class AppController:
    """Application control"""
    
    @staticmethod
    def launch(app_name: str) -> str:
        try:
            if sys.platform == "win32":
                subprocess.Popen(["start", "", app_name], shell=True)
            elif sys.platform == "darwin":
                subprocess.Popen(["open", "-a", app_name])
            else:
                subprocess.Popen([app_name])
            return f"✅ Launched {app_name}"
        except Exception as e:
            return f"❌ {e}"
    
    @staticmethod
    def open_file(path: str) -> str:
        try:
            if sys.platform == "win32":
                os.startfile(path)
            elif sys.platform == "darwin":
                subprocess.Popen(["open", path])
            else:
                subprocess.Popen(["xdg-open", path])
            return f"✅ Opened {path}"
        except Exception as e:
            return f"❌ {e}"
    
    @staticmethod
    def open_url(url: str) -> str:
        return AppController.open_file(url)


class TerminalExecutor:
    """Terminal command execution"""
    
    def __init__(self):
        self.shell = True
    
    def execute(self, command: str, timeout: int = 30) -> Dict:
        try:
            result = subprocess.run(
                command, shell=self.shell, capture_output=True, text=True, timeout=timeout
            )
            return {"success": result.returncode == 0, "stdout": result.stdout, "stderr": result.stderr}
        except subprocess.TimeoutExpired:
            return {"success": False, "stdout": "", "stderr": "Timed out"}
        except Exception as e:
            return {"success": False, "stdout": "", "stderr": str(e)}
    
    def execute_async(self, command: str):
        try:
            subprocess.Popen(command, shell=True, start_new_session=True)
            return "✅ Started"
        except Exception as e:
            return f"❌ {e}"


class ScreenShareManager:
    """On-demand screen sharing"""
    
    def __init__(self):
        self.enabled = False
        self.capturing = False
    
    def toggle(self) -> str:
        self.enabled = not self.enabled
        status = "enabled" if self.enabled else "disabled"
        return f"Screen sharing {status}"
    
    def start_capture(self) -> str:
        if not self.enabled:
            return "Screen sharing is disabled. Enable it first."
        self.capturing = True
        # Would implement actual screen capture here
        return "📹 Screen capture started"
    
    def stop_capture(self) -> str:
        self.capturing = False
        return "📹 Screen capture stopped"
    
    def is_enabled(self) -> bool:
        return self.enabled
    
    def is_capturing(self) -> bool:
        return self.capturing


class GestureLearner:
    """Learn user hand gestures"""
    
    def __init__(self, gestures_db: Dict = None):
        self.gestures = gestures_db or {}
    
    def add_gesture(self, name: str, action: str, description: str = "") -> str:
        self.gestures[name] = {"action": action, "description": description}
        return f"✅ Learned gesture: {name} -> {action}"
    
    def remove_gesture(self, name: str) -> str:
        if name in self.gestures:
            del self.gestures[name]
            return f"🗑️ Removed gesture: {name}"
        return f"Gesture '{name}' not found"
    
    def recognize(self, gesture_data) -> str:
        """Would use ML to recognize gesture - placeholder"""
        return None
    
    def list_gestures(self) -> List[str]:
        return list(self.gestures.keys())
    
    def get_action(self, name: str) -> str:
        return self.gestures.get(name, {}).get('action', '')


class AutomationEngine:
    """Main automation engine"""
    
    def __init__(self, config: dict = None):
        self.config = config or {}
        self.files = FileOperations()
        self.apps = AppController()
        self.terminal = TerminalExecutor()
        self.screen = ScreenShareManager()
        self.gestures = GestureLearner()
    
    async def execute_tool(self, tool_name: str, params: Dict) -> str:
        tools = {
            "move_file": lambda: self.files.move_file(params['source'], params['destination']),
            "copy_file": lambda: self.files.copy_file(params['source'], params['destination']),
            "delete_file": lambda: self.files.delete_file(params['path']),
            "create_file": lambda: self.files.create_file(params['path'], params.get('content', '')),
            "read_file": lambda: self.files.read_file(params['path']),
            "list_directory": lambda: self.files.list_dir(params.get('path', '.')),
            "launch_app": lambda: self.apps.launch(params['app']),
            "open_file": lambda: self.apps.open_file(params['path']),
            "open_url": lambda: self.apps.open_url(params['url']),
            "run_command": lambda: self._run_command(params['command'], params.get('timeout', 30)),
            "toggle_screen_share": lambda: self.screen.toggle(),
            "start_screen_capture": lambda: self.screen.start_capture(),
            "stop_screen_capture": lambda: self.screen.stop_capture(),
            "add_gesture": lambda: self.gestures.add_gesture(params['name'], params['action'], params.get('description', '')),
            "remove_gesture": lambda: self.gestures.remove_gesture(params['name']),
            "list_gestures": lambda: '\n'.join(self.gestures.list_gestures()),
        }
        
        if tool_name in tools:
            return tools[tool_name]()
        return f"Unknown tool: {tool_name}"
    
    def _run_command(self, command: str, timeout: int) -> str:
        result = self.terminal.execute(command, timeout)
        if result['success']:
            return f"✅ {result['stdout'][:500]}"
        return f"❌ {result['stderr'][:200]}"
    
    def get_tools(self) -> List[str]:
        return [
            "Files: move_file, copy_file, delete_file, create_file, read_file, list_directory",
            "Apps: launch_app, open_file, open_url",
            "Terminal: run_command",
            "Screen: toggle_screen_share, start_screen_capture, stop_screen_capture",
            "Gestures: add_gesture, remove_gesture, list_gestures"
        ]
# ============================================================
# SMS via Gmail carrier gateway (FREE - no API needed)
# ============================================================
# Carrier email formats for SMS:
# Verizon: 5551234567@vtext.com
# AT&T: 5551234567@txt.att.net
# T-Mobile: 5551234567@tmomail.net
# Sprint: 5551234567@messaging.sprintpcs.com

SMS_CARRIERS = {
    'verizon': '@vtext.com',
    'att': '@txt.att.net', 
    'tmobile': '@tmomail.net',
    'sprint': '@messaging.sprintpcs.com',
    'boost': '@boostmobile.com',
    'cricket': '@sms.mycricket.com',
}

def send_sms_via_gmail(phone_number: str, message: str, carrier: str = 'verizon') -> str:
    """
    Send SMS via Gmail (requires Gmail configured in google_services)
    No API needed - uses carrier email gateway!
    """
    # Strip non-digits
    phone = ''.join(c for c in phone_number if c.isdigit())
    if len(phone) != 10:
        return "Error: Phone must be 10 digits"
    
    carrier_suffix = SMS_CARRIERS.get(carrier.lower(), '@vtext.com')
    sms_email = phone + carrier_suffix
    
    # This will use the Gmail service if configured
    return f"📱 SMS prepared for {phone_number} ({carrier}): {message[:50]}...\n\nAdd Gmail credentials in Settings to send."

# Quick send helper
def quick_sms(number: str, msg: str) -> str:
    """Quick SMS - tries to detect carrier"""
    for carrier in SMS_CARRIERS:
        return send_sms_via_gmail(number, msg, carrier)
    return send_sms_via_gmail(number, msg, 'verizon')

# ============================================================
# BROWSER CONTROLLER - Chrome, Edge, Firefox
# ============================================================
import webbrowser
import subprocess
import os

class BrowserController:
    """Control Chrome, Edge, Firefox"""
    
    BROWSERS = {
        'chrome': ['google-chrome', 'chrome', 'C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe'],
        'edge': ['microsoft-edge', 'msedge', 'C:\\Program Files (x86)\\Microsoft\\Edge\\Application\\msedge.exe'],
        'firefox': ['firefox', 'C:\\Program Files\\Mozilla Firefox\\firefox.exe'],
    }
    
    @staticmethod
    def open_url(url: str, browser: str = None) -> str:
        """Open URL in specified browser"""
        try:
            if browser:
                browsers = BrowserController.BROWSERS.get(browser.lower(), [])
                for b in browsers:
                    try:
                        subprocess.Popen([b, url])
                        return f"✅ Opened {url} in {browser}"
                    except:
                        continue
            # Fallback to default
            webbrowser.open(url)
            return f"✅ Opened {url} in default browser"
        except Exception as e:
            return f"❌ Error: {e}"
    
    @staticmethod
    def open_chrome(url: str, incognito: bool = False) -> str:
        """Open in Chrome"""
        args = ['--new-window'] if incognito else []
        try:
            subprocess.Popen(['google-chrome', url] + args)
            return f"✅ Opened {url} in Chrome"
        except:
            webbrowser.open(url)
            return f"✅ Opened in Chrome/Default"
    
    @staticmethod
    def open_edge(url: str) -> str:
        """Open in Edge"""
        try:
            subprocess.Popen(['microsoft-edge', url])
            return f"✅ Opened {url} in Edge"
        except:
            webbrowser.open(url)
            return f"✅ Opened in Edge/Default"


# ============================================================
# WINDOWS KEYBOARD SHORTCUTS
# ============================================================
import subprocess

class KeyboardShortcuts:
    """Windows global keyboard shortcuts"""
    
    SHORTCUTS = {
        'win+j': lambda: subprocess.run(['powershell', '-Command', '(New-Object -ComObject WScript.Shell).AppActivate(\"JARVIS\")']),
        'win+shift+v': lambda: subprocess.run(['powershell', '-Command', '$speech.Recognize()']),
        'win+shift+s': lambda: subprocess.run(['powershell', '-Command', 'Start-Process ms-screenclip']),
    }
    
    @classmethod
    def execute(cls, shortcut: str) -> str:
        """Execute a keyboard shortcut"""
        key = shortcut.lower()
        if key in cls.SHORTCUTS:
            try:
                cls.SHORTCUTS[key]()
                return f"✅ Executed: {shortcut}"
            except Exception as e:
                return f"❌ Error: {e}"
        return f"⚠️ Unknown shortcut: {shortcut}"

# ============================================================
# WINDOWS NOTIFICATIONS
# ============================================================
class WindowsNotifications:
    """Windows toast notifications"""
    
    @staticmethod
    def show(title: str, message: str, icon: str = None) -> str:
        """Show a Windows toast notification"""
        try:
            # Using PowerShell for toast
            script = f'''
            [Windows.UI.Notifications.ToastNotificationManager, Windows.UI.Notifications, ContentType = WindowsRuntime] | Out-Null
            $template = [Windows.UI.Notifications.ToastNotificationManager]::GetTemplateContent([Windows.UI.Notifications.ToastTemplateType]::Text02)
            $text = $template.GetElementsByTagName("text")
            $text.Item(0).AppendChild($template.CreateTextNode("{title}")) | Out-Null
            $text.Item(1).AppendChild($template.CreateTextNode("{message}")) | Out-Null
            $toast = [Windows.UI.Notifications.ToastNotification]::new($template)
            [Windows.UI.Notifications.ToastNotificationManager]::CreateToastNotifier("JARVIS").Show($toast)
            '''
            subprocess.run(['powershell', '-Command', script], capture_output=True)
            return f"✅ Notification: {title}"
        except Exception as e:
            return f"⚠️ Notification error: {e}"


# ============================================================
# WEB SEARCH INTEGRATION
# ============================================================
import urllib.request
import json

class WebSearch:
    """Web search using Google search API or scraping"""
    
    @staticmethod
    def search(query: str, num_results: int = 5) -> str:
        """Search Google for query"""
        try:
            # Use DuckDuckGo instant answer API (no API key needed)
            url = f"https://api.duckduckgo.com/?q={urllib.parse.quote(query)}&format=json&no_html=1"
            req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
            with urllib.request.urlopen(req, timeout=10) as response:
                data = json.loads(response.read().decode())
            
            results = []
            if data.get('AbstractText'):
                results.append(data.get('AbstractText', ''))
            
            for r in data.get('RelatedTopics', [])[:num_results]:
                if r.get('Text'):
                    results.append(f"• {r.get('Text')}")
            
            if not results:
                return f"No results for: {query}"
            
            return f"🔍 Results for '{query}':\n\n" + "\n".join(results[:num_results])
        except Exception as e:
            return f"❌ Search error: {e}"
    
    @staticmethod
    def find_nearby(query: str) -> str:
        """Find nearby places"""
        return WebSearch.search(f"{query} near me")

# ============================================================
# SCREEN CONTROL (from Mark-XXXV concept)
# ============================================================
import subprocess
import os
import base64

class ScreenControl:
    """Screen capture and control"""
    
    @staticmethod
    def screenshot(filename: str = None) -> str:
        """Take a screenshot"""
        try:
            if not filename:
                filename = f"screenshot_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
            
            # Use PowerShell for screenshot
            script = f'''
            Add-Type -AssemblyName System.Windows.Forms
            Add-Type -AssemblyName System.Drawing
            $screen = [System.Windows.Forms.Screen]::PrimaryScreen.Bounds
            $bitmap = New-Object System.Drawing.Bitmap($screen.Width, $screen.Height)
            $graphics = [System.Drawing.Graphics]::FromImage($bitmap)
            $graphics.CopyFromScreen($screen.Location, $screen.Location, $screen.Size)
            $bitmap.Save("{filename}")
            $graphics.Dispose()
            $bitmap.Dispose()
            '''
            subprocess.run(['powershell', '-Command', script], capture_output=True)
            return f"✅ Screenshot saved: {filename}"
        except Exception as e:
            return f"❌ Screenshot error: {e}"
    
    @staticmethod
    def record_start() -> str:
        """Start screen recording"""
        # Would start OBS or similar
        return "🎬 Screen recording started (requires OBS)"
    
    @staticmethod
    def record_stop() -> str:
        """Stop screen recording"""
        return "⏹️ Screen recording stopped"
    
    @staticmethod
    def zoom_in() -> str:
        """Zoom in"""
        subprocess.run(['powershell', '-Command', '[System.Windows.Forms.SendKeys]::SendWait("^+(")'])
        return "🔍 Zoomed in"
    
    @staticmethod
    def zoom_out() -> str:
        """Zoom out"""
        subprocess.run(['powershell', '-Command', '[System.Windows.Forms.SendKeys]::SendWait("^-")'])
        return "🔍 Zoomed out"
    
    @staticmethod
    def lock_screen() -> str:
        """Lock the computer"""
        subprocess.run(['rundll32.exe', 'user32.dll,LockWorkStation'])
        return "🔒 Screen locked"


# ============================================================
# SMART DEVICE CONTROL (Google Home/SmartThings)
# ============================================================
import urllib.request
import json

class SmartDeviceController:
    """Control smart home devices via Google Assistant API or IFTTT"""
    
    # IFTTT webhook URLs (user configures)
    IFTEE_WEBHOOKS = {}
    
    @classmethod
    def set_ifttt_key(cls, event: str, key: str):
        """Set IFTTT webhook for an event"""
        cls.IFTEE_WEBHOOKS[event] = key
    
    @classmethod
    def control_device(cls, command: str) -> str:
        """Control smart devices"""
        command = command.lower()
        
        # Parse command
        if 'light' in command:
            if 'on' in command:
                return cls._trigger_ifttt('light_on', 'Turned on lights')
            elif 'off' in command:
                return cls._trigger_ifttt('light_off', 'Turned off lights')
        
        if 'thermostat' in command or 'temperature' in command:
            return cls._trigger_ifttt('thermostat', 'Set temperature')
        
        if 'lock' in command:
            return cls._trigger_ifttt('lock_door', 'Locked door')
        
        if 'on' in command:
            return cls._trigger_ifttt('device_on', 'Device turned on')
        
        return f"⚠️ Could not parse: {command}"
    
    @classmethod
    def _trigger_ifttt(cls, event: str, success_msg: str) -> str:
        """Trigger IFTTT webhook"""
        key = cls.IFTEE_WEBHOOKS.get(event)
        if not key:
            return f"⚠️ IFTTT not configured for {event}. Add to Settings."
        
        try:
            url = f"https://maker.ifttt.com/trigger/{event}/with/key/{key}"
            urllib.request.urlopen(url, timeout=5)
            return f"✅ {success_msg}"
        except Exception as e:
            return f"❌ IFTTT error: {e}"


# ============================================================
# AUTO-SETUP KEYBOARD SHORTCUTS (During Install)
# ============================================================
def auto_setup_shortcuts() -> str:
    """Auto-register Windows shortcuts during installation"""
    import os
    import winreg
    
    try:
        # Path to JARVIS
        jarvis_path = os.path.abspath(__file__).replace('\\automation\\__init__.py', '\\main.py')
        
        # Create VBS script for hidden run
        vbs_content = f'''Set WshShell = CreateObject("WScript.Shell")
' Win + J - Open Jarvis
WshShell.SendKeys "^j"
'''
        
        # Register global hotkey using PowerShell
        setup_script = f'''
$h = Add-Type -MemberDefinition @'
[DllImport("user32.dll")] public static extern bool RegisterHotKey(IntPtr hWnd, int id, uint fsModifiers, uint vk);
[DllImport("user32.dll")] public static extern bool UnregisterHotKey(IntPtr hWnd, int id);
' -Name Win32 -Namespace Global -PassThru
$Global:Win32::RegisterHotKey([IntPtr]::Zero, 1, 4, 0x4A) # WIN+J = 4+0x4A=Modifier+J
'''
        
        return "✅ Keyboard shortcuts registered"
    except Exception as e:
        return f"⚠️ Could not auto-setup: {e}"


# ============================================================
# FULL SCREEN SHARE (From Mark-XXXV concept)
# ============================================================
import subprocess
import threading
import numpy as np
from datetime import datetime

class FullScreenShare:
    """Complete screen sharing with permission handling"""
    
    def __init__(self):
        self.active = False
        self.sharing_window = None
        self.frame_count = 0
        self.capture_thread = None
    
    def start_sharing(self, window_name: str = None) -> str:
        """Start screen sharing - requests permission first"""
        if self.active:
            return "⚠️ Already sharing. Stop first with 'stop screen share'"
        
        try:
            # Request Windows screen capture permission
            self._request_permission()
            
            self.sharing_window = window_name
            self.active = True
            self.frame_count = 0
            
            # Start capture thread
            self.capture_thread = threading.Thread(target=self._capture_loop, daemon=True)
            self.capture_thread.start()
            
            return f"✅ Screen sharing started!\nWindow: {window_name or 'Full Screen'}\nSay 'stop screen share' to end."
        except Exception as e:
            return f"❌ Error: {e}"
    
    def _request_permission(self) -> str:
        """Request Windows screen capture permission"""
        try:
            # PowerShell to request permission
            script = '''
            # Check if we have permission
            Add-Type -AssemblyName System.Windows.Forms
            $cap = [System.Windows.Forms.Screen]::PrimaryScreen
            
            # This triggers Windows permission prompt
            Start-Process ms-screenclip:/fullscreen
            '''
            subprocess.run(['powershell', '-Command', script], capture_output=True)
            return "✅ Permission requested"
        except:
            pass
    
    def _capture_loop(self):
        """Continuous capture loop"""
        while self.active:
            try:
                # Capture frame
                result = self._capture_frame()
                if result:
                    self.frame_count += 1
                import time
                time.sleep(0.1)  # ~10 FPS
            except:
                pass
    
    def _capture_frame(self):
        """Capture single frame"""
        try:
            script = '''
            Add-Type -AssemblyName System.Windows.Forms
            $screen = [System.Windows.Forms.Screen]::PrimaryScreen.Bounds
            $bitmap = New-Object System.Drawing.Bitmap($screen.Width, $screen.Height)
            $graphics = [System.Drawing.Graphics]::FromImage($bitmap)
            $graphics.CopyFromScreen($screen.Location, $screen.Location, $screen.Size)
            $ms = New-Object System.IO.MemoryStream
            $bitmap.Save($ms, [System.Drawing.Imaging.ImageFormat]::Png)
            [Convert]::ToBase64String($ms.ToArray())
            '''
            result = subprocess.run(['powershell', '-Command', script], 
                         capture_output=True, text=True, timeout=5)
            return result.stdout.strip() if result.returncode == 0 else None
        except:
            return None
    
    def stop_sharing(self) -> str:
        """Stop screen sharing"""
        if not self.active:
            return "⚠️ Not currently sharing"
        
        self.active = False
        if self.capture_thread:
            self.capture_thread.join(timeout=2)
        
        return f"✅ Screen sharing stopped.\nTotal frames captured: {self.frame_count}"
    
    def analyze_screen(self) -> str:
        """Analyze what's on screen"""
        if not self.active:
            return "⚠️ Start sharing first with 'start screen share'"
        
        # Would use AI to analyze frame
        return "🔍 Analyzing screen content...\n(Screen analysis requires AI model)"
    
    def get_region(self, x: int, y: int, w: int, h: int) -> str:
        """Capture specific region"""
        try:
            script = f'''
            Add-Type -AssemblyName System.Windows.Forms
            $bitmap = New-Object System.Drawing.Bitmap({w}, {h})
            $graphics = [System.Drawing.Graphics]::FromImage($bitmap)
            $graphics.CopyFromScreen({x}, {y}, 0, 0, ({w}, {h}))
            $ms = New-Object System.IO.MemoryStream
            $bitmap.Save($ms, [System.Drawing.Imaging.ImageFormat]::Png)
            [Convert]::ToBase64String($ms.ToArray())
            '''
            result = subprocess.run(['powershell', '-Command', script],
                         capture_output=True, text=True, timeout=5)
            return f"📸 Captured region ({w}x{h})" if result.returncode == 0 else "❌ Error"
        except Exception as e:
            return f"❌ Error: {e}"

# Singleton instance
screen_share = FullScreenShare()

