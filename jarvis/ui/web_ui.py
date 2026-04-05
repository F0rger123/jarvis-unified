"""
Web UI - Flask-based dashboard
Combines features from danilofalcao/jarvis and vierisid/jarvis
"""

from flask import Flask, render_template_string, request, jsonify
import asyncio
import logging
from pathlib import Path

logger = logging.getLogger('jarvis.ui')

class JarvisWebUI:
    """Flask web interface for Jarvis"""
    
    def __init__(self, jarvis_instance, config: dict):
        self.jarvis = jarvis_instance
        self.config = config
        self.app = Flask(__name__)
        self._setup_routes()
    
    def _setup_routes(self):
        """Setup Flask routes"""
        
        @self.app.route('/')
        def index():
            return self._dashboard_html()
        
        @self.app.route('/chat', methods=['POST'])
        def chat():
            data = request.json
            message = data.get('message', '')
            
            # Run async process in sync context
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            try:
                response = loop.run_until_complete(self.jarvis.process(message))
            finally:
                loop.close()
            
            return jsonify({'response': response})
        
        @self.app.route('/memory')
        def memory():
            memories = self.jarvis.memory.search_memory(request.args.get('q', ''))
            return jsonify(memories)
        
        @self.app.route('/tools')
        def tools():
            tools = self.jarvis.automation.get_available_tools()
            return jsonify({'tools': tools})
        
        @self.app.route('/execute', methods=['POST'])
        def execute_tool():
            data = request.json
            tool = data.get('tool')
            params = data.get('params', {})
            
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            try:
                result = loop.run_until_complete(
                    self.jarvis.automation.execute_tool(tool, params)
                )
            finally:
                loop.close()
            
            return jsonify({'result': result})
    
    def _dashboard_html(self) -> str:
        """Generate the dashboard HTML"""
        return '''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>🤖 Jarvis - AI Assistant</title>
    <style>
        * { box-sizing: border-box; margin: 0; padding: 0; }
        body { 
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
            background: linear-gradient(135deg, #1e3a5f 0%, #2d5a87 100%);
            min-height: 100vh; color: #1a1a1a;
        }
        .container { max-width: 900px; margin: 0 auto; padding: 20px; }
        .header {
            text-align: center; color: white; padding: 30px 0;
        }
        .header h1 { font-size: 2.5rem; margin-bottom: 10px; }
        .status { 
            display: inline-block; padding: 8px 20px; 
            background: rgba(255,255,255,0.1); border-radius: 20px;
            font-size: 0.9rem;
        }
        .card {
            background: white; border-radius: 16px; padding: 24px;
            margin-bottom: 20px; box-shadow: 0 4px 20px rgba(0,0,0,0.1);
        }
        .chat-area {
            display: flex; flex-direction: column; height: 400px;
        }
        .messages {
            flex: 1; overflow-y: auto; padding: 10px;
            background: #f8fafc; border-radius: 12px; margin-bottom: 16px;
        }
        .message { 
            padding: 12px 16px; margin-bottom: 10px; border-radius: 12px;
            max-width: 80%;
        }
        .message.user { 
            background: #3b82f6; color: white; margin-left: auto; 
        }
        .message.assistant { 
            background: #e2e8f0; 
        }
        .input-area { display: flex; gap: 10px; }
        .input-area input {
            flex: 1; padding: 14px; border: 2px solid #e2e8f0;
            border-radius: 12px; font-size: 1rem;
        }
        .input-area input:focus {
            outline: none; border-color: #3b82f6;
        }
        .input-area button {
            padding: 14px 28px; background: #3b82f6; color: white;
            border: none; border-radius: 12px; font-size: 1rem;
            cursor: pointer; transition: background 0.2s;
        }
        .input-area button:hover { background: #2563eb; }
        .tools-grid {
            display: grid; grid-template-columns: repeat(auto-fit, minmax(150px, 1fr));
            gap: 12px;
        }
        .tool-btn {
            padding: 16px; background: #f8fafc; border: 2px solid #e2e8f0;
            border-radius: 12px; text-align: center; cursor: pointer;
            transition: all 0.2s;
        }
        .tool-btn:hover { border-color: #3b82f6; background: #eff6ff; }
        .tool-icon { font-size: 1.5rem; margin-bottom: 8px; }
        .tool-name { font-weight: 600; color: #1e3a5f; }
        .tabs { display: flex; gap: 10px; margin-bottom: 20px; }
        .tab {
            padding: 10px 20px; background: transparent; border: none;
            color: #64748b; cursor: pointer; font-size: 1rem;
        }
        .tab.active { 
            color: #3b82f6; border-bottom: 2px solid #3b82f6; 
        }
        .loading {
            text-align: center; padding: 20px; color: #64748b;
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🤖 Jarvis</h1>
            <span class="status">● Online</span>
        </div>
        
        <div class="card">
            <div class="tabs">
                <button class="tab active" onclick="showTab('chat')">Chat</button>
                <button class="tab" onclick="showTab('tools')">Tools</button>
                <button class="tab" onclick="showTab('memory')">Memory</button>
            </div>
            
            <div id="chat-tab">
                <div class="chat-area">
                    <div class="messages" id="messages">
                        <div class="message assistant">
                            Hello! I'm Jarvis. How can I help you today?
                        </div>
                    </div>
                    <div class="input-area">
                        <input type="text" id="user-input" 
                               placeholder="Type your message..."
                               onkeypress="if(event.key==='Enter')sendMessage()">
                        <button onclick="sendMessage()">Send</button>
                    </div>
                </div>
            </div>
            
            <div id="tools-tab" style="display:none;">
                <div class="tools-grid">
                    <div class="tool-btn" onclick="showTool('files')">
                        <div class="tool-icon">📁</div>
                        <div class="tool-name">Files</div>
                    </div>
                    <div class="tool-btn" onclick="showTool('apps')">
                        <div class="tool-icon">🚀</div>
                        <div class="tool-name">Apps</div>
                    </div>
                    <div class="tool-btn" onclick="showTool('terminal')">
                        <div class="tool-icon">💻</div>
                        <div class="tool-name">Terminal</div>
                    </div>
                    <div class="tool-btn" onclick="showTool('email')">
                        <div class="tool-icon">📧</div>
                        <div class="tool-name">Email</div>
                    </div>
                </div>
            </div>
            
            <div id="memory-tab" style="display:none;">
                <p style="color:#64748b;">Search and view your memories here.</p>
            </div>
        </div>
    </div>
    
    <script>
        async function sendMessage() {
            const input = document.getElementById('user-input');
            const message = input.value.trim();
            if (!message) return;
            
            // Add user message
            addMessage(message, 'user');
            input.value = '';
            
            // Show loading
            const loading = addMessage('Thinking...', 'assistant');
            
            try {
                const response = await fetch('/chat', {
                    method: 'POST',
                    headers: {'Content-Type': 'application/json'},
                    body: JSON.stringify({message})
                });
                const data = await response.json();
                loading.textContent = data.response;
            } catch (e) {
                loading.textContent = 'Error: ' + e.message;
            }
        }
        
        function addMessage(text, type) {
            const div = document.createElement('div');
            div.className = 'message ' + type;
            div.textContent = text;
            document.getElementById('messages').appendChild(div);
            div.scrollIntoView();
            return div;
        }
        
        function showTab(tab) {
            ['chat', 'tools', 'memory'].forEach(t => {
                document.getElementById(t+'-tab').style.display = t === tab ? 'block' : 'none';
            });
            document.querySelectorAll('.tab').forEach((btn, i) => {
                btn.classList.toggle('active', ['chat','tools','memory'][i] === tab);
            });
        }
    </script>
</body>
</html>'''
    
    def run(self, host: str = '0.0.0.0', port: int = 5000):
        """Run the web server"""
        logger.info(f"Starting Jarvis web UI on http://{host}:{port}")
        self.app.run(host=host, port=port, debug=False)