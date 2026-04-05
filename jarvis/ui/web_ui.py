"""
Tron-Style UI - Futuristic, Cyberpunk, Mobile-Friendly
"""

from flask import Flask, render_template_string, request, jsonify
import asyncio
import logging

logger = logging.getLogger('jarvis.ui')

class JarvisTronUI:
    """Futuristic Tron-style web interface"""
    
    def __init__(self, jarvis_instance, config: dict):
        self.jarvis = jarvis_instance
        self.config = config
        self.app = Flask(__name__)
        self._setup_routes()
    
    def _setup_routes(self):
        
        @self.app.route('/')
        def index():
            return self._tron_html()
        
        @self.app.route('/api/chat', methods=['POST'])
        def chat():
            data = request.json
            message = data.get('message', '')
            
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            try:
                response = loop.run_until_complete(self.jarvis.process(message))
                
                # Get learning stats for response
                learning_stats = {}
                if hasattr(self.jarvis, 'learning'):
                    learning_stats = self.jarvis.learning.get_stats()
                
            finally:
                loop.close()
            
            return jsonify({'response': response, 'learning': learning_stats})
        
        @self.app.route('/api/settings')
        def get_settings():
            return jsonify(self.jarvis.get_settings())
        
        @self.app.route('/api/settings', methods=['PUT'])
        def update_settings():
            data = request.json
            for key, value in data.items():
                self.jarvis.update_setting(key, value)
            return jsonify({'status': 'ok'})
        
        @self.app.route('/api/mode', methods=['POST'])
        def toggle_mode():
            result = self.jarvis.toggle_input_mode()
            return jsonify({'mode': self.jarvis.input_mode, 'message': result})
        
        @self.app.route('/api/brain')
        def get_brain():
            if hasattr(self.jarvis, 'brain'):
                return jsonify(self.jarvis.brain.get_brain_data())
            return jsonify({'nodes': [], 'links': []})
        
        @self.app.route('/api/dashboard')
        def get_dashboard():
            if hasattr(self.jarvis, 'dashboard'):
                return jsonify(self.jarvis.dashboard.get_data())
            return jsonify({})
        
        @self.app.route('/api/todos')
        def get_todos():
            if self.jarvis.memory:
                return jsonify(self.jarvis.memory.get_todos())
            return jsonify([])
        
        @self.app.route('/api/todos', methods=['POST'])
        def add_todo():
            data = request.json
            if self.jarvis.memory:
                self.jarvis.memory.add_todo(data.get('task', ''), data.get('priority', 'medium'), data.get('due_date'))
            return jsonify({'status': 'added'})
        
        @self.app.route('/api/todos/<int:todo_id>', methods=['PUT'])
        def update_todo(todo_id):
            data = request.json
            if self.jarvis.memory:
                self.jarvis.memory.update_todo(todo_id, data.get('status'), data.get('task'))
            return jsonify({'status': 'updated'})
        
        @self.app.route('/api/grade', methods=['POST'])
        def grade_response():
            """Grade Jarvis's response for self-learning"""
            data = request.json
            if hasattr(self.jarvis, 'learning'):
                self.jarvis.learning.grade_response(
                    data.get('response_id', 0),
                    data.get('grade', 3),
                    data.get('feedback', '')
                )
            return jsonify({'status': 'graded'})
        
        @self.app.route('/api/food/confirm', methods=['POST'])
        def confirm_food_order():
            """Confirm food order with security"""
            data = request.json
            list_name = data.get('list_name', '')
            if hasattr(self.jarvis, 'food'):
                result = self.jarvis.food.confirm_order(list_name)
            else:
                result = "Food agent not available"
            return jsonify({'result': result})
    
    def _tron_html(self) -> str:
        accent = self.config.get('accent_color', '#00ffff')
        grid = self.config.get('grid_color', '#00ffff22')
        
        return f'''<!DOCTYPE html>
<html lang="en" data-theme="dark">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0, user-scalable=no">
    <title>🤖 Jarvis // TRON</title>
    <style>
        :root {{
            --accent: {accent};
            --accent-dim: {accent}66;
            --grid: {grid};
            --bg: #0a0a0f;
            --surface: #0d0d15;
            --surface-bright: #151520;
            --text: #e0e0e0;
            --text-dim: #808090;
            --glow: 0 0 20px {accent}, 0 0 40px {accent}44;
            --border: {accent}33;
        }}
        
        * {{ box-sizing: border-box; margin: 0; padding: 0; }}
        
        body {{
            font-family: 'Orbitron', 'Rajdhani', 'Segoe UI', sans-serif;
            background: var(--bg);
            color: var(--text);
            min-height: 100vh;
            overflow-x: hidden;
            background-image: 
                linear-gradient(var(--grid) 1px, transparent 1px),
                linear-gradient(90deg, var(--grid) 1px, transparent 1px);
            background-size: 50px 50px;
        }}
        
        /* Scanlines */
        body::before {{
            content: '';
            position: fixed;
            inset: 0;
            background: repeating-linear-gradient(
                0deg,
                transparent,
                transparent 2px,
                rgba(0,255,255,0.03) 2px,
                rgba(0,255,255,0.03) 4px
            );
            pointer-events: none;
            z-index: 1000;
        }}
        
        .app-container {{
            max-width: 1200px; margin: 0 auto; padding: 16px;
            display: grid; grid-template-columns: 1fr; gap: 16px;
            min-height: 100vh;
        }}
        
        @media(min-width: 900px) {{
            .app-container {{
                grid-template-columns: 1fr 350px;
            }}
        }}
        
        /* Header */
        .header {{
            grid-column: 1 / -1;
            display: flex; justify-content: space-between; align-items: center;
            padding: 16px 24px;
            background: linear-gradient(180deg, var(--surface) 0%, transparent 100%);
            border: 1px solid var(--border);
            border-radius: 8px;
            position: relative;
            overflow: hidden;
        }}
        
        .header::after {{
            content: '';
            position: absolute;
            bottom: 0; left: 0; right: 0;
            height: 2px;
            background: linear-gradient(90deg, transparent, var(--accent), transparent);
            animation: scan 3s linear infinite;
        }}
        
        @keyframes scan {{
            0% {{ transform: translateX(-100%); }}
            100% {{ transform: translateX(100%); }}
        }}
        
        .logo {{
            font-size: 1.5rem; font-weight: 700;
            text-transform: uppercase;
            letter-spacing: 4px;
            color: var(--accent);
            text-shadow: var(--glow);
        }}
        
        .status-bar {{
            display: flex; gap: 16px; align-items: center;
        }}
        
        .status-item {{
            font-size: 0.75rem; color: var(--text-dim);
            display: flex; align-items: center; gap: 6px;
        }}
        
        .status-dot {{
            width: 8px; height: 8px; border-radius: 50%;
            background: var(--accent);
            box-shadow: 0 0 10px var(--accent);
            animation: pulse 2s infinite;
        }}
        
        @keyframes pulse {{
            0%, 100% {{ opacity: 1; }}
            50% {{ opacity: 0.5; }}
        }}
        
        /* Main Chat */
        .main-panel {{
            display: flex; flex-direction: column;
            background: var(--surface);
            border: 1px solid var(--border);
            border-radius: 8px;
            overflow: hidden;
        }}
        
        /* Brain Visualization */
        .brain-panel {{
            height: 200px;
            background: var(--surface-bright);
            border-bottom: 1px solid var(--border);
            position: relative;
            overflow: hidden;
        }}
        
        .brain-canvas {{
            width: 100%; height: 100%;
        }}
        
        .brain-overlay {{
            position: absolute; top: 8px; left: 12px;
            font-size: 0.7rem; color: var(--accent);
            text-transform: uppercase; letter-spacing: 2px;
        }}
        
        /* Messages */
        .messages {{
            flex: 1; min-height: 300px;
            padding: 16px; overflow-y: auto;
            display: flex; flex-direction: column; gap: 12px;
        }}
        
        .message {{
            padding: 14px 18px; border-radius: 4px;
            max-width: 85%; line-height: 1.5;
            position: relative;
            animation: fadeIn 0.3s ease;
        }}
        
        @keyframes fadeIn {{
            from {{ opacity: 0; transform: translateY(10px); }}
            to {{ opacity: 1; transform: translateY(0); }}
        }}
        
        .message.user {{
            background: linear-gradient(135deg, var(--accent-dim) 0%, transparent 100%);
            border-left: 3px solid var(--accent);
            align-self: flex-end;
        }}
        
        .message.assistant {{
            background: var(--surface-bright);
            border-left: 3px solid var(--accent);
            align-self: flex-start;
        }}
        
        .message .meta {{
            font-size: 0.65rem; color: var(--text-dim);
            margin-top: 6px;
        }}
        
        .grade-buttons {{
            display: flex; gap: 4px; margin-top: 8px;
        }}
        
        .grade-btn {{
            padding: 2px 8px; font-size: 0.7rem;
            background: var(--surface); border: 1px solid var(--border);
            color: var(--text-dim); cursor: pointer;
            border-radius: 3px;
        }}
        
        .grade-btn:hover {{ background: var(--accent-dim); }}
        
        /* Input */
        .input-area {{
            display: flex; gap: 8px; padding: 16px;
            border-top: 1px solid var(--border);
            background: var(--surface-bright);
        }}
        
        .input-area input {{
            flex: 1; padding: 14px 18px;
            background: var(--bg); border: 1px solid var(--border);
            color: var(--text); font-size: 0.95rem;
            border-radius: 4px; font-family: inherit;
        }}
        
        .input-area input:focus {{
            outline: none; border-color: var(--accent);
            box-shadow: 0 0 10px var(--accent-dim);
        }}
        
        .input-area button {{
            padding: 14px 20px;
            background: linear-gradient(180deg, var(--accent) 0%, #008888 100%);
            border: none; color: var(--bg); font-weight: 700;
            border-radius: 4px; cursor: pointer;
            text-transform: uppercase; letter-spacing: 1px;
        }}
        
        .mode-toggle {{
            padding: 14px;
            background: var(--surface-bright); border: 1px solid var(--border);
            color: var(--accent); cursor: pointer; border-radius: 4px;
            font-size: 1.2rem;
        }}
        
        /* Side Panel */
        .side-panel {{
            display: flex; flex-direction: column; gap: 16px;
        }}
        
        .panel {{
            background: var(--surface);
            border: 1px solid var(--border);
            border-radius: 8px; padding: 16px;
        }}
        
        .panel-title {{
            font-size: 0.75rem; color: var(--accent);
            text-transform: uppercase; letter-spacing: 2px;
            margin-bottom: 12px;
            display: flex; align-items: center; gap: 8px;
        }}
        
        .panel-title::before {{
            content: '▶'; font-size: 0.6rem;
        }}
        
        /* Dashboard Stats */
        .stats-grid {{
            display: grid; grid-template-columns: 1fr 1fr; gap: 8px;
        }}
        
        .stat-card {{
            background: var(--surface-bright);
            padding: 12px; border-radius: 4px;
            text-align: center;
        }}
        
        .stat-value {{
            font-size: 1.5rem; font-weight: 700;
            color: var(--accent);
            text-shadow: var(--glow);
        }}
        
        .stat-label {{
            font-size: 0.65rem; color: var(--text-dim);
            text-transform: uppercase;
        }}
        
        /* Tasks */
        .task-item {{
            display: flex; align-items: center; gap: 8px;
            padding: 8px; background: var(--surface-bright);
            border-radius: 4px; margin-bottom: 6px;
        }}
        
        .task-check {{
            width: 16px; height: 16px;
            border: 1px solid var(--accent);
            border-radius: 2px; cursor: pointer;
        }}
        
        .task-check.checked {{
            background: var(--accent);
        }}
        
        /* Navigation */
        .nav-tabs {{
            display: flex; gap: 4px; overflow-x: auto; padding-bottom: 8px;
        }}
        
        .nav-tab {{
            padding: 8px 16px;
            background: transparent; border: 1px solid var(--border);
            color: var(--text-dim); font-size: 0.75rem;
            text-transform: uppercase; cursor: pointer;
            border-radius: 4px; white-space: nowrap;
        }}
        
        .nav-tab.active {{
            background: var(--accent-dim);
            border-color: var(--accent);
            color: var(--accent);
        }}
        
        /* Sections */
        .section {{ display: none; }}
        .section.active {{ display: block; }}
        
        /* Settings */
        .setting-row {{
            display: flex; justify-content: space-between;
            padding: 10px 0; border-bottom: 1px solid var(--border);
        }}
        
        .setting-label {{ font-size: 0.85rem; }}
        
        select, input[type="color"] {{
            background: var(--bg); border: 1px solid var(--border);
            color: var(--text); padding: 6px 10px; border-radius: 4px;
        }}
        
        /* Voice Indicator */
        .voice-indicator {{
            display: flex; align-items: center; justify-content: center;
            gap: 3px; height: 30px;
            margin-bottom: 8px;
        }}
        
        .voice-bar {{
            width: 3px; background: var(--accent);
            border-radius: 2px; animation: sound 0.5s ease infinite;
        }}
        
        @keyframes sound {{
            0%, 100% {{ height: 10px; }}
            50% {{ height: 25px; }}
        }}
        
        /* Mobile */
        @media(max-width: 600px) {{
            .app-container {{ padding: 8px; }}
            .header {{ padding: 12px 16px; }}
            .logo {{ font-size: 1rem; letter-spacing: 2px; }}
            .messages {{ min-height: 200px; }}
            .side-panel {{ display: none; }}
        }}
    </style>
    <link href="https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700&family=Rajdhani:wght@400;600&display=swap" rel="stylesheet">
</head>
<body>
    <div class="app-container">
        <div class="header">
            <div class="logo">JARVIS <span style="color:var(--text-dim)">//</span> TRON</div>
            <div class="status-bar">
                <div class="status-item"><span class="status-dot"></span> ONLINE</div>
                <div class="status-item" id="inputModeDisplay">TEXT MODE</div>
                <div class="status-item" id="learningStatus">LEARNING: ON</div>
            </div>
        </div>
        
        <div class="main-panel">
            <div class="brain-panel">
                <canvas class="brain-canvas" id="brainCanvas"></canvas>
                <div class="brain-overlay">// BRAIN INTERFACE</div>
            </div>
            
            <div class="voice-indicator" id="voiceIndicator" style="display:none;">
                <div class="voice-bar" style="animation-delay:0s"></div>
                <div class="voice-bar" style="animation-delay:0.1s"></div>
                <div class="voice-bar" style="animation-delay:0.2s"></div>
                <div class="voice-bar" style="animation-delay:0.3s"></div>
                <div class="voice-bar" style="animation-delay:0.4s"></div>
            </div>
            
            <div class="messages" id="messages">
                <div class="message assistant">
                    🤖 Jarvis v3 initialized. All systems operational.
                    <div class="meta">SECURE // TRON MODE // FREE</div>
                </div>
            </div>
            
            <div class="input-area">
                <button class="mode-toggle" id="modeBtn" onclick="toggleMode()">⌨️</button>
                <input type="text" id="userInput" placeholder="Enter command..." onkeypress="if(event.key==='Enter')sendMessage()">
                <button onclick="sendMessage()">SEND</button>
            </div>
        </div>
        
        <div class="side-panel">
            <div class="panel">
                <div class="panel-title">Dashboard</div>
                <div class="stats-grid">
                    <div class="stat-card">
                        <div class="stat-value" id="statTasks">0</div>
                        <div class="stat-label">Tasks</div>
                    </div>
                    <div class="stat-card">
                        <div class="stat-value" id="statBrain">12</div>
                        <div class="stat-label">Nodes</div>
                    </div>
                    <div class="stat-card">
                        <div class="stat-value" id="statLearning">0%</div>
                        <div class="stat-label">Grade</div>
                    </div>
                    <div class="stat-card">
                        <div class="stat-value" id="statAgents">6</div>
                        <div class="stat-label">Agents</div>
                    </div>
                </div>
            </div>
            
            <div class="panel">
                <div class="panel-title">Tasks</div>
                <div id="taskList"></div>
            </div>
            
            <div class="panel">
                <div class="panel-title">Quick Actions</div>
                <div class="nav-tabs">
                    <div class="nav-tab active" onclick="showSection('chat')">Chat</div>
                    <div class="nav-tab" onclick="showSection('food')">Food</div>
                    <div class="nav-tab" onclick="showSection('settings')">Config</div>
                </div>
            </div>
        </div>
    </div>
    
    <script>
        let currentMode = 'text';
        let responseId = 0;
        
        // Initialize
        window.onload = function() {{
            loadDashboard();
            initBrainViz();
        }};
        
        async function toggleMode() {{
            const res = await fetch('/api/mode', {{method: 'POST'}});
            const data = await res.json();
            currentMode = currentMode === 'text' ? 'voice' : 'text';
            document.getElementById('modeBtn').textContent = currentMode === 'text' ? '⌨️' : '🎤';
            document.getElementById('inputModeDisplay').textContent = currentMode.toUpperCase() + ' MODE';
            document.getElementById('voiceIndicator').style.display = currentMode === 'voice' ? 'flex' : 'none';
        }};
        
        async function sendMessage() {{
            const input = document.getElementById('userInput');
            const msg = input.value.trim();
            if(!msg) return;
            
            addMessage(msg, 'user');
            input.value = '';
            
            try {{
                const res = await fetch('/api/chat', {{
                    method: 'POST',
                    headers: {{'Content-Type': 'application/json'}},
                    body: JSON.stringify({{message: msg}})
                }});
                const data = await res.json();
                
                addMessage(data.response, 'assistant', data.learning);
                responseId++;
            }} catch(e) {{
                addMessage('Error: ' + e.message, 'assistant');
            }}
        }};
        
        function addMessage(text, type, learning = null) {{
            const div = document.createElement('div');
            div.className = 'message ' + type;
            
            let content = text;
            if(type === 'assistant' && learning && learning.total_responses > 0) {{
                content += `<div class="meta">Grade: ${learning.avg_grade}/5 | Trend: ${learning.trend}</div>`;
                content += `<div class="grade-buttons">
                    <button class="grade-btn" onclick="grade(1)">1</button>
                    <button class="grade-btn" onclick="grade(2)">2</button>
                    <button class="grade-btn" onclick="grade(3)">3</button>
                    <button class="grade-btn" onclick="grade(4)">4</button>
                    <button class="grade-btn" onclick="grade(5)">5</button>
                </div>`;
            }}
            
            div.innerHTML = content;
            document.getElementById('messages').appendChild(div);
            div.scrollIntoView();
        }};
        
        async function grade(score) {{
            await fetch('/api/grade', {{
                method: 'POST',
                headers: {{'Content-Type': 'application/json'}},
                body: JSON.stringify({{response_id: responseId, grade: score}})
            }});
            alert('Response graded: ' + score + '/5');
        }};
        
        async function loadDashboard() {{
            try {{
                const res = await fetch('/api/dashboard');
                const data = await res.json();
                
                if(data.tasks) {{
                    document.getElementById('statTasks').textContent = data.tasks.pending;
                }}
                if(data.learning) {{
                    document.getElementById('statLearning').textContent = data.learning.avg_grade + '%';
                }}
            }} catch(e) {{}}
        }};
        
        function initBrainViz() {{
            const canvas = document.getElementById('brainCanvas');
            const ctx = canvas.getContext('2d');
            
            // Simple animated brain visualization
            const nodes = [
                {{x: 150, y: 80, label: 'CORE'}, {{x: 80, y: 150, label: 'MEMORY'},
                {{x: 220, y: 150, label: 'VOICE'}, {{x: 80, y: 220, label: 'FOOD'},
                {{x: 220, y: 220, label: 'GOOGLE'}, {{x: 150, y: 280, label: 'LEARN'}}
            ];
            
            let frame = 0;
            function animate() {{
                frame++;
                ctx.fillStyle = '#0a0a0f';
                ctx.fillRect(0, 0, canvas.width, canvas.height);
                
                // Draw nodes
                nodes.forEach((n, i) => {{
                    const yOff = Math.sin(frame * 0.02 + i) * 5;
                    ctx.beginPath();
                    ctx.arc(n.x, n.y + yOff, 20, 0, Math.PI * 2);
                    ctx.strokeStyle = '#00ffff';
                    ctx.lineWidth = 2;
                    ctx.stroke();
                    
                    ctx.fillStyle = '#00ffff';
                    ctx.font = '10px Orbitron';
                    ctx.textAlign = 'center';
                    ctx.fillText(n.label, n.x, n.y + yOff - 25);
                }});
                
                // Draw connections
                ctx.strokeStyle = '#00ffff33';
                ctx.lineWidth = 1;
                for(let i = 0; i < nodes.length; i++) {{
                    for(let j = i + 1; j < nodes.length; j++) {{
                        ctx.beginPath();
                        ctx.moveTo(nodes[i].x, nodes[i].y);
                        ctx.lineTo(nodes[j].x, nodes[j].y);
                        ctx.stroke();
                    }}
                }}
                
                requestAnimationFrame(animate);
            }}
            
            canvas.width = canvas.offsetWidth;
            canvas.height = canvas.offsetHeight;
            animate();
        }};
        
        function showSection(name) {{
            // Placeholder for section switching
            console.log('Section:', name);
        }};
    </script>
</body>
</html>'''
    
    def run(self, host: str = '0.0.0.0', port: int = 5000):
        logger.info(f"Starting Jarvis TRON UI on http://{host}:{port}")
        self.app.run(host=host, port=port, debug=False)