"""
Automation Module - File ops, app control, terminal
From Mark-XXXV and desktop automation features
"""

import os
import sys
import shutil
import subprocess
import logging
from pathlib import Path
from typing import Optional, Dict, List

logger = logging.getLogger('jarvis.automation')

class FileOperations:
    """File system operations - move, delete, edit, create"""
    
    @staticmethod
    def move_file(source: str, destination: str) -> str:
        """Move a file from source to destination"""
        try:
            shutil.move(source, destination)
            return f"✅ Moved file to {destination}"
        except Exception as e:
            return f"❌ Error moving file: {str(e)}"
    
    @staticmethod
    def copy_file(source: str, destination: str) -> str:
        """Copy a file"""
        try:
            shutil.copy2(source, destination)
            return f"✅ Copied file to {destination}"
        except Exception as e:
            return f"❌ Error copying file: {str(e)}"
    
    @staticmethod
    def delete_file(path: str) -> str:
        """Delete a file"""
        try:
            os.remove(path)
            return f"✅ Deleted {path}"
        except Exception as e:
            return f"❌ Error deleting file: {str(e)}"
    
    @staticmethod
    def create_file(path: str, content: str = "") -> str:
        """Create a new file with content"""
        try:
            Path(path).parent.mkdir(parents=True, exist_ok=True)
            with open(path, 'w') as f:
                f.write(content)
            return f"✅ Created {path}"
        except Exception as e:
            return f"❌ Error creating file: {str(e)}"
    
    @staticmethod
    def read_file(path: str) -> str:
        """Read file contents"""
        try:
            with open(path, 'r') as f:
                return f.read()
        except Exception as e:
            return f"❌ Error reading file: {str(e)}"
    
    @staticmethod
    def list_directory(path: str = ".") -> List[str]:
        """List directory contents"""
        try:
            return os.listdir(path)
        except Exception as e:
            return [f"Error: {str(e)}"]
    
    @staticmethod
    def create_directory(path: str) -> str:
        """Create a directory"""
        try:
            Path(path).mkdir(parents=True, exist_ok=True)
            return f"✅ Created directory {path}"
        except Exception as e:
            return f"❌ Error creating directory: {str(e)}"


class AppController:
    """Launch and control applications"""
    
    @staticmethod
    def launch_app(app_name: str) -> str:
        """Launch an application"""
        try:
            if sys.platform == "win32":
                subprocess.Popen(["start", "", app_name], shell=True)
            elif sys.platform == "darwin":
                subprocess.Popen(["open", "-a", app_name])
            else:
                # Linux - try common desktop environments
                subprocess.Popen([app_name])
            return f"✅ Launched {app_name}"
        except Exception as e:
            return f"❌ Error launching app: {str(e)}"
    
    @staticmethod
    def open_file(file_path: str) -> str:
        """Open a file with default application"""
        try:
            if sys.platform == "win32":
                os.startfile(file_path)
            elif sys.platform == "darwin":
                subprocess.Popen(["open", file_path])
            else:
                subprocess.Popen(["xdg-open", file_path])
            return f"✅ Opened {file_path}"
        except Exception as e:
            return f"❌ Error opening file: {str(e)}"
    
    @staticmethod
    def open_url(url: str) -> str:
        """Open a URL in browser"""
        try:
            if sys.platform == "win32":
                os.startfile(url)
            elif sys.platform == "darwin":
                subprocess.Popen(["open", url])
            else:
                subprocess.Popen(["xdg-open", url])
            return f"✅ Opened {url}"
        except Exception as e:
            return f"❌ Error opening URL: {str(e)}"


class TerminalExecutor:
    """Execute terminal/shell commands"""
    
    def __init__(self, shell: bool = True):
        self.shell = shell
    
    def execute(self, command: str, timeout: int = 30) -> Dict[str, str]:
        """Execute a command and return output"""
        try:
            result = subprocess.run(
                command,
                shell=self.shell,
                capture_output=True,
                text=True,
                timeout=timeout
            )
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
    
    def execute_async(self, command: str):
        """Execute command asynchronously"""
        try:
            if sys.platform == "win32":
                subprocess.Popen(command, shell=True)
            else:
                subprocess.Popen(command, shell=True, start_new_session=True)
            return "✅ Command started"
        except Exception as e:
            return f"❌ Error: {str(e)}"


class AutomationEngine:
    """Main automation engine combining all automation features"""
    
    def __init__(self, config: dict = None):
        self.config = config or {}
        self.files = FileOperations()
        self.apps = AppController()
        self.terminal = TerminalExecutor()
    
    async def execute_tool(self, tool_name: str, params: Dict) -> str:
        """Execute a tool based on name and parameters"""
        try:
            if tool_name == "move_file":
                return self.files.move_file(params['source'], params['destination'])
            elif tool_name == "copy_file":
                return self.files.copy_file(params['source'], params['destination'])
            elif tool_name == "delete_file":
                return self.files.delete_file(params['path'])
            elif tool_name == "create_file":
                return self.files.create_file(params['path'], params.get('content', ''))
            elif tool_name == "read_file":
                return self.files.read_file(params['path'])
            elif tool_name == "list_directory":
                return "\n".join(self.files.list_directory(params.get('path', '.')))
            elif tool_name == "create_directory":
                return self.files.create_directory(params['path'])
            elif tool_name == "launch_app":
                return self.apps.launch_app(params['app'])
            elif tool_name == "open_file":
                return self.apps.open_file(params['path'])
            elif tool_name == "open_url":
                return self.apps.open_url(params['url'])
            elif tool_name == "run_command":
                result = self.terminal.execute(params['command'], params.get('timeout', 30))
                if result['success']:
                    return f"✅ Output:\n{result['stdout']}"
                else:
                    return f"❌ Error: {result['stderr']}"
            else:
                return f"Unknown tool: {tool_name}"
        except Exception as e:
            return f"❌ Error executing {tool_name}: {str(e)}"
    
    def get_available_tools(self) -> List[str]:
        """Get list of available automation tools"""
        return [
            "move_file", "copy_file", "delete_file", "create_file",
            "read_file", "list_directory", "create_directory",
            "launch_app", "open_file", "open_url", "run_command"
        ]