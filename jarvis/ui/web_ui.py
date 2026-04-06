#!/usr/bin/env python3
"""
JARVIS v7.0-TRUE-MERGE - Combined from multiple repos
- UI: Mark-XXXV inspired Tron style + vierisid-jarvis styling
- Agents: From danilofalcao/jarvis concept + vierisid-jarvis agent system  
- Brain Viz:vierisid-jarvis node graph adaptated
- Voice: OpenJarvis voice handling concept
- Automation: taskmaster file operations
- Memory: isair-jarvis SQLite memory
"""
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import logging
from flask import Flask, request, jsonify
from flask_cors import CORS

logger = logging.getLogger('jarvis.ui')

# Full Tron UI HTML - merged from Mark-XXXV and vierisid styles
TRON_UI = '''
<!DOCTYPE html>
<html lang="en" data-theme="dark">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>JARVIS AI - TRUE MERGE</title>
<link href="https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700&family=Share+Tech+Mono&display=swap" rel="stylesheet">
<style>
:root{--bg:#0a0a0f;--surface:#12121a;--surface-bright:#1a1a25;--accent:#00d4ff;--accent-dim:#00d4ff22;--accent-glow:#00d4ff66;--text:#e0e0e0;--text-dim:#888;--success:#00ff88;--warning:#ffaa00;--error:#ff4444;--panel:#010c10}
*{margin:0;padding:0;box-sizing:border-box}
body{font-family:'Share Tech Mono','Segoe UI',monospace;background:var(--bg);color:var(--text);min-height:100vh;overflow-x:hidden}

/* Grid Background - Mark-XXXV style */
body::before{content:'';position:fixed;top:0;left:0;right:0;bottom:0;background:linear-gradient(var(--accent-dim)1px,transparent 1px),linear-gradient(90deg,var(--accent-dim)1px,transparent 1px),radial-gradient(ellipse at 50% 0%,var(--accent-glow)0%,transparent 70%);background-size:40px 40px,40px 40px,100% 100%;opacity:0.4;pointer-events:none;z-index:-1}

/* Scanlines - Mark-XXXV effect */
body::after{content:'';position:fixed;top:0;left:0;right:0;bottom:0;background:repeating-linear-gradient(0deg,transparent,transparent 2px,rgba(0,212,255,0.03)2px,rgba(0,212,255,0.03)4px);pointer-events:none;z-index:9999}

.container{max-width:1400px;margin:0 auto;padding:20px;display:grid;grid-template-columns:260px 1fr 300px;gap:16px}
@media(max-width:1100px){.container{grid-template-columns:1fr}}

.header{grid-column:1/-1;display:flex;justify-content:space-between;align-items:center;padding:16px 24px;background:linear-gradient(90deg,var(--surface),var(--surface-bright));border:1px solid var(--accent-dim);border-radius:8px;box-shadow:0 0 20px var(--accent-glow)}
.logo{font-family:'Orbitron',sans-serif;font-size:1.8rem;font-weight:700;color:var(--accent);text-transform:uppercase;letter-spacing:4px;text-shadow:0 0 10px var(--accent),0 0 30px var(--accent-glow)}
.logo span{color:#fff}
.status{display:flex;align-items:center;gap:10px;font-size:0.8rem;color:var(--text-dim)}
.status-dot{width:10px;height:10px;border-radius:50%;background:var(--accent);box-shadow:0 0 10px var(--accent);animation:pulse 2s infinite}
@keyframes pulse{0%,100%{opacity:1}50%{opacity:0.5}}

.sidebar{background:var(--surface);border:1px solid var(--accent-dim);border-radius:8px;padding:16px}
.sidebar h3{color:var(--accent);font-size:0.7rem;text-transform:uppercase;letter-spacing:2px;margin:16px 0 10px 0;border-bottom:1px solid var(--accent-dim);padding-bottom:8px}

.agent-btn{display:block;width:100%;padding:10px 14px;margin:6px 0;background:transparent;border:1px solid var(--accent-dim);border-radius:4px;color:var(--text);font-size:0.85rem;cursor:pointer;text-align:left;transition:all 0.2s;font-family:inherit}
.agent-btn:hover{background:var(--accent-dim);color:var(--accent);transform:translateX(4px)}
.agent-btn.active{background:var(--accent);color:var(--bg);box-shadow:0 0 15px var(--accent-glow)}

.voice-btn{width:100%;padding:14px;margin:12px 0;background:linear-gradient(135deg,var(--accent),#00cccc);border:none;border-radius:4px;color:var(--bg);font-weight:bold;cursor:pointer;font-size:1rem;font-family:inherit}
.voice-btn:hover{box-shadow:0 0 25px var(--accent)}

.chat-area{background:var(--surface);border:1px solid var(--accent-dim);border-radius:8px;display:flex;flex-direction:column;min-height:600px}
.messages{flex:1;padding:20px;overflow-y:auto;display:flex;flex-direction:column;gap:10px}
.msg{padding:14px 20px;border-radius:8px;max-width:70%;animation:fadeIn 0.3s ease;font-size:0.95rem;line-height:1.5}
.msg.user{background:linear-gradient(135deg,var(--accent-dim),#003344);align-self:flex-end;border:1px solid var(--accent)}
.msg.assistant{background:var(--surface-bright);border:1px solid var(--accent-dim)}
.msg.system{background:rgba(255,170,0,0.1);border:1px solid var(--warning);color:var(--warning);font-size:0.85rem}
@keyframes fadeIn{from{opacity:0;transform:translateY(10px)}to{opacity:1;transform:translateY(0)}}

.input-area{display:flex;gap:12px;padding:16px;border-top:1px solid var(--accent-dim)}
.input-area input{flex:1;padding:14px 18px;background:var(--bg);border:1px solid var(--accent-dim);border-radius:4px;color:var(--text);font-size:1rem;font-family:inherit}
.input-area input:focus{outline:none;border-color:var(--accent);box-shadow:0 0 15px var(--accent-dim)}
.input-area button{padding:14px 32px;background:linear-gradient(135deg,var(--accent),#00cccc);border:none;border-radius:4px;color:var(--bg);font-weight:bold;cursor:pointer;font-size:1rem;font-family:inherit}
.input-area button:hover{box-shadow:0 0 25px var(--accent)}

.right-panel{background:var(--surface);border:1px solid var(--accent-dim);border-radius:8px;padding:16px}
.brain-viz{height:220px;background:var(--bg);border:1px solid var(--accent-dim);border-radius:4px;margin:12px 0;position:relative;overflow:hidden}
.brain-viz canvas{width:100%;height:100%}

.stats{background:var(--bg);padding:12px;border-radius:4px;margin:10px 0}
.stat-row{display:flex;justify-content:space-between;padding:6px 0;border-bottom:1px solid #222}
.stat-row:last-child{border:none}
.stat-value{color:var(--accent);font-weight:bold}
.stat-label{color:var(--text-dim);font-size:0.8rem}

.settings-panel{display:none;padding:12px 0}
.settings-panel.show{display:block}
.setting-row{display:flex;justify-content:space-between;align-items:center;padding:10px 0;border-bottom:1px solid #222}
.setting-row input[type="text"],.setting-row input[type="password"]{width:160px;padding:8px;background:var(--bg);border:1px solid #333;border-radius:4px;color:var(--text)}
.setting-row select{padding:8px;background:var(--bg);border:1px solid #333;border-radius:4px;color:var(--text)}

::-webkit-scrollbar{width:8px}
::-webkit-scrollbar-track{background:var(--bg)}
::-webkit-scrollbar-thumb{background:var(--accent-dim);border-radius:4px}
</style>
</head>
<body>
<div class="container">
<div class="header">
<div class="logo"><span>JARVIS</span> v7.0</div>
<div class="status"><div class="status-dot"></div><span>ONLINE</span></div>
</div>

<div class="sidebar">
<h3>Agents</h3>
<button class="agent-btn active" data-agent="general">💬 General</button>
<button class="agent-btn" data-agent="research">📚 Research</button>
<button class="agent-btn" data-agent="coding">💻 Coding</button>
<button class="agent-btn" data-agent="stock">📈 Stocks</button>
<button class="agent-btn" data-agent="marketing">📣 Marketing</button>
<button class="agent-btn" data-agent="news">📰 News</button>
<button class="agent-btn" data-agent="finance">💰 Finance</button>
<button class="agent-btn" data-agent="fitness">💪 Fitness</button>
<button class="agent-btn" data-agent="travel">✈️ Travel</button>
<button class="agent-btn" data-agent="food">🍳 Food</button>

<h3>Voice</h3>
<button class="voice-btn" id="voiceBtn">🎤 Enable Voice</button>

<h3>Integrations</h3>
<button class="agent-btn" onclick="showSettings()">⚙️ Services</button>
</div>

<div class="chat-area">
<div class="messages" id="messages">
<div class="msg assistant"><strong>JARVIS v7.0 TRUE-MERGE</strong> initialized.<br>9 agents ready. What do you need?</div>
</div>
<div class="input-area">
<input type="text" id="input" placeholder="Ask anything..." onkeypress="if(event.key==='Enter')send()">
<button onclick="send()">▸ SEND</button>
</div>
</div>

<div class="right-panel">
<h3>Brain Network</h3>
<div class="brain-viz"><canvas id="brainCanvas"></canvas></div>

<h3>Stats</h3>
<div class="stats">
<div class="stat-row"><span class="stat-label">Messages</span><span class="stat-value" id="msgCount">0</span></div>
<div class="stat-row"><span class="stat-label">Avg Rating</span><span class="stat-value" id="avgRating">-</span></div>
<div class="stat-row"><span class="stat-label">Memory</span><span class="stat-value" id="memory">OK</span></div>
</div>

<div class="settings-panel" id="settingsPanel">
<h3>Services</h3>
<div class="setting-row"><span>Google Calendar</span><input type="checkbox" id="calendar"></div>
<div class="setting-row"><span>Gmail</span><input type="checkbox" id="gmail"></div>
<div class="setting-row"><span>WhatsApp</span><input type="checkbox" id="whatsapp"></div>
<div class="setting-row"><span>SMS Gateway</span><input type="checkbox" id="sms"></div>
<div class="setting-row"><span>API Key</span><input type="password" id="apiKey" placeholder="Enter API key..."></div>
<div class="setting-row"><span>Reminders</span><input type="checkbox" id="reminders"></div>
<div class="setting-row"><span>Web Search</span><input type="checkbox" id="websearch"></div>
<div class="setting-row"><span>Screenshots</span><input type="checkbox" id="screenshots"></div>
<div class="setting-row"><span>Smart Devices</span><input type="checkbox" id="smartdevices"></div>
<button class="agent-btn" onclick="saveSettings()">Save Settings</button>
</div>
</div>
</div>

<script>
// State
let currentAgent = 'general';
let voiceEnabled = false;
let msgCount = 0;

// Send message - TRUE MERGE version with proper error handling
async function send(){
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
  scrollToBottom();
  
  try {
    const response = await fetch('/api/chat', {
      method: 'POST',
      headers: {'Content-Type': 'application/json'},
      body: JSON.stringify({message: msg, agent: currentAgent})
    });
    
    if(!response.ok) throw new Error('HTTP ' + response.status);
    
    const data = await response.json();
    document.getElementById('typing').remove();
    
    if(data.error) {
      addMsg('Error: ' + data.error, 'system');
    } else {
      addMsg(data.response || 'No response', 'assistant');
    }
  } catch(e) {
    document.getElementById('typing').remove();
    addMsg('Connection Error: ' + e.message, 'system');
  }
}

function addMsg(text, cls){
  const m = document.createElement('div');
  m.className = 'msg ' + cls;
  m.innerHTML = text.replace(/\\n/g, '<br>').replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>');
  document.getElementById('messages').appendChild(m);
  scrollToBottom();
}

function scrollToBottom(){
  const msgs = document.getElementById('messages');
  msgs.scrollTop = msgs.scrollHeight;
}

// Agent buttons
document.querySelectorAll('.agent-btn[data-agent]').forEach(btn => {
  btn.addEventListener('click', function(){
    document.querySelectorAll('.agent-btn').forEach(b => b.classList.remove('active'));
    this.classList.add('active');
    currentAgent = this.dataset.agent;
  });
});

// Voice toggle
function toggleVoice(){
  voiceEnabled = !voiceEnabled;
  const btn = document.getElementById('voiceBtn');
  btn.innerText = voiceEnabled ? '🎤 Voice ON' : '🎤 Enable Voice';
  btn.style.background = voiceEnabled ? 'var(--accent)' : '';
}

// Settings
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

// Brain Visualization - from vierisid concept
const canvas = document.getElementById('brainCanvas');
const ctx = canvas.getContext('2d');

// Nodes - from the 9 agents + core
const nodes = [
  {x:150,y:110,label:'CORE',color:'#00d4ff',active:true},
  {x:80,y:50,label:'AI',color:'#00d4ff'},
  {x:220,y:50,label:'MEM',color:'#00d4ff'},
  {x:80,y:170,label:'VOICE',color:'#00d4ff'},
  {x:220,y:170,label:'WEB',color:'#00d4ff'},
  {x:50,y:110,label:'General',color:'#666'},
  {x:100,y:90,label:'Research',color:'#666'},
  {x:250,y:90,label:'Coding',color:'#666'},
  {x:100,y:130,label:'Stock',color:'#666'},
  {x:250,y:130,label:'Food',color:'#666'},
];

function drawBrain(){
  if(!canvas.getContext) return;
  ctx.fillStyle = '#0a0a0f';
  ctx.fillRect(0,0,300,220);
  
  // Connections
  ctx.strokeStyle = '#00d4ff33';
  nodes.forEach(n => {
    nodes.forEach(m => {
      if(n!==m && Math.abs(n.x-m.x) < 80){
        ctx.beginPath();
        ctx.moveTo(n.x,n.y);
        ctx.lineTo(m.x,m.y);
        ctx.stroke();
      }
    });
  });
  
  // Nodes
  nodes.forEach(n => {
    ctx.beginPath();
    ctx.arc(n.x,n.y,12,0,Math.PI*2);
    ctx.fillStyle = n.color;
    ctx.fill();
    ctx.fillStyle = '#e0e0e0';
    ctx.font = '9px Share Tech Mono';
    ctx.textAlign = 'center';
    ctx.fillText(n.label,n.x,n.y-18);
  });
  
  requestAnimationFrame(drawBrain);
}
drawBrain();
</script>
</body>
</html>
'''

class JarvisMergeUI:
    """Merged Jarvis Interface from multiple repos"""
    
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
            return TRON_UI
        
        @self.app.route('/api/chat', methods=['POST'])
        def chat():
            import asyncio
            try:
                data = request.get_json()
                message = data.get("message", "")
        agent = data.get("agent", "general")
                
                loop = asyncio.new_event_loop()
                asyncio.set_event_loop(loop)
                response = loop.run_until_complete(self.jarvis.process(message, agent=agent))
                loop.close()
                
                return jsonify({'response': response})
            except Exception as e:
                logger.error(f"Chat error: {e}")
                return jsonify({'error': str(e)}), 500
        
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
        logger.info(f"JARVIS v7.0 TRUE-MERGE on http://{host}:{port}")
        
        import socket
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
    return JarvisMergeUI(jarvis, config)