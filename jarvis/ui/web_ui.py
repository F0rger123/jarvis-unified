#!/usr/bin/env python3
"""
Jarvis v5.0-SIMPLE - TRON-Style UI
Fixes for v5.0 - Simplified for easy install
"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import logging
logger = logging.getLogger('jarvis.ui')

HTML_TEMPLATE = '''
<!DOCTYPE html>
<html lang="en" data-theme="dark">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Jarvis AI</title>
<style>
:root{--accent:#00ffff;--accent-dim:#00ffff22;--bg:#0a0a0f;--surface:#151520;--text:#e0e0e0}
*{margin:0;padding:0;box-sizing:border-box}
body{font-family:'Segoe UI',system-ui,sans-serif;background:var(--bg);color:var(--text);min-height:100vh}
.container{max-width:800px;margin:0 auto;padding:16px}
.header{display:flex;justify-content:space-between;align-items:center;padding:16px;border-bottom:1px solid var(--accent-dim)}
.logo{font-size:1.5rem;font-weight:700;color:var(--accent);text-transform:uppercase;letter-spacing:3px}
.messages{min-height:300px;background:var(--surface);border-radius:8px;padding:16px;margin:16px 0;overflow-y:auto}
.msg{padding:12px;margin:8px 0;border-radius:8px;max-width:80%}
.msg.user{background:var(--accent-dim);margin-left:auto}
.msg.assistant{background:#1a1a25}
.input-area{display:flex;gap:8px}
.input-area input{flex:1;padding:12px;border-radius:8px;border:1px solid #333;background:var(--surface);color:var(--text)}
.input-area button{padding:12px 24px;background:var(--accent);border:none;border-radius:8px;color:var(--bg);font-weight:bold;cursor:pointer}
.btn{padding:8px 16px;background:var(--accent);border:none;border-radius:8px;color:var(--bg);font-weight:bold;cursor:pointer}
.settings{background:var(--surface);padding:16px;border-radius:8px;margin:16px 0}
.setting-row{display:flex;justify-content:space-between;padding:8px 0;border-bottom:1px solid #333}
.agent{display:inline-block;padding:8px 16px;background:var(--surface);border-radius:20px;margin:4px;font-size:0.8rem;cursor:pointer;border:1px solid var(--accent-dim)}
.agent:hover{background:var(--accent-dim)}
.toggle{padding:12px;background:var(--surface);border-radius:8px;margin:8px 0;cursor:pointer}
</style>
</head>
<body>
<div class="container">
<div class="header">
<div class="logo">JARVIS</div>
<div id="status">● READY</div>
</div>
<div class="agents" id="agents"></div>
<div class="messages" id="messages">
<div class="msg assistant">🤖 Jarvis v5.0 ready! Ask me anything.</div>
</div>
<div class="input-area">
<button id="modeBtn" onclick="toggleMode()">⌨️</button>
<input type="text" id="input" placeholder="Ask anything..." onkeypress="if(event.key==='Enter')send()">
<button onclick="send()">SEND</button>
</div>
<div class="toggle" onclick="showSettings()">⚙️ Settings</div>
<div id="settings" class="settings" style="display:none">
<div class="setting-row"><span>Tone</span><select id="tone"><option>Professional</option><option>Helpful</option></select></div>
<div class="setting-row"><span>API Key</span><input type="password" id="apiKey" placeholder="Enter API key..."></div>
<div class="setting-row"><button class="btn" onclick="saveSettings()">Save</button></div>
</div>
</div>
<script>
let mode='text';
function send(){
  const i=document.getElementById('input');
  const m=i.value.trim();
  if(!m)return;
  addMsg(m,'user');
  i.value='';
  fetch('/api/chat',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({message:m})})
    .then(r=>r.json()).then(d=>addMsg(d.response,'assistant')).catch(e=>addMsg('Error: '+e,'assistant'));
}
function addMsg(t,c){
  const m=document.createElement('div');
  m.className='msg '+c;
  m.innerHTML=t;
  document.getElementById('messages').appendChild(m);
  m.scrollIntoView();
}
function toggleMode(){
  mode=mode==='text'?'voice':'text';
  document.getElementById('modeBtn').textContent=mode==='text'?'⌨️':'🎤';
  document.getElementById('status').textContent=mode.toUpperCase()+' MODE';
}
function showSettings(){
  document.getElementById('settings').style.display=document.getElementById('settings').style.display==='none'?'block':'none';
}
function saveSettings(){
  const k=document.getElementById('apiKey').value;
  if(k){localStorage.setItem('jarvis_apikey',k);alert('Saved!');}
}
</script>
</body>
</html>
'''

class JarvisTronUI:
    """Simple Tron-style web interface"""
    
    def __init__(self, jarvis_instance, config):
        self.jarvis = jarvis_instance
        self.config = config
        self.app = None
        self._setup_routes()
    
    def _setup_routes(self):
        from flask import Flask, request, jsonify
        from flask_cors import CORS
        
        self.app = Flask(__name__)
        CORS(self.app)
        
        @self.app.route('/')
        def index():
            return HTML_TEMPLATE
        
        @self.app.route('/api/chat', methods=['POST'])
        def chat():
            import asyncio
            message = request.json.get('message', '')
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            response = loop.run_until_complete(self.jarvis.process(message))
            loop.close()
            return jsonify({'response': response})
        
        @self.app.route('/api/settings')
        def get_settings():
            return jsonify(self.config)
        
        @self.app.route('/api/dashboard')
        def dashboard():
            if hasattr(self.jarvis, 'get_dashboard'):
                return jsonify(self.jarvis.get_dashboard())
            return jsonify({'nodes':[],'links':[]})
    
    def run(self, host='0.0.0.0', port=5000):
        logger.info(f"Starting Jarvis UI on http://{host}:{port}")
        # Find available port
        import socket
        while port < 5010:
            try:
                sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                sock.settimeout(1)
                result = sock.connect_ex((host, port))
                sock.close()
                if result != 0:
                    break  # Port is free
            except:
                pass
            port += 1
        
        self.app.run(host=host, port=port, debug=False)

def create_ui(jarvis, config):
    return JarvisTronUI(jarvis, config)