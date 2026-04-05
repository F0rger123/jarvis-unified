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