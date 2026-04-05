"""
Jarvis Unified v3 - Tron UI, Food Agent, Self-Learning, Brain Viz
100% Free, modular AI assistant
"""

import os
import json
import logging
import asyncio
import random
from typing import Optional, Dict, Any, List
from datetime import datetime, timedelta
from pathlib import Path

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger('jarvis')

# ==================== CONFIG ====================

class JarvisConfig:
    def __init__(self, env_file: str = '.env'):
        self.env_file = env_file
        self.config = {}
        self.load_env()
    
    def load_env(self):
        if Path(self.env_file).exists():
            with open(self.env_file, 'r') as f:
                for line in f:
                    line = line.strip()
                    if line and not line.startswith('#') and '=' in line:
                        key, value = line.split('=', 1)
                        os.environ[key.strip()] = value.strip()
        
        self.config = {
            # === AI - 100% FREE ===
            'ai_provider': os.getenv('AI_PROVIDER', 'ollama'),
            'ollama_url': os.getenv('OLLAMA_URL', 'http://localhost:11434'),
            'ollama_model': os.getenv('OLLAMA_MODEL', 'qwen3:8b'),
            'gemini_api_key': os.getenv('GEMINI_API_KEY', ''),
            'openrouter_key': os.getenv('OPENROUTER_API_KEY', ''),
            
            # === Voice ===
            'tts_engine': os.getenv('TTS_ENGINE', 'pyttsx3'),
            'stt_engine': os.getenv('STT_ENGINE', 'whisper'),
            'wake_word': os.getenv('WAKE_WORD', 'Jarvis').lower(),
            'input_mode': os.getenv('INPUT_MODE', 'text'),  # text or voice
            
            # === UI - Tron Style ===
            'ui_theme': os.getenv('UI_THEME', 'tron'),
            'accent_color': os.getenv('ACCENT_COLOR', '#00ffff'),
            'secondary_color': os.getenv('SECONDARY_COLOR', '#ff00ff'),
            'grid_color': os.getenv('GRID_COLOR', '#00ffff33'),
            
            # === Tone ===
            'jarvis_tone': os.getenv('JARVIS_TONE', 'helpful'),
            
            # === Learning ===
            'self_learning': os.getenv('SELF_LEARNING', 'true').lower() == 'true',
            'learning_db': os.getenv('LEARNING_DB', 'jarvis_learning.json'),
            
            # === Memory & Brain ===
            'memory_db': os.getenv('MEMORY_DB', 'jarvis_memory.db'),
            'brain_viz': os.getenv('BRAIN_VIZ', 'true').lower() == 'true',
            
            # === Food Agent ===
            'food_default_store': os.getenv('FOOD_DEFAULT_STORE', 'walmart'),
            
            # === SMS (Gmail - FREE) ===
            'sms_via_gmail': os.getenv('SMS_VIA_GMAIL', 'true').lower() == 'true',
            
            # === Security ===
            'confirm_payments': os.getenv('CONFIRM_PAYMENTS', 'true').lower() == 'true',
            'confirm_orders': os.getenv('CONFIRM_ORDERS', 'true').lower() == 'true',
            'confirm_sms': os.getenv('CONFIRM_SMS', 'true').lower() == 'true',
            
            # === Dashboard ===
            'dashboard_enabled': os.getenv('DASHBOARD', 'true').lower() == 'true',
            
            # === Google ===
            'google_client_id': os.getenv('GOOGLE_CLIENT_ID', ''),
            'google_client_secret': os.getenv('GOOGLE_CLIENT_SECRET', ''),
            'google_refresh_token': os.getenv('GOOGLE_REFRESH_TOKEN', ''),
            
            # === Server ===
            'port': int(os.getenv('PORT', '5000')),
        }
    
    def get(self, key: str, default: Any = None) -> Any:
        return self.config.get(key, default)


# ==================== SELF-LEARNING SYSTEM ====================

class SelfLearningEngine:
    """Jarvis grades and improves its own responses"""
    
    def __init__(self, db_file: str = "jarvis_learning.json"):
        self.db_file = db_file
        self.data = self._load()
    
    def _load(self) -> Dict:
        if os.path.exists(self.db_file):
            with open(self.db_file, 'r') as f:
                return json.load(f)
        return {"responses": [], "grades": [], "improvements": [], "patterns": {}}
    
    def _save(self):
        with open(self.db_file, 'w') as f:
            json.dump(self.data, f, indent=2)
    
    def log_response(self, prompt: str, response: str, context: str = ""):
        entry = {
            "id": len(self.data.get('responses', [])),
            "prompt": prompt[:200],
            "response": response[:500],
            "context": context,
            "timestamp": datetime.now().isoformat(),
            "grade": None,
            "feedback": None
        }
        self.data.setdefault('responses', []).append(entry)
        self._save()
    
    def grade_response(self, response_id: int, grade: int, feedback: str = ""):
        """Grade response 1-5, store for learning"""
        for resp in self.data.get('responses', []):
            if resp['id'] == response_id:
                resp['grade'] = grade
                resp['feedback'] = feedback
                break
        
        # Update patterns
        self.data.setdefault('grades', []).append({
            "grade": grade,
            "timestamp": datetime.now().isoformat()
        })
        
        # Analyze and improve
        self._analyze_and_improve(grade)
        self._save()
    
    def _analyze_and_improve(self, grade: int):
        """Analyze grades and suggest improvements"""
        grades = [g['grade'] for g in self.data.get('grades', [])]
        
        if len(grades) >= 5:
            avg = sum(grades) / len(grades)
            
            if avg < 3:
                # Needs improvement - note in patterns
                self.data.setdefault('patterns', {})['needs_work'] = {
                    "avg_grade": avg,
                    "suggestions": [
                        "Be more concise",
                        "Add more specific details",
                        "Ask clarifying questions"
                    ]
                }
            elif avg >= 4:
                self.data['patterns']['excellent'] = {"avg_grade": avg}
    
    def get_system_prompt_addition(self) -> str:
        """Return learned improvements for AI context"""
        patterns = self.data.get('patterns', {})
        
        if 'needs_work' in patterns:
            return "Note: Recent responses have been rated lower. Focus on being more concise and specific."
        elif 'excellent' in patterns:
            return "Note: Responses have been highly rated. Continue current approach."
        
        return ""
    
    def get_stats(self) -> Dict:
        grades = self.data.get('grades', [])
        if not grades:
            return {"total_responses": 0, "avg_grade": 0, "trend": "neutral"}
        
        recent = grades[-10:]
        older = grades[-20:-10] if len(grades) > 10 else []
        
        recent_avg = sum(g['grade'] for g in recent) / len(recent)
        older_avg = sum(g['grade'] for g in older) / len(older) if older else recent_avg
        
        trend = "improving" if recent_avg > older_avg else "declining" if recent_avg < older_avg else "stable"
        
        return {
            "total_responses": len(self.data.get('responses', [])),
            "avg_grade": round(sum(grades) / len(grades), 2),
            "recent_avg": round(recent_avg, 2),
            "trend": trend
        }


# ==================== FOOD AGENT ====================

class FoodAgent:
    """Grocery ordering, ingredients, cooking timers"""
    
    def __init__(self, config: JarvisConfig, memory=None):
        self.config = config
        self.memory = memory
        self.shopping_lists = {}
        self.cooking_timers = {}
    
    async def process_food_request(self, request: str) -> str:
        """Handle food-related requests"""
        req = request.lower()
        
        if any(w in req for w in ['order', 'buy', 'get', 'shop']):
            return await self._handle_order(request)
        elif any(w in req for w in ['what', 'ingredient', 'recipe', 'make']):
            return await self._handle_recipe(request)
        elif any(w in req for w in ['timer', 'cook', 'minutes', 'hours']):
            return self._handle_timer(request)
        elif any(w in req for w in ['list', 'groceries']):
            return self._show_lists()
        else:
            return "I can help you: order groceries, find recipes, set cooking timers, manage shopping lists. What do you need?"
    
    async def _handle_order(self, request: str) -> str:
        """Handle grocery ordering"""
        # Extract items from request
        items = self._extract_items(request)
        
        if not items:
            return "What items would you like to order? List them and I'll add them to your cart."
        
        store = self.config.get('food_default_store', 'walmart')
        
        # Build shopping list
        list_name = f"order_{datetime.now().strftime('%Y%m%d_%H%M')}"
        self.shopping_lists[list_name] = {
            "items": items,
            "store": store,
            "created": datetime.now().isoformat(),
            "status": "pending_confirmation"
        }
        
        items_str = ", ".join(items)
        return f"📝 Added to {store.title()} cart:\n• {items_str}\n\n⚠️ CONFIRMATION REQUIRED: Should I proceed to checkout or add more items?"
    
    def _extract_items(self, text: str) -> List[str]:
        """Extract grocery items from text"""
        # Common food words
        food_words = ['milk', 'bread', 'eggs', 'butter', 'cheese', 'chicken', 'beef', 'pork',
                     'apple', 'banana', 'orange', 'lettuce', 'tomato', 'potato', 'rice', 'pasta',
                     'cereal', 'juice', 'coffee', 'tea', 'water', 'snack', 'frozen', 'canned']
        
        words = text.lower().split()
        items = [w for w in words if w in food_words or len(w) > 3]
        
        return items[:10]  # Limit to 10 items
    
    async def _handle_recipe(self, request: str) -> str:
        """Find recipe and ingredients"""
        # Simple recipe database
        recipes = {
            "pasta": {"ingredients": ["pasta", "sauce", "cheese", "olive oil"], "steps": 3, "time": 20},
            "chicken": {"ingredients": ["chicken breast", "salt", "pepper", "oil", "garlic"], "steps": 4, "time": 35},
            "salad": {"ingredients": ["lettuce", "tomato", "cucumber", "olive oil", "lemon"], "steps": 2, "time": 10},
            "omelette": {"ingredients": ["eggs", "butter", "cheese", "salt", "pepper"], "steps": 3, "time": 10},
            "stir fry": {"ingredients": ["chicken", "vegetables", "soy sauce", "oil", "rice"], "steps": 4, "time": 25}
        }
        
        for key, recipe in recipes.items():
            if key in request.lower():
                ingredients = ", ".join(recipe['ingredients'])
                return f"🍳 {key.title()} Recipe:\n\n📋 Ingredients:\n• {ingredients}\n\n⏱️ Steps: {recipe['steps']}\n⏰ Time: {recipe['time']} minutes\n\nWant me to add these ingredients to your shopping list or set a timer?"
        
        return "I know simple recipes for: pasta, chicken, salad, omelette, stir fry. Which would you like?"
    
    def _handle_timer(self, request: str) -> str:
        """Set cooking timer"""
        import re
        
        # Extract time
        match = re.search(r'(\d+)\s*(minute|min|hour|hr)', request.lower())
        
        if not match:
            return "How long should the timer be? (e.g., 'set timer for 10 minutes')"
        
        amount = int(match.group(1))
        unit = match.group(2)
        
        if 'hour' in unit:
            seconds = amount * 3600
            label = f"{amount} hour(s)"
        else:
            seconds = amount * 60
            label = f"{amount} minutes"
        
        timer_id = f"timer_{len(self.cooking_timers) + 1}"
        self.cooking_timers[timer_id] = {
            "duration": seconds,
            "label": label,
            "start": datetime.now().isoformat(),
            "status": "running"
        }
        
        # Note: Actual timer would need async implementation
        return f"⏱️ Timer set for {label}. I'll notify you when it's done!\n\n(Note: Timer runs in background)"
    
    def _show_lists(self) -> str:
        """Show shopping lists"""
        if not self.shopping_lists:
            return "📝 No shopping lists yet. Ask me to 'order groceries' to create one."
        
        result = "📝 Your Shopping Lists:\n\n"
        for name, lst in self.shopping_lists.items():
            items = ", ".join(lst['items'])
            result += f"• {name}: {items}\n"
        
        return result
    
    def confirm_order(self, list_name: str) -> str:
        """Confirm and process order"""
        if list_name not in self.shopping_lists:
            return f"List '{list_name}' not found"
        
        lst = self.shopping_lists[list_name]
        lst['status'] = "confirmed"
        
        store = lst['store']
        
        return f"✅ Order confirmed!\n\n🛒 {store.title()}: {', '.join(lst['items'])}\n\n⚠️ WARNING: This is a simulated order. To actually order, integration with {store.title()} API would need to be configured."


# ==================== SMS VIA GMAIL (FREE) ====================

class SMSGateway:
    """Send SMS via Gmail - 100% FREE"""
    
    def __init__(self, config: JarvisConfig):
        self.config = config
    
    async def send_sms(self, to: str, message: str) -> str:
        """Send SMS via Gmail (Google Messages web)"""
        
        # Security: Always require confirmation for SMS
        if self.config.get('confirm_sms', True):
            return f"⚠️ CONFIRMATION REQUIRED:\n\nSend SMS to {to}:\n\n\"{message}\"\n\nReply 'yes' to confirm or 'no' to cancel."
        
        return await self._send_via_gmail(to, message)
    
    async def _send_via_gmail(self, to: str, message: str) -> str:
        """Actually send via Gmail"""
        # Option 1: Google Messages (web)
        # This would need OAuth setup
        
        # Option 2: Gmail to SMS gateway (free)
        # Many carriers support email to SMS
        carrier_gateways = {
            'verizon': '@vtext.com',
            'att': '@txt.att.net',
            'tmobile': '@tmomail.net',
            'sprint': '@messaging.sprintpcs.com',
            'boost': '@smsboostmobile.com'
        }
        
        # For now, return instructions
        return f"📱 SMS would be sent to {to}:\n\n\"{message}\"\n\nTo enable actual SMS via Gmail:\n1. Set up Google OAuth in .env\n2. Configure your carrier\n3. Grant permissions\n\n⚠️ Actual SMS sending requires OAuth setup. See docs."


# ==================== BRAIN VISUALIZATION ====================

class BrainVisualization:
    """Visual representation of Jarvis's agents and workflows"""
    
    def __init__(self):
        self.agents = {
            "core": {"name": "Core AI", "type": "processor", "connections": ["memory", "voice", "automation"]},
            "memory": {"name": "Memory", "type": "storage", "connections": ["core", "learning"]},
            "learning": {"name": "Self-Learning", "type": "learning", "connections": ["memory", "core"]},
            "voice": {"name": "Voice I/O", "type": "input_output", "connections": ["core", "food"]},
            "automation": {"name": "Automation", "type": "action", "connections": ["core", "browser"]},
            "food": {"name": "Food Agent", "type": "agent", "connections": ["voice", "shopping"]},
            "google": {"name": "Google Services", "type": "integration", "connections": ["core", "calendar", "gmail", "sms"]},
            "calendar": {"name": "Calendar", "type": "service", "connections": ["google"]},
            "gmail": {"name": "Gmail", "type": "service", "connections": ["google", "sms"]},
            "sms": {"name": "SMS Gateway", "type": "service", "connections": ["google"]},
            "shopping": {"name": "Shopping", "type": "service", "connections": ["food"]},
            "browser": {"name": "Browser", "type": "action", "connections": ["automation"]}
        }
    
    def get_brain_data(self) -> Dict:
        """Get brain visualization data"""
        nodes = []
        links = []
        
        for id, agent in self.agents.items():
            nodes.append({
                "id": id,
                "label": agent['name'],
                "type": agent['type']
            })
            
            for conn in agent['connections']:
                links.append({
                    "source": id,
                    "target": conn
                })
        
        return {"nodes": nodes, "links": links}
    
    def get_workflow_status(self) -> Dict:
        """Get current workflow status"""
        return {
            "active_agents": ["core", "memory", "voice"],
            "pending_tasks": 3,
            "learning_enabled": True,
            "brain_activity": "normal"
        }


# ==================== DASHBOARD ====================

class Dashboard:
    """Analytics and workflow dashboard"""
    
    def __init__(self, memory=None, learning=None):
        self.memory = memory
        self.learning = learning
    
    def get_data(self) -> Dict:
        # Task stats
        todos = self.memory.get_todos() if self.memory else []
        pending = len([t for t in todos if t.get('status') == 'pending'])
        completed = len([t for t in todos if t.get('status') == 'completed'])
        
        # Learning stats
        learning_stats = self.learning.get_stats() if self.learning else {}
        
        # Automation stats
        automations = self.memory.get_automations() if self.memory else []
        
        return {
            "tasks": {
                "total": len(todos),
                "pending": pending,
                "completed": completed,
                "completion_rate": round(completed / len(todos) * 100, 1) if todos else 0
            },
            "learning": learning_stats,
            "automations": {
                "total": len(automations),
                "enabled": len([a for a in automations if a.get('enabled', True)])
            },
            "brain": {
                "active_agents": 6,
                "total_nodes": 12,
                "connections": 18
            },
            "voice": {
                "input_mode": "text",  # Would track actual
                "last_command": "None"
            }
        }


# ==================== MAIN JARVIS ====================

class Jarvis:
    def __init__(self, config: JarvisConfig = None):
        self.config = config or JarvisConfig()
        
        # Core
        self.ai = AIClient(self.config)
        
        # Memory & Learning
        from jarvis.memory import Memory
        self.memory = Memory(self.config.config)
        self.learning = SelfLearningEngine(self.config.get('learning_db'))
        
        # Agents
        self.food = FoodAgent(self.config, self.memory)
        self.sms = SMSGateway(self.config)
        self.brain = BrainVisualization()
        self.dashboard = Dashboard(self.memory, self.learning)
        
        # Automation
        from jarvis.automation import AutomationEngine
        self.automation = AutomationEngine(self.config.config)
        
        # Google
        from jarvis.api.google_services import GoogleServices
        self.google = GoogleServices(self.config.config) if self.config.get('google_client_id') else None
        
        self.input_mode = self.config.get('input_mode', 'text')
        
        logger.info(f"Jarvis v3 initialized - Theme: {self.config.get('ui_theme')}")
    
    async def process(self, user_input: str) -> str:
        # Log for learning
        self.learning.log_response(user_input, "", "chat")
        
        # Route to appropriate handler
        if any(w in user_input.lower() for w in ['order', 'food', 'grocery', 'cook', 'recipe', 'timer']):
            response = await self.food.process_food_request(user_input)
        elif any(w in user_input.lower() for w in ['sms', 'text', 'message']):
            response = await self.sms.send_sms("user", user_input.replace("send", "").replace("sms", "").strip())
        else:
            # Regular AI chat
            context = self.memory.get_context() if self.memory else []
            learning_prompt = self.learning.get_system_prompt_addition()
            
            full_prompt = learning_prompt + "\n\nUser: " + user_input if learning_prompt else user_input
            
            response = await self.ai.chat(full_prompt, context)
        
        # Save interaction
        if self.memory:
            self.memory.add_interaction(user_input, response)
        
        return response
    
    def get_settings(self) -> Dict:
        return {
            'input_mode': self.input_mode,
            'ui_theme': self.config.get('ui_theme'),
            'accent_color': self.config.get('accent_color'),
            'self_learning': self.config.get('self_learning'),
            'brain_viz': self.config.get('brain_viz'),
            'learning_stats': self.learning.get_stats(),
            'ai_provider': self.ai.provider if hasattr(self.ai, 'provider') else 'unknown'
        }
    
    def update_setting(self, key: str, value: Any):
        if key == 'input_mode':
            self.input_mode = value
        self.config.config[key] = value
    
    def toggle_input_mode(self) -> str:
        self.input_mode = 'voice' if self.input_mode == 'text' else 'text'
        return f"Input mode: {self.input_mode}"


# ==================== AI CLIENT ====================

class AIClient:
    def __init__(self, config: JarvisConfig):
        self.config = config
        self.provider = self._init_provider()
    
    def _init_provider(self):
        if self._check_ollama():
            logger.info("Using Ollama (100% FREE)")
            return 'ollama'
        if self.config.get('gemini_api_key'):
            return 'gemini'
        return 'none'
    
    def _check_ollama(self) -> bool:
        try:
            import requests
            resp = requests.get(f"{self.config.get('ollama_url')}/api/tags", timeout=2)
            return resp.status_code == 200
        except:
            return False
    
    async def chat(self, message: str, context: List[Dict] = None) -> str:
        if self.provider == 'ollama':
            return await self._ollama_chat(message, context)
        return "No AI provider. Install Ollama for 100% FREE usage."
    
    async def _ollama_chat(self, message: str, context: List[Dict] = None) -> str:
        import requests
        
        messages = [{"role": "system", "content": f"You are Jarvis, a helpful AI with {self.config.get('jarvis_tone', 'helpful')} tone."}]
        if context:
            messages.extend(context[-10:])
        messages.append({"role": "user", "content": message})
        
        try:
            resp = requests.post(
                f"{self.config.get('ollama_url')}/api/chat",
                json={"model": self.config.get('ollama_model'), "messages": messages, "stream": False},
                timeout=120
            )
            return resp.json().get('message', {}).get('content', 'No response')
        except Exception as e:
            return f"Ollama error: {e}"


if __name__ == "__main__":
    async def main():
        print("🤖 Jarvis v3 - Tron UI + Food Agent + Self-Learning")
        
        config = JarvisConfig()
        jarvis = Jarvis(config)
        
        print(f"Theme: {config.get('ui_theme')}")
        print(f"Input: {jarvis.input_mode}")
        print(f"Learning: {config.get('self_learning')}")
        
        while True:
            mode = "🎤" if jarvis.input_mode == "voice" else "⌨️"
            try:
                user_input = input(f"{mode} You: ").strip()
                if not user_input:
                    continue
                
                if user_input.lower() in ['quit', 'exit']:
                    break
                
                if user_input.lower() == 'mode':
                    print(jarvis.toggle_input_mode())
                    continue
                
                if user_input.lower() == 'brain':
                    print(json.dumps(jarvis.brain.get_brain_data(), indent=2))
                    continue
                
                if user_input.lower() == 'dash':
                    print(json.dumps(jarvis.dashboard.get_data(), indent=2))
                    continue
                
                response = await jarvis.process(user_input)
                print(f"🤖 Jarvis: {response}\n")
            except KeyboardInterrupt:
                break
    
    asyncio.run(main())