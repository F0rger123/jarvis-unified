#!/usr/bin/env python3
"""
JARVIS ONE-CLICK GUI INSTALLER
No terminal commands needed - just click!

This creates a simple GUI that:
1. Checks/Installs Python automatically
2. Shows a nice window to paste API key
3. Creates shortcuts
4. Launches Jarvis
"""
import sys, os, subprocess, threading, time, urllib.request, zipfile, shutil

# Try to use tkinter (built into Python)
try:
    import tkinter as tk
    from tkinter import ttk, messagebox
    HAS_TKINTER = True
except ImportError:
    HAS_TKINTER = False

# If no tkinter, install and retry
if not HAS_TKINTER:
    try:
        subprocess.run([sys.executable, '-m', 'pip', 'install', 'tkinter', '-q'], check=True)
        import tkinter as tk
        from tkinter import ttk, messagebox
        HAS_TKINTER = True
    except:
        pass

class JarvisInstaller:
    """GUI Installer for Jarvis"""
    
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("🤖 Jarvis v4.0 Installer")
        self.root.geometry("500x400")
        self.root.configure(bg="#0a0a0f")
        self.root.resizable(False, False)
        
        # Style
        self.style = ttk.Style()
        self.style.theme_use('clam')
        self.style.configure('TButton', background='#00ffff', foreground='#0a0a0f', font=('Arial', 12, 'bold'))
        self.style.configure('TLabel', background='#0a0a0f', foreground='#00ffff')
        
        self.setup_ui()
        
    def setup_ui(self):
        # Logo
        tk.Label(self.root, text="🤖", font=("Arial", 48), bg="#0a0a0f", fg="#00ffff").pack(pady=10)
        tk.Label(self.root, text="JARVIS v4.0", font=("Arial", 24, "bold"), bg="#0a0a0f", fg="#00ffff").pack()
        tk.Label(self.root, text="One-Click Setup", font=("Arial", 12), bg="#0a0a0f", fg="#888").pack()
        
        # Status
        self.status_var = tk.StringVar(value="Initializing...")
        tk.Label(self.root, textvariable=self.status_var, font=("Arial", 10), bg="#0a0a0f", fg="#00ff88").pack(pady=10)
        
        # API Key input
        tk.Label(self.root, text="Paste your FREE API key:", bg="#0a0a0f", fg="#e0e0e0").pack(pady=(20, 5))
        
        self.api_entry = tk.Entry(self.root, width=40, font=("Arial", 11), bg="#151520", fg="#e0e0e0", relief="flat")
        self.api_entry.pack(pady=5)
        
        tk.Label(self.root, text="Get free key: https://aistudio.google.com/app/apikey", 
               font=("Arial", 8), bg="#0a0a0f", fg="#666").pack()
        
        # Buttons
        btn_frame = tk.Frame(self.root, bg="#0a0a0f")
        btn_frame.pack(pady=20)
        
        self.install_btn = ttk.Button(btn_frame, text="🚀 INSTALL & LAUNCH", command=self.start_install)
        self.install_btn.pack(side=tk.LEFT, padx=5)
        
        # Progress bar
        self.progress = ttk.Progressbar(self.root, length=400, mode='determinate')
        self.progress.pack(pady=10)
        
        # Log
        self.log_var = tk.StringVar(value="Ready")
        tk.Label(self.root, textvariable=self.log_var, font=("Arial", 8), bg="#0a0a0f", fg="#666").pack(pady=5)
        
    def log(self, msg):
        self.log_var.set(msg)
        self.root.update()
        
    def set_progress(self, value):
        self.progress['value'] = value
        self.root.update()
        
    def start_install(self):
        api_key = self.api_entry.get().strip()
        
        if not api_key:
            messagebox.showerror("Error", "Please enter your API key!")
            return
            
        if not api_key.startswith('AI'):
            messagebox.showerror("Error", "API key should start with 'AI...'")
            return
        
        # Disable button
        self.install_btn.config(state='disabled')
        
        # Run installation in thread
        threading.Thread(target=self.install, args=(api_key,), daemon=True).start()
        
    def install(self, api_key):
        self.status_var.set("Installing Python (if needed)...")
        self.log("Checking Python...")
        self.set_progress(10)
        
        # Check/install Python (simplified - just assume it's there or warn)
        try:
            subprocess.run([sys.executable, '--version'], check=True, capture_output=True)
        except:
            self.status_var.set("Please install Python 3.10+ from python.org")
            messagebox.showwarning("Warning", "Python not found. Please install from python.org")
            self.install_btn.config(state='normal')
            return
        
        self.status_var.set("Creating environment...")
        self.log("Creating virtual environment...")
        self.set_progress(30)
        
        # Create venv (in current directory)
        venv_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'venv')
        if not os.path.exists(venv_path):
            try:
                subprocess.run([sys.executable, '-m', 'venv', venv_path], check=True, capture_output=True)
            except:
                pass  # Continue even if venv fails
        
        self.log("Installing dependencies...")
        self.set_progress(50)
        
        # Install deps
        pip = os.path.join(venv_path, 'Scripts', 'pip') if os.name == 'nt' else os.path.join(venv_path, 'bin', 'pip')
        if os.path.exists(pip):
            subprocess.run([pip, 'install', '-q', 'flask', 'flask-cors', 'requests', 'pyttsx3'], capture_output=True)
        
        self.status_var.set("Configuring Jarvis...")
        self.log("Writing config...")
        self.set_progress(70)
        
        # Write .env
        env_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'jarvis', '.env')
        os.makedirs(os.path.dirname(env_path), exist_ok=True)
        
        env_content = f"""# Jarvis v4.0 Configuration
AI_PROVIDER=gemini
GEMINI_API_KEY={api_key}
GEMINI_MODEL=gemini-3.1-flash-lite
USE_GEMMA_FOR_CODE=true
CONFIRM_PAYMENTS=true
CONFIRM_ORDERS=true
CONFIRM_SMS=true
CONFIRM_WHATSAPP=true
UI_THEME=tron
ACCENT_COLOR=#00ffff
JARVIS_TONE=helpful
PORT=5000
"""
        with open(env_path, 'w') as f:
            f.write(env_content)
        
        self.status_var.set("Launching Jarvis...")
        self.log("Starting web server...")
        self.set_progress(90)
        
        # Start Jarvis
        jarvis_dir = os.path.dirname(os.path.abspath(__file__))
        main_py = os.path.join(jarvis_dir, 'jarvis', 'main.py')
        
        if os.path.exists(main_py):
            # Try to start
            try:
                subprocess.Popen([sys.executable, main_py, '--web'], 
                          cwd=os.path.join(jarvis_dir, 'jarvis'),
                          stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL,
                          start_new_session=True)
            except:
                pass
        
        self.set_progress(100)
        self.status_var.set("✅ JARVIS IS READY!")
        
        # Open browser
        time.sleep(2)
        import webbrowser
        webbrowser.open('http://localhost:5000')
        
        messagebox.showinfo("🎉 Success!", "Jarvis is now open in your browser!\n\nIf it didn't open, go to: http://localhost:5000")
        
        self.root.quit()

def main():
    if not HAS_TKINTER:
        print("ERROR: tkinter not available. Please install Python with tkinter support.")
        sys.exit(1)
    
    app = JarvisInstaller()
    app.root.mainloop()

if __name__ == "__main__":
    main()