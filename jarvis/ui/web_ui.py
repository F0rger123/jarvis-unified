#!/usr/bin/env python3
"""
Jarvis v6.0-TRON-UI - Full Tron-Style Interface
"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import logging
from flask import Flask, request, jsonify
from flask_cors import CORS

logger = logging.getLogger('jarvis.ui')

# Full Tron UI HTML with all features
TRON_HTML = '''
<!DOCTYPE html>
<html lang="en" data-theme="dark">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>JARVIS AI - TRON Edition</title>
<style>
:root{--accent:#00ffff;--accent-dim:#00ffff33;--accent-glow:#00ffff66;--bg:#0a0a0f;--bg-grid:#0d0d14;--surface:#12121a;--surface-bright:#1a1a25;--text:#e0e0e0;--text-dim:#888}
*{margin:0;padding:0;box-sizing:border-box}
body{font-family:'Orbitron','Segoe UI',system-ui,sans-serif;background:var(--bg);color:var(--text);min-height:100vh;overflow-x:hidden}

/* Grid Background */
body::before{content:'';position:fixed;top:0;left:0;right:0;bottom:0;background:
linear-gradient(var(--accent-dim) 1px,transparent 1px),
linear-gradient(90deg,var(--accent-dim) 1px,transparent 1px),
radial-gradient(ellipse at 50% 0%,var(--accent-glow) 0%,transparent 70%);
background-size:50px 50px,50px 50px,100% 100%;opacity:0.3;pointer-events:none;z-index:-1}

/* Scanlines */
body::after{content:'';position:fixed;top:0;left:0;right:0;bottom:0;background:repeating-linear-gradient(0deg,transparent,transparent 2px,rgba(0,255,255,0.03) 2px,rgba(0,255,255,0.03) 4px);pointer-events:none;z-index:9999}

.container{max-width:1200px;margin:0 auto;padding:20px;display:grid;grid-template-columns:1fr 280px;gap:20px}
@media(max-width:900px){.container{grid-template-columns:1fr}}

.logo{font-size:1.8rem;font-weight:700;color:var(--accent);text-transform:uppercase;letter-spacing:4px;text-shadow:0 0 10px var(--accent),0 0 20px var(--accent-glow)}
.logo span{color:#fff}

.header{display:flex;justify-content:space-between;align-items:center;padding:16px 20px;background:linear-gradient(90deg,var(--surface),var(--surface-bright));border:1px solid var(--accent-dim);border-radius:8px;margin-bottom:16px;grid-column:1/-1}
.header-left{display:flex;align-items:center;gap:16px}
.status{display:flex;align-items:center;gap:8px;font-size:0.85rem;color:var(--text-dim)}
.status-dot{width:8px;height:8px;background:#0f0;border-radius:50%;animation:pulse 2s infinite}
.status-dot.online{background:var(--accent);box-shadow:0 0 10px var(--accent)}
@keyframes pulse{0%,100%{opacity:1}50%{opacity:0.5}}

/* Sidebar */
.sidebar{background:var(--surface);border:1px solid var(--accent-dim);border-radius:8px;padding:16px}
.sidebar h3{color:var(--accent);font-size:0.75rem;text-transform:uppercase;letter-spacing:2px;margin-bottom:12px;border-bottom:1px solid var(--accent-dim);padding-bottom:8px}
.agent-btn{display:block;width:100%;padding:10px 12px;margin:6px 0;background:transparent;border:1px solid var(--accent-dim);border-radius:4px;color:var(--text);font-size:0.85rem;cursor:pointer;text-align:left;transition:all 0.2s}
.agent-btn:hover{background:var(--accent-dim);color:var(--accent)}
.agent-btn.active{background:var(--accent);color:var(--bg);box-shadow:0 0 15px var(--accent-glow)}
.voice-btn{width:100%;padding:12px;margin:8px 0;background:linear-gradient(135deg,var(--accent),#00cccc);border:none;border-radius:4px;color:var(--bg);font-weight:bold;cursor:pointer;font-size:1rem}
.voice-btn:hover{box-shadow:0 0 20px var(--accent)}

/* Chat Area */
.chat-area{background:var(--surface);border:1px solid var(--accent-dim);border-radius:8px;display:flex;flex-direction:column;min-height:500px}
.messages{flex:1;padding:20px;overflow-y:auto;display:flex;flex-direction:column;gap:12px}
.msg{padding:14px 18px;border-radius:8px;max-width:75%;animation:fadeIn 0.3s ease}
.msg.user{background:linear-gradient(135deg,var(--accent-dim),#003333);align-self:flex-end;border:1px solid var(--accent)}
.msg.assistant{background:var(--surface-bright);border:1px solid var(--accent-dim)}
.msg.system{background:#1a1a0a;border:1px solid #ffaa00;color:#ffaa00;font-size:0.85rem}
@keyframes fadeIn{from{opacity:0;transform:translateY(10px)}to{opacity:1;transform:translateY(0)}}

/* Input */
.input-area{display:flex;gap:10px;padding:16px;border-top:1px solid var(--accent-dim)}
.input-area input{flex:1;padding:14px 18px;background:var(--bg);border:1px solid var(--accent-dim);border-radius:4px;color:var(--text);font-size:1rem}
.input-area input:focus{outline:none;border-color:var(--accent);box-shadow:0 0 10px var(--accent-dim)}
.input-area button{padding:14px 28px;background:linear-gradient(135deg,var(--accent),#00cccc);border:none;border-radius:4px;color:var(--bg);font-weight:bold;cursor:pointer;font-size:1rem;transition:all 0.2s}
.input-area button:hover{box-shadow:0 0 20px var(--accent)}

/* Brain Visualization */
.brain-viz{height:200px;background:var(--bg);border:1px solid var(--accent-dim);border-radius:4px;margin:12px 0;position:relative;overflow:hidden}
.brain-viz canvas{width:100%;height:100%}

/* Settings */
.settings-panel{background:var(--surface);border:1px solid var(--accent-dim);border-radius:8px;padding:16px;margin-top:16px;display:none}
.settings-panel.show{display:block}
.setting-row{display:flex;justify-content:space-between;align-items:center;padding:10px 0;border-bottom:1px solid #222}
.setting-row input[type="text"],.setting-row input[type="password"]{width:200px;padding:8px;background:var(--bg);border:1px solid #333;border-radius:4px;color:var(--text)}
.setting-row select{padding:8px;background:var(--bg);border:1px solid #333;border-radius:4px;color:var(--text)}

/* Stats */
.stats{display:grid;grid-template-columns:1fr 1fr;gap:8px;margin-top:12px}
.stat-box{background:var(--bg);padding:12px;border-radius:4px;text-align:center}
.stat-box .value{font-size:1.5rem;color:var(--accent);font-weight:bold}
.stat-box .label{font-size:0.7rem;color:var(--text-dim);text-transform:uppercase}

/* Scrollbar */
::-webkit-scrollbar{width:8px}
::-webkit-scrollbar-track{background:var(--bg)}
::-webkit-scrollbar-thumb{background:var(--accent-dim);border-radius:4px}
::-webkit-scrollbar-thumb:hover{background:var(--accent)}
</style>
</head>
<body>
<div class="container">
<div class="header">
<div class="header-left">
<div class="logo"><span>JARVIS</span> AI</div>
<div class="status"><div class="status-dot online"></div><span>ONLINE</span></div>
</div>
<div style="display:flex;gap:10px">
<button class="agent-btn" style="width:auto" onclick="showBrain()">🧠 Brain</button>
<button class="agent-btn" style="width:auto" onclick="showSettings()">⚙️</button>
</div>
</div>

<div class="chat-area">
<div class="messages" id="messages">
<div class="msg assistant">🤖 <strong>JARVIS v6.0</strong> initialized.<br><br>I'm ready. What do you need?</div>
</div>
<div class="input-area">
<input type="text" id="input" placeholder="Ask anything..." onkeypress="if(event.key==='Enter')send()">
<button onclick="send()">▸ SEND</button>
</div>
</div>

<div class="sidebar">
<h3>Agents</h3>
<button class="agent-btn active" onclick="useAgent('general')">💬 General</button>
<button class="agent-btn" onclick="useAgent('research')">📚 Research</button>
<button class="agent-btn" onclick="useAgent('coding')">💻 Coding</button>
<button class="agent-btn" onclick="useAgent('stock')">📈 Stocks</button>
<button class="agent-btn" onclick="useAgent('marketing')">📣 Marketing</button>
<button class="agent-btn" onclick="useAgent('fitness')">💪 Fitness</button>
<button class="agent-btn" onclick="useAgent('travel')">✈️ Travel</button>
<button class="agent-btn" onclick="useAgent('food')">🍳 Food</button>

<h3>Voice</h3>
<button class="voice-btn" id="voiceBtn" onclick="toggleVoice()">🎤 Enable Voice</button>

<h3>Stats</h3>
<div class="stats">
<div class="stat-box"><div class="value" id="msgCount">0</div><div class="label">Messages</div></div>
<div class="stat-box"><div class="value" id="rating">-</div><div class="label">Rating</div></div>
</div>

<div class="brain-viz"><canvas id="brainCanvas"></canvas></div>
</div>

<div class="settings-panel" id="settingsPanel">
<h3>Settings</h3>
<div class="setting-row"><span>Tone</span><select id="tone"><option>Professional</option><option>Helpful</option><option>Sassy</option></select></div>
<div class="setting-row"><span>Model</span><select id="model"><option>gemini-3.1-flash-lite</option><option>gemma-4-9b-it</option></select></div>
<div class="setting-row"><span>Code Brain</span><input type="checkbox" id="codeBrain" checked></div>
<div class="setting-row"><span>API Key</span><input type="password" id="apiKey" placeholder="Enter API key..."></div>
<button class="agent-btn" onclick="saveSettings()">Save Settings</button>
</div>
</div>
</div>

<script>
let currentAgent = 'general';
let voiceEnabled = false;
let msgCount = 0;

function send(){
  const input = document.getElementById('input');
  const msg = input.value.trim();
  if(!msg) return;
  
  addMsg(msg, 'user');
  input.value = '';
  msgCount++;
  document.getElementById('msgCount').innerText = msgCount;
  
  // Show typing
  const typing = document.createElement('div');
  typing.className = 'msg assistant';
  typing.id = 'typing';
  typing.innerHTML = '<em>Processing...</em>';
  document.getElementById('messages').appendChild(typing);
  
  fetch('/api/chat', {
    method: 'POST',
    headers: {'Content-Type': 'application/json'},
    body: JSON.stringify({message: '[' + currentAgent + '] ' + msg})
  })
  .then(r => r.json())
  .then(d => {
    document.getElementById('typing').remove();
    addMsg(d.response || 'No response', 'assistant');
  })
  .catch(e => {
    document.getElementById('typing').remove();
    addMsg('Error: ' + e.message, 'assistant');
  });
}

function addMsg(text, cls){
  const m = document.createElement('div');
  m.className = 'msg ' + cls;
  // Convert line breaks
  m.innerHTML = text.replace(/\\n/g, '<br>');
  document.getElementById('messages').appendChild(m);
  m.scrollIntoView({behavior: 'smooth'});
}

function useAgent(agent){
  currentAgent = agent;
  document.querySelectorAll('.agent-btn').forEach(b => b.classList.remove('active'));
  event.target.classList.add('active');
}

function toggleVoice(){
  voiceEnabled = !voiceEnabled;
  document.getElementById('voiceBtn').innerText = voiceEnabled ? '🎤 Voice ON' : '🎤 Enable Voice';
  document.getElementById('voiceBtn').style.background = voiceEnabled ? 'var(--accent)' : '';
}

function showSettings(){
  document.getElementById('settingsPanel').classList.toggle('show');
}

function saveSettings(){
  const key = document.getElementById('apiKey').value;
  if(key){
    fetch('/api/settings', {
      method: 'PUT',
      headers: {'Content-Type': 'application/json'},
      body: JSON.stringify({gemini_api_key: key})
    }).then(() => alert('Settings saved!')).catch(e => alert('Error: ' + e));
  }
}

// Brain visualization
const canvas = document.getElementById('brainCanvas');
const ctx = canvas.getContext('2d');
const nodes = [
  {x: 140, y: 100, label: 'CORE', active: true},
  {x: 80, y: 50, label: 'AI'},
  {x: 200, y: 50, label: 'MEM'},
  {x: 80, y: 150, label: 'VOICE'},
  {x: 200, y: 150, label: 'WEB'}
];
function drawBrain(){
  ctx.fillStyle = '#0a0a0f';
  ctx.fillRect(0, 0, 280, 200);
  
  // Connections
  ctx.strokeStyle = '#00ffff33';
  nodes.forEach(n => {
    nodes.forEach(m => {
      if(n !== m){
        ctx.beginPath();
        ctx.moveTo(n.x, n.y);
        ctx.lineTo(m.x, m.y);
        ctx.stroke();
      }
    });
  });
  
  // Nodes
  nodes.forEach(n => {
    ctx.beginPath();
    ctx.arc(n.x, n.y, 15, 0, Math.PI * 2);
    ctx.fillStyle = n.active ? '#00ffff' : '#00ffff66';
    ctx.fill();
    ctx.fillStyle = '#00ffff';
    ctx.font = '10px Orbitron';
    ctx.textAlign = 'center';
    ctx.fillText(n.label, n.x, n.y - 22);
  });
  
  requestAnimationFrame(drawBrain);
}
drawBrain();
</script>
</body>
</html>
'''

class JarvisTronUI:
    """Tron-Style Jarvis Interface"""
    
    def __init__(self, jarvis_instance, config):
        self.jarvis = jarvis_instance
        self.config = config
        self.app = None
        self._setup_routes()
    
    def _setup_routes(self):
        self.app = Flask(__name__)
        CORS(self.app)
        
        @self.app.route('/')
        def index():
            return TRON_HTML
        
        @self.app.route('/api/chat', methods=['POST'])
        def chat():
            import asyncio
            try:
                data = request.get_json()
                message = data.get('message', '') if data else ''
                
                loop = asyncio.new_event_loop()
                asyncio.set_event_loop(loop)
                response = loop.run_until_complete(self.jarvis.process(message))
                loop.close()
                
                return jsonify({'response': response})
            except Exception as e:
                logger.error(f"Chat error: {e}")
                return jsonify({'response': f'Error: {str(e)}'}), 500
        
        @self.app.route('/api/settings', methods=['GET'])
        def get_settings():
            return jsonify(self.config)
        
        @self.app.route('/api/settings', methods=['PUT'])
        def update_settings():
            try:
                data = request.get_json()
                for key, value in data.items():
                    self.config[key] = value
                return jsonify({'status': 'ok'})
            except Exception as e:
                return jsonify({'error': str(e)}), 500
        
        @self.app.route('/api/dashboard')
        def dashboard():
            if hasattr(self.jarvis, 'get_dashboard'):
                return jsonify(self.jarvis.get_dashboard())
            return jsonify({'nodes': [], 'links': [], 'stats': {}})
    
    def run(self, host='0.0.0.0', port=5000):
        logger.info(f"Starting JARVIS TRON UI on http://{host}:{port}")
        import socket
        # Find available port
        test_port = port
        while test_port < port + 10:
            try:
                sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                sock.settimeout(1)
                result = sock.connect_ex((host, test_port))
                sock.close()
                if result != 0:
                    break
            except:
                break
            test_port += 1
        
        self.app.run(host=host, port=test_port, debug=False)

def create_ui(jarvis, config):
    return JarvisTronUI(jarvis, config)