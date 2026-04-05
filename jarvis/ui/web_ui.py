"""
Enhanced Web UI - Mobile-friendly, customizable, speech visual
"""

from flask import Flask, render_template_string, request, jsonify
import asyncio
import logging

logger = logging.getLogger('jarvis.ui')

class JarvisWebUI:
    """Enhanced Flask web interface"""
    
    def __init__(self, jarvis_instance, config: dict):
        self.jarvis = jarvis_instance
        self.config = config
        self.app = Flask(__name__)
        self._setup_routes()
    
    def _setup_routes(self):
        
        @self.app.route('/')
        def index():
            return self._dashboard_html()
        
        @self.app.route('/api/chat', methods=['POST'])
        def chat():
            data = request.json
            message = data.get('message', '')
            
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            try:
                response = loop.run_until_complete(self.jarvis.process(message))
            finally:
                loop.close()
            
            return jsonify({'response': response})
        
        @self.app.route('/api/settings')
        def get_settings():
            return jsonify(self.jarvis.get_settings())
        
        @self.app.route('/api/settings', methods=['PUT'])
        def update_settings():
            data = request.json
            for key, value in data.items():
                self.jarvis.update_setting(key, value)
            return jsonify({'status': 'ok', 'settings': self.jarvis.get_settings()})
        
        @self.app.route('/api/screen-share', methods=['POST'])
        def toggle_screen():
            enabled = self.jarvis.toggle_screen_share()
            return jsonify({'enabled': enabled})
        
        @self.app.route('/api/todos')
        def get_todos():
            if self.jarvis.memory:
                return jsonify(self.jarvis.memory.get_todos())
            return jsonify([])
        
        @self.app.route('/api/todos', methods=['POST'])
        def add_todo():
            data = request.json
            if self.jarvis.memory:
                self.jarvis.memory.add_todo(
                    data.get('task', ''),
                    data.get('priority', 'medium'),
                    data.get('due_date')
                )
            return jsonify({'status': 'added'})
        
        @self.app.route('/api/todos/<int:todo_id>', methods=['PUT'])
        def update_todo(todo_id):
            data = request.json
            if self.jarvis.memory:
                self.jarvis.memory.update_todo(todo_id, data.get('status'), data.get('task'))
            return jsonify({'status': 'updated'})
        
        @self.app.route('/api/todos/<int:todo_id>', methods=['DELETE'])
        def delete_todo(todo_id):
            if self.jarvis.memory:
                self.jarvis.memory.delete_todo(todo_id)
            return jsonify({'status': 'deleted'})
        
        @self.app.route('/api/gestures')
        def get_gestures():
            if self.jarvis.memory:
                return jsonify(self.jarvis.memory.get_gestures())
            return jsonify([])
        
        @self.app.route('/api/gestures', methods=['POST'])
        def add_gesture():
            data = request.json
            if self.jarvis.memory:
                self.jarvis.memory.add_gesture(data.get('name'), data.get('action'), data.get('trigger', ''))
            return jsonify({'status': 'added'})
        
        @self.app.route('/api/calendar')
        def get_calendar():
            if hasattr(self.jarvis, 'google') and self.jarvis.google:
                events = self.jarvis.google.get_events(7)
                return jsonify(events)
            return jsonify([])
        
        @self.app.route('/api/calendar', methods=['POST'])
        def create_event():
            data = request.json
            if hasattr(self.jarvis, 'google') and self.jarvis.google:
                from datetime import datetime
                start = datetime.fromisoformat(data.get('start'))
                result = self.jarvis.google.create_event(
                    data.get('title', 'Event'),
                    start,
                    data.get('duration', 60),
                    data.get('description', '')
                )
                return jsonify({'result': result})
            return jsonify({'error': 'Google not configured'})
        
        @self.app.route('/api/automations')
        def get_automations():
            if self.jarvis.memory:
                return jsonify(self.jarvis.memory.get_automations())
            return jsonify([])
    
    def _dashboard_html(self) -> str:
        theme = self.config.get('theme', 'dark')
        accent = self.config.get('accent_color', '#3b82f6')
        
        return f'''<!DOCTYPE html>
<html lang="en" data-theme="{theme}">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0, user-scalable=no">
    <title>🤖 Jarvis</title>
    <style>
        :root {{
            --bg: { '#0f172a' if theme == 'dark' else '#f8fafc' };
            --surface: { '#1e293b' if theme == 'dark' else '#ffffff' };
            --text: { '#f1f5f9' if theme == 'dark' else '#1e293b' };
            --text-muted: { '#94a3b8' if theme == 'dark' else '#64748b' };
            --accent: {accent};
            --accent-hover: {accent}dd;
            --border: { '#334155' if theme == 'dark' else '#e2e8f0' };
        }}
        
        * {{ box-sizing: border-box; margin: 0; padding: 0; -webkit-tap-highlight-color: transparent; }}
        
        body {{
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
            background: var(--bg); color: var(--text);
            min-height: 100vh; overflow-x: hidden;
        }}
        
        .app-container {{
            max-width: 600px; margin: 0 auto; padding: 16px;
            display: flex; flex-direction: column; min-height: 100vh;
        }}
        
        /* Header */
        .header {{
            display: flex; justify-content: space-between; align-items: center;
            padding: 12px 0; margin-bottom: 16px;
        }}
        .header h1 {{ font-size: 1.5rem; }}
        .header-buttons {{ display: flex; gap: 8px; }}
        .icon-btn {{
            width: 40px; height: 40px; border-radius: 12px;
            background: var(--surface); border: 1px solid var(--border);
            font-size: 1.2rem; cursor: pointer; display: flex;
            align-items: center; justify-content: center;
        }}
        
        /* Speech Visual */
        .speech-visual {{
            background: var(--surface); border-radius: 16px; padding: 20px;
            margin-bottom: 16px; min-height: 80px; display: flex;
            align-items: center; justify-content: center;
        }}
        .speech-bars {{
            display: flex; align-items: center; gap: 3px; height: 40px;
        }}
        .bar {{
            width: 4px; background: var(--accent); border-radius: 2px;
            transition: height 0.1s ease;
        }}
        .speech-text {{ font-size: 1.1rem; text-align: center; }}
        
        /* Chat */
        .chat-card {{
            background: var(--surface); border-radius: 16px;
            flex: 1; display: flex; flex-direction: column;
            overflow: hidden; margin-bottom: 16px;
        }}
        .messages {{
            flex: 1; padding: 16px; overflow-y: auto;
            display: flex; flex-direction: column; gap: 12px;
        }}
        .message {{
            padding: 12px 16px; border-radius: 16px; max-width: 85%;
            line-height: 1.5;
        }}
        .message.user {{
            background: var(--accent); color: white; align-self: flex-end;
        }}
        .message.assistant {{
            background: var(--border); align-self: flex-start;
        }}
        
        .input-area {{
            display: flex; gap: 8px; padding: 12px; border-top: 1px solid var(--border);
        }}
        .input-area input {{
            flex: 1; padding: 14px; border-radius: 12px;
            border: 1px solid var(--border); background: var(--bg);
            color: var(--text); font-size: 1rem;
        }}
        .input-area button {{
            padding: 14px 20px; border-radius: 12px; border: none;
            background: var(--accent); color: white; font-weight: 600;
            cursor: pointer;
        }}
        
        /* Bottom Nav */
        .bottom-nav {{
            display: flex; gap: 8px; padding: 8px 0;
            overflow-x: auto;
        }}
        .nav-chip {{
            padding: 10px 16px; border-radius: 20px; white-space: nowrap;
            background: var(--surface); border: 1px solid var(--border);
            cursor: pointer; font-size: 0.9rem;
        }}
        .nav-chip.active {{
            background: var(--accent); color: white; border-color: var(--accent);
        }}
        
        /* Sections */
        .section {{ display: none; }}
        .section.active {{ display: block; }}
        
        .card {{
            background: var(--surface); border-radius: 16px;
            padding: 16px; margin-bottom: 12px;
        }}
        .card h3 {{ font-size: 1rem; margin-bottom: 12px; color: var(--text-muted); }}
        
        /* Settings */
        .setting-row {{
            display: flex; justify-content: space-between; align-items: center;
            padding: 12px 0; border-bottom: 1px solid var(--border);
        }}
        .setting-row:last-child {{ border: none; }}
        .setting-label {{ font-size: 0.95rem; }}
        .setting-value {{ color: var(--text-muted); font-size: 0.9rem; }}
        
        select, input[type="text"], input[type="color"] {{
            padding: 8px 12px; border-radius: 8px;
            border: 1px solid var(--border); background: var(--bg);
            color: var(--text);
        }}
        
        .toggle {{
            width: 48px; height: 26px; border-radius: 13px;
            background: var(--border); position: relative; cursor: pointer;
            transition: background 0.2s;
        }}
        .toggle.on {{ background: var(--accent); }}
        .toggle::after {{
            content: ''; position: absolute; width: 22px; height: 22px;
            background: white; border-radius: 50%; top: 2px; left: 2px;
            transition: transform 0.2s;
        }}
        .toggle.on::after {{ transform: translateX(22px); }}
        
        /* Todos */
        .todo-item {{
            display: flex; align-items: center; gap: 12px;
            padding: 12px; border-radius: 12px; background: var(--bg);
            margin-bottom: 8px;
        }}
        .todo-check {{
            width: 24px; height: 24px; border-radius: 6px;
            border: 2px solid var(--border); cursor: pointer;
        }}
        .todo-check.checked {{ background: var(--accent); border-color: var(--accent); }}
        .todo-text {{ flex: 1; }}
        .todo-text.done {{ text-decoration: line-through; opacity: 0.6; }}
        
        /* FAB */
        .fab {{
            position: fixed; bottom: 80px; right: 20px;
            width: 56px; height: 56px; border-radius: 50%;
            background: var(--accent); color: white; border: none;
            font-size: 1.5rem; cursor: pointer;
            box-shadow: 0 4px 12px rgba(0,0,0,0.3);
        }}
        
        @media (max-width: 600px) {{
            .app-container {{ padding: 12px; }}
            .message {{ max-width: 90%; }}
        }}
    </style>
</head>
<body>
    <div class="app-container">
        <div class="header">
            <h1>🤖 Jarvis</h1>
            <div class="header-buttons">
                <button class="icon-btn" onclick="showSettings()">⚙️</button>
                <button class="icon-btn" onclick="toggleScreenShare()">📺</button>
            </div>
        </div>
        
        <div class="speech-visual" id="speechVisual">
            <div class="speech-text" id="speechText">Ready to help!</div>
        </div>
        
        <div class="chat-card">
            <div class="messages" id="messages">
                <div class="message assistant">Hello! I'm Jarvis. What can I help you with?</div>
            </div>
            <div class="input-area">
                <input type="text" id="userInput" placeholder="Type or speak..." 
                       onkeypress="if(event.key==='Enter')sendMessage()">
                <button onclick="sendMessage()">➤</button>
            </div>
        </div>
        
        <div class="bottom-nav">
            <div class="nav-chip active" onclick="showSection('chat', this)">💬 Chat</div>
            <div class="nav-chip" onclick="showSection('tasks', this)">📋 Tasks</div>
            <div class="nav-chip" onclick="showSection('calendar', this)">📅 Calendar</div>
            <div class="nav-chip" onclick="showSection('automations', this)">⚡ Auto</div>
            <div class="nav-chip" onclick="showSection('gestures', this)">👋 Gestures</div>
        </div>
        
        <!-- Tasks Section -->
        <div id="tasks-section" class="section">
            <div class="card">
                <h3>📋 Your Tasks</h3>
                <div id="todoList"></div>
            </div>
            <button class="fab" onclick="addTodo()">+</button>
        </div>
        
        <!-- Calendar Section -->
        <div id="calendar-section" class="section">
            <div class="card">
                <h3>📅 Upcoming Events</h3>
                <div id="calendarEvents"></div>
            </div>
        </div>
        
        <!-- Automations Section -->
        <div id="automations-section" class="section">
            <div class="card">
                <h3>⚡ Automations</h3>
                <p style="color:var(--text-muted)">Configure automated tasks (daily emails, etc.)</p>
            </div>
        </div>
        
        <!-- Gestures Section -->
        <div id="gestures-section" class="section">
            <div class="card">
                <h3>👋 Your Gestures</h3>
                <div id="gestureList"></div>
            </div>
        </div>
        
        <!-- Settings Modal -->
        <div id="settings-modal" style="display:none;position:fixed;inset:0;background:rgba(0,0,0,0.5);align-items:center;justify-content:center;z-index:100;">
            <div class="card" style="max-width:400px;width:90%;max-height:80vh;overflow-y:auto;">
                <h3>⚙️ Settings</h3>
                <div class="setting-row">
                    <span>Tone</span>
                    <select id="toneSelect" onchange="updateSetting('jarvis_tone', this.value)">
                        <option value="helpful">Helpful</option>
                        <option value="humorous">Humorous</option>
                        <option value="sassy">Sassy</option>
                        <option value="formal">Formal</option>
                        <option value="friendly">Friendly</option>
                    </select>
                </div>
                <div class="setting-row">
                    <span>Wake Word</span>
                    <input type="text" id="wakeWord" style="width:100px" onchange="updateSetting('wake_word', this.value)">
                </div>
                <div class="setting-row">
                    <span>Theme</span>
                    <select id="themeSelect" onchange="updateSetting('theme', this.value);location.reload()">
                        <option value="dark">Dark</option>
                        <option value="light">Light</option>
                    </select>
                </div>
                <div class="setting-row">
                    <span>Accent Color</span>
                    <input type="color" id="accentColor" onchange="updateSetting('accent_color', this.value);location.reload()">
                </div>
                <div class="setting-row">
                    <span>Screen Share</span>
                    <div class="toggle" id="screenToggle" onclick="toggleScreenShare()"></div>
                </div>
                <div class="setting-row">
                    <span>Microphone</span>
                    <select id="micSelect"><option value="default">Default</option></select>
                </div>
                <div class="setting-row">
                    <span>Browser</span>
                    <select id="browserSelect" onchange="updateSetting('default_browser', this.value)">
                        <option value="chrome">Chrome</option>
                        <option value="edge">Edge</option>
                        <option value="firefox">Firefox</option>
                    </select>
                </div>
                <button onclick="closeSettings()" style="width:100%;padding:12px;margin-top:16px;background:var(--accent);color:white;border:none;border-radius:8px;">Done</button>
            </div>
        </div>
    </div>
    
    <script>
        let currentSection = 'chat';
        
        function showSection(section, btn) {{
            currentSection = section;
            document.querySelectorAll('.section').forEach(s => s.classList.remove('active'));
            document.getElementById(section + '-section').classList.add('active');
            document.querySelectorAll('.nav-chip').forEach(c => c.classList.remove('active'));
            btn.classList.add('active');
            
            if(section === 'tasks') loadTodos();
            if(section === 'calendar') loadCalendar();
            if(section === 'gestures') loadGestures();
        }}
        
        async function sendMessage() {{
            const input = document.getElementById('userInput');
            const msg = input.value.trim();
            if(!msg) return;
            
            addMessage(msg, 'user');
            input.value = '';
            
            // Show speech visual
            document.getElementById('speechText').textContent = 'Thinking...';
            
            try {{
                const res = await fetch('/api/chat', {{
                    method: 'POST',
                    headers: {{'Content-Type': 'application/json'}},
                    body: JSON.stringify({{message: msg}})
                }});
                const data = await res.json();
                addMessage(data.response, 'assistant');
                document.getElementById('speechText').textContent = data.response.substring(0, 50) + '...';
                setTimeout(() => document.getElementById('speechText').textContent = 'Ready to help!', 3000);
            }} catch(e) {{
                addMessage('Error: ' + e.message, 'assistant');
            }}
        }}
        
        function addMessage(text, type) {{
            const div = document.createElement('div');
            div.className = 'message ' + type;
            div.textContent = text;
            document.getElementById('messages').appendChild(div);
            div.scrollIntoView();
        }}
        
        function showSettings() {{
            document.getElementById('settings-modal').style.display = 'flex';
            loadSettings();
        }}
        
        function closeSettings() {{
            document.getElementById('settings-modal').style.display = 'none';
        }}
        
        async function loadSettings() {{
            const res = await fetch('/api/settings');
            const settings = await res.json();
            document.getElementById('toneSelect').value = settings.tone || 'helpful';
            document.getElementById('wakeWord').value = settings.wake_word || 'Jarvis';
            document.getElementById('themeSelect').value = settings.theme || 'dark';
            document.getElementById('accentColor').value = settings.accent_color || '#3b82f6';
            if(settings.screen_share) document.getElementById('screenToggle').classList.add('on');
            document.getElementById('browserSelect').value = settings.default_browser || 'chrome';
        }}
        
        async function updateSetting(key, value) {{
            await fetch('/api/settings', {{
                method: 'PUT',
                headers: {{'Content-Type': 'application/json'}},
                body: JSON.stringify({{[key]: value}})
            }});
        }}
        
        async function toggleScreenShare() {{
            const res = await fetch('/api/screen-share', {{method: 'POST'}});
            const data = await res.json();
            document.getElementById('screenToggle').classList.toggle('on', data.enabled);
        }}
        
        async function loadTodos() {{
            const res = await fetch('/api/todos');
            const todos = await res.json();
            document.getElementById('todoList').innerHTML = todos.map(t => `
                <div class="todo-item">
                    <div class="todo-check ${{t.status === 'completed' ? 'checked' : ''}}" 
                         onclick="toggleTodo(${{t.id}}, '${{t.status}}')"></div>
                    <span class="todo-text ${{t.status === 'completed' ? 'done' : ''}}">${{t.task}}</span>
                </div>
            `).join('');
        }}
        
        async function toggleTodo(id, status) {{
            await fetch('/api/todos/' + id, {{
                method: 'PUT',
                headers: {{'Content-Type': 'application/json'}},
                body: JSON.stringify({{status: status === 'completed' ? 'pending' : 'completed'}})
            }});
            loadTodos();
        }}
        
        async function addTodo() {{
            const task = prompt('New task:');
            if(task) {{
                await fetch('/api/todos', {{
                    method: 'POST',
                    headers: {{'Content-Type': 'application/json'}},
                    body: JSON.stringify({{task: task, priority: 'medium'}})
                }});
                loadTodos();
            }}
        }}
        
        async function loadCalendar() {{
            const res = await fetch('/api/calendar');
            const events = await res.json();
            document.getElementById('calendarEvents').innerHTML = events.length ? events.map(e => `
                <div class="todo-item"><span class="todo-text">${{e.summary}} - ${{e.start || 'TBD'}}</span></div>
            `).join('') : '<p style="color:var(--text-muted)">No upcoming events</p>';
        }}
        
        async function loadGestures() {{
            const res = await fetch('/api/gestures');
            const gestures = await res.json();
            document.getElementById('gestureList').innerHTML = gestures.length ? gestures.map(g => `
                <div class="todo-item"><span class="todo-text">${{g.name}} → ${{g.action}}</span></div>
            `).join('') : '<p style="color:var(--text-muted)">No gestures learned yet</p>';
        }}
    </script>
</body>
</html>'''
    
    def run(self, host: str = '0.0.0.0', port: int = 5000):
        logger.info(f"Starting Jarvis UI on http://{host}:{port}")
        self.app.run(host=host, port=port, debug=False)