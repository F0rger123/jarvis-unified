#!/usr/bin/env python3
"""
JARVIS v4.0.2 - GUI INSTALLER WITH PROGRESS
Shows real-time progress in a GUI window
"""
import sys
import os
import subprocess
import threading
import time
import urllib.request
import urllib.error

# Try to use tkinter
try:
    import tkinter as tk
    from tkinter import ttk, messagebox
    HAS_TK = True
except:
    HAS_TK = False

class JarvisGUI:
    def __init__(self):
        if not HAS_TK:
            print("ERROR: tkinter not available")
            sys.exit(1)
        
        self.root = tk.Tk()
        self.root.title("🤖 Jarvis v4.0.2 Installer")
        self.root.geometry("450x350")
        self.root.configure(bg="#0a0a0f")
        self.root.resizable(False, False)
        
        self.status_colors = {
            'pending': '#666',
            'running': '#ffaa00', 
            'success': '#00ff88',
            'error': '#ff4444'
        }
        
        self.setup_ui()
        self.run_checks()
        
    def setup_ui(self):
        # Title
        tk.Label(self.root, text="🤖", font=("Arial", 36), bg="#0a0a0f", fg="#00ffff").pack(pady=5)
        tk.Label(self.root, text="JARVIS v4.0.2", font=("Arial", 18, "bold"), bg="#0a0a0f", fg="#00ffff").pack()
        tk.Label(self.root, text="One-Click Installer", font=("Arial", 10), bg="#0a0a0f", fg="#666").pack()
        
        # Steps
        self.steps = {}
        step_frame = tk.Frame(self.root, bg="#0a0a0f")
        step_frame.pack(pady=20, fill=tk.BOTH, expand=True, padx=20)
        
        steps = [
            ("Python", "Checking Python..."),
            ("Venv", "Creating environment..."),
            ("Deps", "Installing dependencies..."),
            ("Test", "Testing imports..."),
            ("Config", "Configuring..."),
            ("Server", "Starting server..."),
        ]
        
        for name, label in steps:
            row = tk.Frame(step_frame, bg="#0a0a0f")
            row.pack(fill=tk.X, pady=3)
            
            indicator = tk.Label(row, text="⏳", font=("Arial", 12), bg="#0a0a0f", fg="#666", width=3)
            indicator.pack(side=tk.LEFT)
            
            text = tk.Label(row, text=label, font=("Arial", 10), bg="#0a0a0f", fg="#888", anchor=tk.W)
            text.pack(side=tk.LEFT, fill=tk.X, expand=True)
            
            self.steps[name] = {"indicator": indicator, "text": text, "label": label}
        
        # Log area
        self.log_text = tk.Text(self.root, height=6, bg="#151520", fg="#00ff88", 
                          font=("Courier", 8), relief=tk.FLAT, state=tk.DISABLED)
        self.log_text.pack(fill=tk.BOTH, expand=True, padx=20, pady=(0, 10))
        
    def log(self, msg):
        self.log_text.config(state=tk.NORMAL)
        self.log_text.insert(tk.END, msg + "\n")
        self.log_text.see(tk.END)
        self.log_text.config(state=tk.DISABLED)
        self.root.update()
        
    def set_step(self, name, status, detail=None):
        if name not in self.steps:
            return
            
        step = self.steps[name]
        color = self.status_colors.get(status, '#666')
        
        icon = {'pending': '⏳', 'running': '🔄', 'success': '✅', 'error': '❌'}.get(status, '⏳')
        step["indicator"].config(fg=color, text=icon)
        step["text"].config(fg=color)
        
        if detail:
            step["text"].config(text=detail)
        
        self.root.update()
        
    def run_checks(self):
        """Run all installation steps"""
        self.log("Starting Jarvis installation...")
        
        # Step 1: Python
        self.set_step("Python", "running")
        try:
            result = subprocess.run([sys.executable, '--version'], capture_output=True, text=True, timeout=5)
            ver = result.stdout.strip() if result.stdout else result.stderr.strip()
            self.log(f"Python: {ver}")
            self.set_step("Python", "success", f"Python: {ver}")
        except Exception as e:
            self.set_step("Python", "error", f"Python not found!")
            self.log(f"ERROR: {e}")
            messagebox.showerror("Error", f"Python not found: {e}")
            return
            
        # Step 2: Venv
        self.set_step("Venv", "running")
        venv_path = "venv"
        try:
            if not os.path.exists(venv_path):
                subprocess.run([sys.executable, '-m', 'venv', venv_path], capture_output=True, timeout=60)
                self.log("Created venv")
            else:
                self.log("Using existing venv")
            self.set_step("Venv", "success")
        except Exception as e:
            self.set_step("Venv", "error")
            self.log(f"ERROR: {e}")
            
        # Step 3: Dependencies
        self.set_step("Deps", "running")
        pip = os.path.join(venv_path, "Scripts", "pip") if os.name == 'nt' else os.path.join(venv_path, "bin", "pip")
        try:
            subprocess.run([pip, 'install', '-q', 'flask', 'flask-cors', 'requests', 'pyttsx3'], 
                       capture_output=True, timeout=120)
            self.log("Installed: flask, flask-cors, requests, pyttsx3")
            self.set_step("Deps", "success")
        except Exception as e:
            self.set_step("Deps", "error")
            self.log(f"ERROR: {e}")
            
        # Step 4: Test imports
        self.set_step("Test", "running")
        try:
            sys.path.insert(0, 'jarvis')
            from core.jarvis import JarvisConfig
            self.log("Core imports: OK")
            self.set_step("Test", "success")
        except Exception as e:
            self.set_step("Test", "error")
            self.log(f"ERROR importing: {e}")
            messagebox.showerror("Import Error", str(e))
            
        # Step 5: Config
        self.set_step("Config", "running")
        env_path = os.path.join("jarvis", ".env")
        try:
            os.makedirs("jarvis", exist_ok=True)
            if not os.path.exists(env_path):
                with open(env_path, 'w') as f:
                    f.write("GEMINI_API_KEY=\nGEMINI_MODEL=gemini-3.1-flash-lite\n")
                self.log("Created .env")
            self.set_step("Config", "success")
        except Exception as e:
            self.set_step("Config", "error")
            self.log(f"ERROR: {e}")
            
        # Step 6: Start server
        self.set_step("Server", "running")
        self.log("Starting server...")
        
        try:
            # Start in thread
            def start_server():
                os.chdir("jarvis")
                subprocess.run([sys.executable, "main.py", "--web"])
            
            thread = threading.Thread(target=start_server, daemon=True)
            thread.start()
            
            # Wait for server with progress
            for i in range(15):
                time.sleep(1)
                self.log(f"Waiting... {i+1}/15")
                self.root.update()
                
                try:
                    urllib.request.urlopen('http://localhost:5000', timeout=2)
                    self.log("Server is UP!")
                    self.set_step("Server", "success", "Server running!")
                    break
                except:
                    continue
            else:
                self.set_step("Server", "error", "Server not responding!")
                self.log("WARNING: Server may not have started")
                
        except Exception as e:
            self.set_step("Server", "error")
            self.log(f"ERROR: {e}")
            
        # Done
        self.log("\n✅ Installation complete!")
        self.log("Open http://localhost:5000 in your browser")
        
        # Open browser
        try:
            import webbrowser
            webbrowser.open('http://localhost:5000')
        except:
            pass
            
        messagebox.showinfo("Ready!", "Jarvis is running at http://localhost:5000")

def main():
    if HAS_TK:
        app = JarvisGUI()
        app.root.mainloop()
    else:
        print("Please install Python with tkinter: python.org")

if __name__ == "__main__":
    main()